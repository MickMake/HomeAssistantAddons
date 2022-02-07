#!/usr/bin/env python3

# Copyright (c) 2017 Dennis Mellican
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from SungrowModbusTcpClient import SungrowModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from importlib import import_module
from threading import Thread

import paho.mqtt.client as mqtt
import datetime
import logging
import getopt
import json
import time
import sys
import re


MIN_SIGNED   = -2147483648
MAX_UNSIGNED =  4294967295


##Load options
options = {}
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = 'i:p:m:M:o:U:P:l:s:t'
long_options = ['ip=', 'port=', 'model=', 'mqtt_host=', 'mqtt_port=',
                 'mqtt_user=', 'mqtt_pass=', 'log_level=', 'scan=', 'timeout=']
try:
    arguments, values = getopt.getopt(
        argument_list, short_options, long_options)
except getopt.error as e:
    raise ValueError('Invalid parameters!')

for current_argument, current_value in arguments:
    if current_value == 'null' or len(current_value) == 0 or current_value.isspace():
        pass
    elif current_argument in ("-i", "--ip"):
        options['inverter_ip'] = current_value
    elif current_argument in ("-p", "--port"):
        options['inverter_port'] = current_value
    elif current_argument in ("-m", "--model"):
        options['model'] = current_value
    elif current_argument in ("-M", "--mqtt_host"):
        options['mqtt_host'] = current_value 
    elif current_argument in ("-o", "--mqtt_port"):
        options['mqtt_port'] = int(current_value)
    elif current_argument in ("-U", "--mqtt_user"):
        options['mqtt_user'] = current_value 
    elif current_argument in ("-P", "--mqtt_pass"):
        options['mqtt_pass'] = current_value 
    elif current_argument in ("-l", "--log_level"):
        options['log_level'] = current_value
    elif current_argument in ("-s", "--scan"):
        options['scan_interval'] = int(current_value)
    elif current_argument in ("-t", "--timeout"):
        options['timeout'] = int(current_value)

    
if options['log_level'] == 'WARNING':
    log_level = logging.WARNING
elif options['log_level'] == 'INFO':
    log_level = logging.INFO
else:
    log_level = logging.DEBUG
logging.basicConfig(level=log_level)

if "sungrow-" in options['model']:
    options['slave'] = 0x01
else:
    options['slave'] = 3



# SMA datatypes and their register lengths
# S = Signed Number, U = Unsigned Number, STR = String
sma_moddatatype = {
  "S16": 1,
  "U16": 1,
  "S32": 2,
  "U32": 2,
  "U64": 4,
  "STR16": 8,
  "STR32": 16,
}

# Load the modbus register map for the inverter
modmap_file = f"modbus-{options['model']}"
try:
    modmap = import_module(modmap_file)
except ModuleNotFoundError:
    logging.error(f"Unable to locate {modmap_file}.py")
    sys.exit(1)

# This will try the Sungrow client otherwise will default to the standard library.
client_payload = {
    "host": options['inverter_ip'],
    "timeout": options['timeout'],
    "RetryOnEmpty": True,
    "retries": 3,
    "port": options['inverter_port'],
}

if "sungrow-" in options['model']:
    logging.info(f"Create SungrowModbusTcpClient. Model: {options['model']}")
    client = SungrowModbusTcpClient.SungrowModbusTcpClient(**client_payload)
else:
    logging.info(f"Create ModbusTcpClient. Model: {options['model']}")
    client = ModbusTcpClient(**client_payload)

client.connect()
client.close()
logging.info("Modbus connected")

# Configure MQTT
mqtt_client = mqtt.Client("ModbusTCP")
mqtt_client.username_pw_set(options['mqtt_user'], options['mqtt_pass'])
if options['mqtt_port'] == 8883:
    mqtt_client.tls_set()

mqtt_client.connect(options['mqtt_host'], port=options['mqtt_port'])
logging.info("Configured MQTT Client")

# Inverter Scanning
inverter = {}
bus = json.loads(modmap.scan)

