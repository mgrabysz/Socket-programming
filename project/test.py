import socket
import sys
import threading
import time
import unittest

sys.path.append('../gateway')
import gateway.registration as registration
import client.messages as messages
import gateway.gateway as gtw


class TestRegistration(unittest.TestCase):

    def test_unregister_no_such_device(self):
        self.assertFalse(registration._unregister(1))

    def test_unregister(self):
        registration.get_registered_devices()[1] = ("127.0.0.1", 2140)
        registration._unregister(1)
        self.assertFalse(1 in registration.get_registered_devices().keys())

    def test_register(self):
        registration._register(("127.0.0.1", 2137), 4)
        self.assertTrue(4 in registration.get_registered_devices().keys())
        self.assertEqual(registration.get_registered_devices()[4][0], "127.0.0.1")
        self.assertEqual(registration.get_registered_devices()[4][1], 2137)

    def test_register_already_exists(self):
        registration._registered_devices[1] = ("127.0.0.1", 2140)
        self.assertFalse(registration._register(("127.0.0.1", 2140), 5))
        self.assertFalse(registration._register(("127.0.0.1", 2141), 1))

    def test_handle_message_register(self):
        message = messages.RegisterMessage(1, 1673876709.461439).__dict__
        address = ("127.0.0.1", 2140)
        registration.handle_message(address, message)
        self.assertEqual(registration.get_registered_devices()[1][0], "127.0.0.1")
        self.assertEqual(registration.get_registered_devices()[1][1], 2140)

    def test_handle_message_unregister(self):
        registration.get_registered_devices()[1] = ("127.0.0.1", 2140)
        message = messages.UnregisterMessage(1).__dict__
        address = ("127.0.0.1", 2140)
        registration.handle_message(address, message)
        self.assertFalse(1 in registration.get_registered_devices().keys())


# class TestGateway(unittest.TestCase):
#
#     def test_gateway(self):
#         test_gateway = gtw.Gateway(
#             port=gtw.DEFAULT_GATEWAY_PORT,
#             servers=gtw.DEFAULT_SERVERS,
#             interval=gtw.DEFAULT_INTERVAL,
#             sync_interval=gtw.DEFAULT_SYNC_INTERVAL,
#             private_key=gtw.DEFAULT_PRIVATE_KEY_PATH,
#             public_key=gtw.DEFAULT_PUBLIC_KEY_PATH,
#             key_password=gtw.DEFAULT_KEY_PASSWORD,
#             is_verbose=False
#         )
#         gateway_thread = threading.Thread(target=test_gateway.start())
#         gateway_thread.start()
#         time.sleep(0.000001)
#
#         mock_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#         register_message = messages.RegisterMessage(1, 1673876709.461439)
#         msg_bytes = register_message.to_json().encode()
#         mock_client.sendto(msg_bytes, ("127.0.0.1", gtw.DEFAULT_GATEWAY_PORT))



if __name__ == '__main__':
    unittest.main()
