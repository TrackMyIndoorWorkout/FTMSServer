import asyncio
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
from ftms import FTMSService
from ftms_state import FTMSState
import socket

# https://realpython.com/python-sockets/
# 
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
# Description packet's format:
# Byte 0: version number
# Byte 1 & 2: 0x1826 (FTMS service UUID)
# Byte 3 & 4: 0x2AD1 or 0x2AD2 FTMS data characteristics
# Byte 5: following packet length
DESCRIPTOR_PACKET_LENGTH = 6

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
  advert = Advertisement("Fitness Machine", ["1826"], 0x0481, 3600)
  await advert.register(bus, adapter)

  packet_length = DESCRIPTOR_PACKET_LENGTH
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f"Connected by {addr}")
      while True:
        data = conn.recv(packet_length)
        if not data:
          service.state = FTMSState.WAITING_FOR_DESCRIPTOR
          packet_length = DESCRIPTOR_PACKET_LENGTH
          continue

        print(f"Recevied: {data.hex()}")
        if service.state == FTMSState.WAITING_FOR_DESCRIPTOR:
          if data[1] != 0x18 or data[2] != 0x26:
            print(f"Wrong FTMS service UUID: not 0x1826")
            break

          if data[3] != 0x2A:
            print(f"Wrong FTMS characteristic UUID: does not start with 0x2A")
            break

          if data[4] != 0xD1 and data[4] != 0xD2:
            print(f"Unsupported machine: currently 0x2AD1 Rower or 0x2AD2 Indoor Bike")
            break
          else:
            packet_length = data[5]
            if data[4] == 0xD1:
              service.state = FTMSState.PADDLING
            else: # data[4] == 0xD2:
              service.state = FTMSState.RIDING
        else:
          service.update_measurement(data)
          await asyncio.sleep(0.1) # safety sleep

  await bus.wait_for_disconnect()

if __name__ == "__main__":
  asyncio.run(main())
