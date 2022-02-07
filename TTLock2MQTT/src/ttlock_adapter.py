import paho.mqtt.client as mqtt
import time
import threading
import concurrent.futures
import getopt
import sys
import logging
from ttlockwrapper import TTLock, TTlockAPIError, constants


class TTLock2MQTTClient(mqtt.Client):
    def __init__(self, ttlock, broker, port, broker_user, broker_pass, keepalive):
        super().__init__(self.mqttClientId, False)
        self.ttlock = ttlock

        self.connected_flag = False
        self.on_connect = TTLock2MQTTClient.cb_on_connect
        self.on_disconnect = TTLock2MQTTClient.cb_on_disconnect
        self.on_message = TTLock2MQTTClient.cb_on_message
        self.broker_host = broker
        self.broker_port = port
        self.keepalive_mqtt = keepalive
        if broker_user and broker_pass:
            self.username_pw_set(broker_user, password=broker_pass)
        if port == 8883:
            self.tls_set()
        logging.info("Client {} TTlock Mqtt Created".format(
            self.mqttClientId))
        self.COMMAND_TOPIC = None

    def sendMensage(self, topic, msg, retain=False):
        logging.debug('Client {} sending mensage "{}" to topic "{}" and retained {}'.format(
            self.mqttClientId, msg, topic, retain))
        self.publish(topic, msg, 0, retain)

    def mqttConnection(self):
        logging.debug("Client {} try connection at {}:{}".format(
            self.mqttClientId, self.broker_host, self.broker_port))
        self.connect(self.broker_host, self.broker_port, self.keepalive_mqtt)

    @classmethod
    def cb_on_message(cls, client, userdata, message):
        try:
            time.sleep(1)
            logging.debug("Client {} message received: {}".format(client.mqttClientId, str(message.payload.decode("utf-8"))))
            client.handleMessage(message)
        except Exception:
            logging.exception('Client {} error on received mqtt message'.format(client.getLockId()))

    @classmethod
    def cb_on_disconnect(cls, client, userdata, rc):
        client.connected_flag = False  # set flag
        logging.info("Client {} disconnected!".format(client.mqttClientId))

    @classmethod
    def cb_on_connect(cls, client, userdata, flags, rc):
        try:
            if rc == 0:
                client.connected_flag = True  # set flag
                logging.info("Client {} connected OK!".format(client.mqttClientId))
                if client.COMMAND_TOPIC:
                    logging.info("Client {} subscribe on command topic: {}".format(
                        client.mqttClientId, client.COMMAND_TOPIC))
                    client.subscribe(client.COMMAND_TOPIC)
                client.sendDiscoveryMsgs()
                time.sleep(20)
                client.forcePublishInfos()
            else:
                logging.error("Client {} Bad connection Returned code= {}".format(
                    client.mqttClientId, rc))
        except Exception:
            logging.exception('Client {} error on connect'.format(client.mqttClientId))


class TTLock2MQTTClientGateway(TTLock2MQTTClient):

    def __init__(self, gateway, ttlock, broker, port, broker_user, broker_pass, connection_info_delay, keepalive):
        self.gateway = gateway
        self.mqttClientId = "GATEWAY-{}-{}".format(str(self.getGatewayId()), str(int(time.time())))
        super().__init__(ttlock, broker, port, broker_user, broker_pass, keepalive)

        self.DISCOVERY_GATEWAY_CONNECTION_TOPIC = 'homeassistant/binary_sensor/ttlock/{}_gateway/config'.format(
            self.getGatewayId())
        self.CONNECTION_BINARY_SENSOR_TOPIC = 'TTLock2MQTT/{}/connection'.format(
            self.getGatewayId())
        self.CONNECTION_BINARY_SENSOR_PAYLOAD = '{{"device_class": "connectivity", "name": "{} connection", "state_topic": "{}", "value_template": "{{{{ value_json.connection }}}}", "uniq_id":"{}_CONNECTION","device":{{"identifiers":["{}"], "name": "TTLOCK_GATEWAY_{}", "connections":[["mac","{}"]]}} }}'
        self.CONNECTION_PAYLOAD = '{{"connection": "{}"}}'

        self.lastConnectionPublishInfo = time.time()
        self.connection_info_delay = connection_info_delay
        

    def getGatewayId(self):
        return self.gateway.get(constants.GATEWAY_ID_FIELD)

    def getMac(self):
        return self.gateway.get(constants.GATEWAY_MAC_FIELD)

    def getName(self):
        return self.gateway.get('gatewayName')
    
    def updateGatewayJson(self):
        try:
            for gateway in self.ttlock.get_gateway_generator():
                if gateway.get(constants.GATEWAY_ID_FIELD)==self.getGatewayId():
                    self.gateway = gateway
                    return
        except Exception as error:
            logging.error('Client {} error while update Gateway Json: {}'.format(
                self.mqttClientId, str(error)))

    def publishInfos(self):
        if time.time()-self.lastConnectionPublishInfo > self.connection_info_delay:
            self.updateGatewayJson()
            self.forcePublishConnectionInfo()

    def forcePublishConnectionInfo(self):
        try:
            logging.info(
                'Client {} publish connection info.'.format(self.mqttClientId))
            self.sendGatewayConnectionLevel()
        except Exception as error:
            logging.error('Client {} error: {}'.format(
                self.mqttClientId, str(error)))
        finally:
            self.lastConnectionPublishInfo = time.time()
    
    def forcePublishInfos(self):
        self.forcePublishConnectionInfo()

    def sendGatewayConnectionLevel(self):
        connectionState = 'ON' if self.gateway.get('isOnline') else 'OFF'
        msg = self.CONNECTION_PAYLOAD.format(connectionState)
        self.sendMensage(self.CONNECTION_BINARY_SENSOR_TOPIC, msg)

    def sendDiscoveryMsgs(self):
        logging.info(
            'Client {} sending discoveries msgs.'.format(self.mqttClientId))
        msg = self.CONNECTION_BINARY_SENSOR_PAYLOAD.format(self.getName(
        ), self.CONNECTION_BINARY_SENSOR_TOPIC, self.getGatewayId(), self.getGatewayId(), self.getGatewayId(), self.getMac())
        self.sendMensage(self.DISCOVERY_GATEWAY_CONNECTION_TOPIC, msg, True)