def load_registers(register_type, start, count=100):
    try:
        if register_type == "read":
            rr = client.read_input_registers(
                int(start),
                count=count,
                unit=options['slave'],
            )
        elif register_type == "holding":
            rr = client.read_holding_registers(
                int(start),
                count=count,
                unit=options['slave'],
            )
        else:
            raise RuntimeError(f"Unsupported register type: {type}")
    except Exception as err:
        logging.warning("No data. Try increasing the timeout or scan interval.")
        return False

    if rr.isError():
        logging.warning("Modbus connection failed")
        return False

    if not hasattr(rr, 'registers'):
        logging.warning("No registers returned")
        return

    if len(rr.registers) != count:
        logging.warning(f"Mismatched number of registers read {len(rr.registers)} != {count}")
        return

    overflow_regex = re.compile(r"(?P<register_name>[a-zA-Z0-9_\.]+)_overflow$")
    divide_regex = re.compile(r"(?P<register_name>[a-zA-Z0-9_]+)_(?P<divide_by>[0-9\.]+)$")

    for num in range(0, count):
        run = int(start) + num + 1

        if register_type == "read" and modmap.read_register.get(str(run)):
            register_name = modmap.read_register.get(str(run))
            register_value = rr.registers[num]

            # Check if the modbus map has an '_overflow' on the end
            # If so the value 'could' be negative (65535 - x) where (-x) is the actual number
            # So a value of '64486' actually represents '-1049'
            # We rely on a second '_indicator' register to tell is if it's actually negative or not, otherwise it's ambigious!
            should_overflow = overflow_regex.match(register_name)

            if should_overflow:
                register_name = should_overflow["register_name"]

                # Find the indicator register value
                indicator_name = f"{register_name}_indicator"

                for reg_num, reg_name in modmap.read_register.items():
                    if reg_name == indicator_name:
                        indicator_register = int(reg_num)
                        break
                else:
                    indicator_register = None

                if indicator_register is not None:
                    # Given register '5084' and knowing start of '5000' we can assume the index
                    # Of our indicator value is 5084 - 5000 - 1 (because of the 'off by 1')
                    indicator_value = rr.registers[indicator_register - int(start) - 1]

                    if indicator_value == 65535:
                        # We are in overflow
                        register_value = -1 * (65535 - register_value)

            # Check if the modbus map has an '_10' or '_100' etc on the end
            # If so, we divide by that and drop it from the name
            should_divide = divide_regex.match(register_name)

            if should_divide:
                register_name = should_divide["register_name"]
                register_value = float(register_value) / float(should_divide["divide_by"])

            # Set the final register name and value, any adjustments above included
            inverter[register_name] = register_value
        elif register_type == "holding" and modmap.holding_register.get(str(run)):
            register_name = modmap.holding_register.get(str(run))
            register_value = rr.registers[num]

            inverter[register_name] = register_value

    return True

# Function for polling data from the target and triggering writing to log file if set
def load_sma_register(registers):
    # Request each register from datasets, omit first row which contains only column headers
    for thisrow in registers:
        name = thisrow[0]
        startPos = thisrow[1]
        type = thisrow[2]
        format = thisrow[3]
    
        # If the connection is somehow not possible (e.g. target not responding)
        # show a error message instead of excepting and stopping
        try:
            received = client.read_input_registers(
                address=startPos,
                count=sma_moddatatype[type],
                unit=options['slave']
            )
        except Exception:
            thisdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.error(f"{thisdate}: Connection not possible, check settings or connection")
            return
    
        message = BinaryPayloadDecoder.fromRegisters(received.registers, endian=Endian.Big)

        # Provide the correct result depending on the defined datatype
        if type == "S32":
            interpreted = message.decode_32bit_int()
        elif type == "U32":
            interpreted = message.decode_32bit_uint()
        elif type == "U64":
            interpreted = message.decode_64bit_uint()
        elif type == "STR16":
            interpreted = message.decode_string(16)
        elif type == "STR32":
            interpreted = message.decode_string(32)
        elif type == "S16":
            interpreted = message.decode_16bit_int()
        elif type == "U16":
            interpreted = message.decode_16bit_uint()
        else:
            # If no data type is defined do raw interpretation of the delivered data
            interpreted = message.decode_16bit_uint()
    
        # Check for "None" data before doing anything else
        if ((interpreted == MIN_SIGNED) or (interpreted == MAX_UNSIGNED)):
            displaydata = None
        else:
            # Put the data with correct formatting into the data table
            if format == "FIX3":
                displaydata = float(interpreted) / 1000
            elif format == "FIX2":
                displaydata = float(interpreted) / 100
            elif format == "FIX1":
                displaydata = float(interpreted) / 10
            else:
                displaydata = interpreted
    
        logging.debug(f"************** {name} = {displaydata}")
        inverter[name] = displaydata
  
    # Add timestamp
    inverter["Timestamp"] = datetime.datetime.now().strftime("%Y-%mm-%dd %H:%M:%S")

