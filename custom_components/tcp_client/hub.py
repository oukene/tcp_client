import asyncio
import logging
import threading
import time
import socket

from .const import *

_LOGGER = logging.getLogger(__name__)
                
class Hub:
    """Dummy hub for Hello World example."""
    manufacturer = DOMAIN
    
    def __init__(self, hass, host, port):
        """Init dummy hub."""
        _LOGGER.debug("init hub")
        self.hass = hass
        self._host = host
        self._port = port
        self._entities = {}
        self._socket = None
        self._connected = False
        self._recv_thread = None
        self._unload = False
        _LOGGER.debug("start server!!!")
        self._recv_thread = threading.Thread(target=self.start_server)
        self._recv_thread.daemon = True
        self._recv_thread.start()

    def add_entity(self, entity):
        self._entities[entity.entity_id] = entity

    def close(self):
        self.set_entity_state(False)
        self._connected = False
        if self._socket != None:
            try:
                _LOGGER.debug("socket close")
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
            except Exception as e:
                _LOGGER.error("exception : " + e)
            
        self._socket = None

    def isConnected(self):
        return self._connected

    def set_entity_state(self, state):
        for id, e in self._entities.items():
            e.set_available(state)

    def connect(self):
        self.close()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(True)

        while True:
            try:
                _LOGGER.debug(f"try connect - IP : {self._host}, port : {self._port}")
                self._socket.connect((self._host, self._port))
                _LOGGER.debug("연결 성공")
                self._connected = True
                self.set_entity_state(True)
                break
            except:
                _LOGGER.error("연결 실패, 재연결 시도")
                time.sleep(10)
                self.set_entity_state(False)
                self._connected = False
                continue
        
    def start_server(self):
        #str = "02 10 02 02 09 03 02 02 09 03 10 00 00 00 40 03"
        #num = bytearray.fromhex(str)
        #_LOGGER.debug(f"hex data test : {num}")
        self.connect()

        while True:
            if self._recv_thread == None:
                return
            try:
                data = self._socket.recv(1024)
                if self._unload == True:
                    return
                _LOGGER.debug(f"recv data : {data}")
                if data == b'':
                    self.connect()
                    continue
                if not data:
                    self.connect()
                    continue

                for id, e in self._entities.items():
                    e.on_recv_data(data)
            except socket.timeout:
                self.connect()
                continue
            #except socket.timeout:
            #    self.connect()
            #except Exception as e:
            #    _LOGGER.error("error exception : " + str(e))
            #    self.connect()
            #    continue

    def send_packet(self, data):
        try:
            if self._socket != None:
                for d in data:
                    self._socket.send(bytes.fromhex(d))
            else:
                # 재연결 후 다시 보냄
                self.connect()
                for d in data:
                    self._socket.send(bytes.fromhex(d))
        except:
            # 재연결 후 다시 보냄
            _LOGGER.error("send_packet, 소켓이 연결되지 않음, 재접속 후 전송 시도")
            self.connect()
            for d in data:
                self._socket.send(bytes.fromhex(d))

    @property
    def hub_id(self):
        """ID for dummy hub."""
        return self._id

    async def test_connection(self):
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True