class TTLock2MQTTClientLock(TTLock2MQTTClient):

    def __init__(self, lock, gateway, ttlock, broker, port, broker_user, broker_pass, state_delay, battery_delay, keepalive):
        self.lock = lock
        self.gateway = gateway
        self.mqttClientId = "LOCK-{}-{}".format(str(self.getLockId()), str(int(time.time())))
        super().__init__(ttlock, broker, port, broker_user, broker_pass, keepalive)

        self.DISCOVERY_LOCK_TOPIC = 'homeassistant/lock/ttlock/{}_lock/config'.format(
            self.getLockId())
        self.DISCOVERY_SENSOR_TOPIC = 'homeassistant/sensor/ttlock/{}_battery/config'.format(
            self.getLockId())
        self.BATTERY_LEVEL_SENSOR_TOPIC = 'TTLock2MQTT/{}/battery'.format(
            self.getLockId())
        self.COMMAND_TOPIC = 'TTLock2MQTT/{}/command'.format(self.getLockId())
        self.STATE_SENSOR_TOPIC = 'TTLock2MQTT/{}/state'.format(
            self.getLockId())
        self.DISCOVERY_LOCK_PAYLOAD = '{{"name": "{} lock", "command_topic": "{}", "state_topic": "{}", "value_template": "{{{{ value_json.state }}}}", "uniq_id":"{}_lock","device":{{"identifiers":["{}"], "name": "TTLOCK_LOCK_{}", "connections":[["mac","{}"]]}} }}'
        self.DISCOVERY_BATTERY_LEVEL_SENSOR_PAYLOAD = '{{"device_class": "battery", "name": "{} battery", "state_topic": "{}", "unit_of_measurement": "%", "value_template": "{{{{ value_json.battery }}}}", "uniq_id":"{}_battery","device":{{"identifiers":["{}"], "name": "TTLOCK_LOCK_{}", "connections":[["mac","{}"]]}} }}'
        self.STATE_PAYLOAD = '{{"state": "{}"}}'
        self.BATTERY_LEVEL_PAYLOAD = '{{"battery": {}}}'

        self.lastStatePublishInfo = time.time()
        self.lastBatteryPublishInfo = time.time()
        self.state_delay = state_delay
        self.battery_delay = battery_delay

    def getName(self):
        return self.lock.get(constants.LOCK_ALIAS_FIELD)

    def getLockId(self):
        return self.lock.get(constants.LOCK_ID_FIELD)

    def getMac(self):
        return self.lock.get(constants.LOCK_MAC_FIELD)

    def getGatewayId(self):
        return self.gateway.get(constants.GATEWAY_ID_FIELD)

    def handleMessage(self, message):
        result = False
        command = str(message.payload.decode("utf-8"))
        if command == 'LOCK':
            result = self.ttlock.lock(self.getLockId())
        elif command == 'UNLOCK':
            result = self.ttlock.unlock(self.getLockId())
        else:
            logging.info('Invalid command.')
            return
        if not result:
            logging.warning(
                'Client {} has fail to send API command.'.format(self.mqttClientId))
            # todo: send unavailble msg
            return
        time.sleep(3)
        self.forcePublishStateInfo()

    def publishInfos(self):
        if time.time()-self.lastStatePublishInfo > self.state_delay:
            self.forcePublishStateInfo()
        if time.time()-self.lastBatteryPublishInfo > self.battery_delay:
            self.forcePublishBatteryInfo()

    def forcePublishStateInfo(self):
        try:
            logging.info(
                'Client {} publish lock state.'.format(self.mqttClientId))
            self.sendLockState()
        except Exception as error:
            logging.error('Client {} error: {}'.format(
                self.mqttClientId, str(error)))
        finally:
            self.lastStatePublishInfo = time.time()

    def forcePublishBatteryInfo(self):
        try:
            logging.info(
                'Client {} publish battery info.'.format(self.mqttClientId))
            self.sendLockBatteryLevel()
        except Exception as error:
            logging.error('Client {} error: {}'.format(
                self.mqttClientId, str(error)))
        finally:
            self.lastBatteryPublishInfo = time.time()
    
    def forcePublishInfos(self):
        self.forcePublishStateInfo()
        self.forcePublishBatteryInfo()

    def sendLockBatteryLevel(self):
        batteryLevel = self.ttlock.lock_electric_quantity(self.getLockId())
        msg = self.BATTERY_LEVEL_PAYLOAD.format(batteryLevel)
        self.sendMensage(self.BATTERY_LEVEL_SENSOR_TOPIC, msg)

    def sendLockState(self):
        # Open state of lock:0-locked,1-unlocked,2-unknown
        state = self.ttlock.lock_state(self.getLockId())
        if state == 2:
            logging.warning(
                'Client {} lock state TTlockAPI return "unknown".'.format(self.mqttClientId))
            return
        lock_is = 'UNLOCKED' if state else 'LOCKED'
        msg = self.STATE_PAYLOAD.format(lock_is)
        self.sendMensage(self.STATE_SENSOR_TOPIC, msg, True)

    def sendDiscoveryMsgs(self):
        logging.info(
            'Client {} sending discoveries msgs.'.format(self.mqttClientId))
        msg = self.DISCOVERY_BATTERY_LEVEL_SENSOR_PAYLOAD.format(self.getName(
        ), self.BATTERY_LEVEL_SENSOR_TOPIC, self.getLockId(), self.getLockId(), self.getLockId(), self.getMac())
        self.sendMensage(self.DISCOVERY_SENSOR_TOPIC, msg, True)

        msg = self.DISCOVERY_LOCK_PAYLOAD.format(self.getName(), self.COMMAND_TOPIC, self.STATE_SENSOR_TOPIC, self.getLockId(
        ), self.getLockId(), self.getLockId(), self.getMac())
        self.sendMensage(self.DISCOVERY_LOCK_TOPIC, msg, True)