def publish_mqtt_discovery(inverter):
    mqtt_client.reconnect()
    logging.info("Publish Home Assistant Discovery message")

    SENSOR_TOPIC = 'inverter_{}/tele/SENSOR'.format(options['model'])
    DISCOVERY_TOPIC = 'homeassistant/sensor/inverter{}/{}/config'.format(options['model'], "{}") # energy/power
    if "sungrow-" in options['model']:
        manufacturer = 'Sungrow'
    else:
        manufacturer = 'SMA'
    DISCOVERY_PAYLOAD = '{{"name": "Inverter {}", "uniq_id":"{}","stat_t": "{}", "json_attr_t": "{}", "unit_of_meas": "{}","dev_cla": "{}","state_class": "{}", "val_tpl": "{{{{ value_json.{} }}}}", "ic": "mdi:solar-power","device":{{ "name": "Solar Inverter","mf": "{}", "mdl": "{}", "connections":[["address", "{}" ]] }} }}'
    
    energy_today_msg = DISCOVERY_PAYLOAD.format("Energy Today","inverter_energy_today", SENSOR_TOPIC, SENSOR_TOPIC, "kWh", "energy", "total_increasing", "daily_power_yield / 1000", manufacturer, options['model'], options['inverter_ip'])
    energy_month_msg = DISCOVERY_PAYLOAD.format("Energy Monthly","inverter_energy_month", SENSOR_TOPIC, SENSOR_TOPIC, "kWh", "energy", "total_increasing", "monthly_power_yield / 1000", manufacturer, options['model'], options['inverter_ip'])
    power_msg = DISCOVERY_PAYLOAD.format("Power", "inverter_power", SENSOR_TOPIC, SENSOR_TOPIC, "W", "power", "measurement","total_pv_power", manufacturer, options['model'], options['inverter_ip'], options['inverter_port'])
    tempertature_msg = DISCOVERY_PAYLOAD.format("Temperature", "inverter_temperature", SENSOR_TOPIC, SENSOR_TOPIC, "°C", "temperature", "measurement","internal_temp", manufacturer, options['model'], options['inverter_ip'], options['inverter_port'])
    daily_energy_consumpt_msg = DISCOVERY_PAYLOAD.format("Daily Energy Consumption", "inverter_energy_consumpt_daily", SENSOR_TOPIC, SENSOR_TOPIC, "kWh", "energy", "total_increasing","daily_energy_consumption / 1000", manufacturer, options['model'], options['inverter_ip'], options['inverter_port'])
    daily_energy_import_msg = DISCOVERY_PAYLOAD.format("Daily Energy Import", "inverter_energy_import_daily", SENSOR_TOPIC, SENSOR_TOPIC, "kWh", "energy", "total_increasing","daily_purchased_energy / 1000", manufacturer, options['model'], options['inverter_ip'], options['inverter_port'])
    

    result = mqtt_client.publish(DISCOVERY_TOPIC.format("energy_today"), energy_today_msg)
    result = mqtt_client.publish(DISCOVERY_TOPIC.format("energy_monthly"), energy_month_msg)        
    result = mqtt_client.publish(DISCOVERY_TOPIC.format("power"), power_msg)
    result = mqtt_client.publish(DISCOVERY_TOPIC.format("temperature"), tempertature_msg)
    result = mqtt_client.publish(DISCOVERY_TOPIC.format("daily_energy_consumpt"), daily_energy_consumpt_msg)
    result = mqtt_client.publish(DISCOVERY_TOPIC.format("daily_energy_import"), daily_energy_import_msg)
    
    result.wait_for_publish()




def publish_mqtt(inverter):
    # After a while you'll need to reconnect, so just reconnect before each publish
    mqtt_client.reconnect()
    SENSOR_TOPIC = 'inverter_{}/tele/SENSOR'.format(options['model'])
    result = mqtt_client.publish(SENSOR_TOPIC, json.dumps(inverter).replace('"', '\"'))
    result.wait_for_publish()


    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        # See https://github.com/eclipse/paho.mqtt.python/blob/master/src/paho/mqtt/client.py#L149 for error code mapping
        logging.error(f"Failed to publish to MQTT with error code: {result.rc}")
    else:
        logging.info("Published to MQTT")

    return result

# Core monitoring loop
def scrape_inverter():
    """ Connect to the inverter and scrape the metrics """
    client.connect()

    if "sungrow-" in options['model']:
        for i in bus["read"]:
            if not load_registers("read", i["start"], int(i["range"])):
                return False

        for i in bus["holding"]:
            if not load_registers("holding", i["start"], int(i["range"])):
                return False
  
        # Sungrow inverter specifics:
        # Work out if the grid power is being imported or exported
        if options['model'] == "sungrow-sh5k":
            try:
                if inverter["grid_import_or_export"] == 65535:
                    export_power = (65535 - inverter["export_power"]) * -1
                    inverter["export_power"] = export_power
            except Exception:
                pass

        try:
            inverter["timestamp"] = "%s-%02d-%02dT%s:%02d:%02d" % (
                inverter["year"],
                inverter["month"],
                inverter["day"],
                inverter["hour"],
                inverter["minute"],
                inverter["second"],
            )
            del inverter["year"]
            del inverter["month"]
            del inverter["day"]
            del inverter["hour"]
            del inverter["minute"]
            del inverter["second"]
        except Exception:
            pass
    elif "sma-" in options['model']:
        load_sma_register(modmap.sma_registers)
    else:
        raise RuntimeError(f"Unsupported inverter model detected: {options['model']}")

    client.close()

    logging.info(inverter)
    return True

#Publish once
publish_mqtt_discovery(inverter)

while True:
    # Scrape the inverter
    success = scrape_inverter()

    if not success:
        logging.warning("Failed to scrape inverter, sleeping until next scan")
        time.sleep(options['scan_interval'])
        continue

    # Optionally publish the metrics if enabled
    if mqtt_client is not None:
        t = Thread(target=publish_mqtt, args=(inverter,))
        t.start()

    # Sleep until the next scan
    time.sleep(options['scan_interval'])