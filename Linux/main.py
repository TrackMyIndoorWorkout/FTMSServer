import asyncio
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
from ftms import FTMSService
import socket

# https://realpython.com/python-sockets/
# 
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

async def main():
  # Alternativly you can request this bus directly from dbus_next.
  bus = await get_message_bus()

  service = FTMSService()
  await service.register(bus)

  # An agent is required to handle pairing 
  agent = NoIoAgent()
  # This script needs superuser for this to work.
  await agent.register(bus)

  adapter = await Adapter.get_first(bus)

  # Start an advert that will last for 3600 seconds.
  #
  # Full service UUID from a Schwinn IC4
  # 00001826-0000-1000-8000-00805f9b34fb
  #
  # Appearance: Category (bits 15 to 6) 0x012
  # Subcat
  # 0x00 0x0480 Generic Cycling
  # 0x01 0x0481 Cycling Computer
  # 0x02 0x0482 Speed Sensor
  # 0x03 0x0483 Cadence Sensor
  # 0x04 0x0484 Power Sensor
  # 0x05 0x0485 Speed and Cadence Sensor
  advert = Advertisement("Indoor Bike", ["1826"], 0x0480, 3600)
  await advert.register(bus, adapter)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f"Connected by {addr}")
      while True:
        data = conn.recv(20)
        if not data:
          break

        print(f"Recevied: {data}")
        service.update_measurement(data)
        await asyncio.sleep(0.1)

  await bus.wait_for_disconnect()

if __name__ == "__main__":
  asyncio.run(main())