def client_loop(ttlock2MqttClient, loop_delay=2.0, run_forever=False):
    try:
        logging.info("Client {} TTlock Mqtt on client_loop".format(
            ttlock2MqttClient.mqttClientId))
        bad_connection = 0
        ttlock2MqttClient.mqttConnection()
        while run_flag:  # loop
            ttlock2MqttClient.loop(loop_delay)
            if ttlock2MqttClient.connected_flag:
                ttlock2MqttClient.publishInfos()
            else:
                if bad_connection > 5 and not run_forever:
                    logging.error("Client {} has 5 times bad connection".format(
                        ttlock2MqttClient.mqttClientId))
                    break
                bad_connection += 1
                time.sleep(10)

        if ttlock2MqttClient.connected_flag:
            ttlock2MqttClient.disconnect()

    except Exception as e:
        logging.exception("Client {} Loop Thread Error ".format(
            ttlock2MqttClient.mqttClientId))

    finally:
        logging.debug("Client {} return future".format(
            ttlock2MqttClient.mqttClientId))
        return ttlock2MqttClient

def create_futures(id,client):
    if not client:
        logging.debug('TTlock Element {} Client is empty...'.format(id))
    elif id in client_futures.keys() and not client_futures.get(id).done():
        logging.debug('TTlock Element {} Client already created...'.format(id))
    else:
        client_futures[id] = executor.submit(client_loop, client)
    time.sleep(DELAY_BETWEEN_NEW_THREADS_CREATION)

def createClients(broker, port, broker_user, broker_pass, ttlock_client, ttlock_token,state_delay,battery_delay):
    ttlock = TTLock(ttlock_client, ttlock_token)
    ttlock2MqttClient = None
    for gateway in ttlock.get_gateway_generator():
        ttlock2MqttClient = TTLock2MQTTClientGateway(gateway, ttlock, broker, port, broker_user, broker_pass, battery_delay, DELAY_BETWEEN_LOCK_PUBLISH_INFOS*2)
        create_futures(gateway.get(constants.GATEWAY_ID_FIELD),ttlock2MqttClient)
        for lock in ttlock.get_locks_per_gateway_generator(gateway.get(constants.GATEWAY_ID_FIELD)):
            ttlock2MqttClient = TTLock2MQTTClientLock(
                    lock, gateway, ttlock, broker, port, broker_user, broker_pass, state_delay, battery_delay, DELAY_BETWEEN_LOCK_PUBLISH_INFOS*2)
            create_futures(lock.get(constants.LOCK_ID_FIELD),ttlock2MqttClient)
        

def main(broker, port, broker_user, broker_pass, ttlock_client, ttlock_token,state_delay,battery_delay):
    try:
        if not ttlock_client or not ttlock_token:
            raise ValueError('Invalid ttlock client or token.')

        logging.debug("Starting main loop...")
        while True:
            try:
                createClients(broker, port, broker_user, broker_pass,
                              ttlock_client, ttlock_token,state_delay,battery_delay)
                logging.info("Current threads: {}".format(
                    threading.active_count()))
            except Exception as e:
                logging.exception("Error main method {}".format(e))
                time.sleep(DELAY_BETWEEN_NEW_THREADS_CREATION)

    except KeyboardInterrupt:
        logging.info("Ending...")
        global run_flag
        run_flag = False
        for id, future in client_futures.items():
            logging.info("Client {} thread is over!".format(
                future.result().mqttClientId))
    except ValueError as e:
        logging.exception('Exiting script...')

def create_access_token(user, password, clientId, clientSecret):
    redirect_url = "https://yourdomain.com"
    result=TTLock.get_token(clientId,clientSecret,user,password,redirect_url)
    if result.get(constants.ACCESS_TOKEN_FIELD):
        return result.get(constants.ACCESS_TOKEN_FIELD)
    else:
        raise TTlockAPIError()


def isEmptyStr(s):
    return s == 'null' or len(s) == 0 or s.isspace()


DELAY_BETWEEN_NEW_THREADS_CREATION = 60
DELAY_BETWEEN_LOCK_PUBLISH_INFOS = 60
run_flag = True
client_futures = dict()
executor = concurrent.futures.ThreadPoolExecutor()

if __name__ == '__main__':

    broker = 'localhost'
    port = 1883
    broker_user = None
    broker_pass = None
    ttlock_user = None
    ttlock_pass = None
    ttlock_client = None
    ttlock_secret = None
    
    scan_interval = DELAY_BETWEEN_LOCK_PUBLISH_INFOS
    battery_scan_interval = DELAY_BETWEEN_LOCK_PUBLISH_INFOS*5
    loglevel = 'INFO'
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = 'u:p:i:s:m:o:U:P:l:S'
    long_options = ['tt_user=', 'tt_pass=','tt_id=','tt_secret=','mqtt_host=', 'mqtt_port=', 'mqtt_user=',
                    'mqtt_pass=', 'log_level=', 'scan=']
    try:
        arguments, values = getopt.getopt(
            argument_list, short_options, long_options)
    except getopt.error as e:
        raise ValueError('Invalid parameters!')

    for current_argument, current_value in arguments:
        if isEmptyStr(current_value):
            pass
        elif current_argument in ("-U", "--tt_user"):
            ttlock_user = current_value
        elif current_argument in ("-P", "--tt_pass"):
            ttlock_pass = current_value
        elif current_argument in ("-i", "--tt_id"):
            ttlock_client = current_value
        elif current_argument in ("-s", "--tt_secret"):
            ttlock_secret = current_value
        elif current_argument in ("-m", "--mqtt_host"):
            broker = current_value 
        elif current_argument in ("-o", "--mqtt_port"):
            port = int(current_value)
        elif current_argument in ("-u", "--mqtt_user"):
            broker_user = current_value
        elif current_argument in ("-p", "--mqtt_pass"):
            broker_pass = current_value
        elif current_argument in ("-l", "--log_level"):
            loglevel = current_value
        elif current_argument in ("-S", "--scan"):
            scan_interval = int(current_value)


    battery_scan_interval = scan_interval * 5

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logging.basicConfig(level=numeric_level, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] TTLock2MQTT: %(message)s', )

    logging.debug("Options: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
        ttlock_user, ttlock_pass, ttlock_client, ttlock_secret, broker, port, broker_user,loglevel, broker_pass,scan_interval,battery_scan_interval))
    ttlock_token = create_access_token(ttlock_user, ttlock_pass, ttlock_client, ttlock_secret)
    logging.debug("Access Token: {}".format(ttlock_token))
    
    main(broker, port, broker_user, broker_pass, ttlock_client, ttlock_token,scan_interval,battery_scan_interval)
