from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags

import struct

class FTMSService(Service):
  def __init__(self):
    # Base 16 service UUID, This should be a primary service.
    super().__init__("1826", True)

  @characteristic("2AD2", CharFlags.NOTIFY)
  def measurement(self, options):
    # This function is called when the characteristic is read.
    # Since this characteristic is notify only this function is a placeholder.
    # You don't need this function Python 3.9+ (See PEP 614).
    # You can generally ignore the options argument 
    # (see Advanced Characteristics and Descriptors Documentation).
    pass

  def update_measurement(self, measurement):
    # Call this when you get a new heartrate reading.
    # Note that notification is asynchronous (you must await something at some point after calling this).
    # flags = [84, 11]

    # Bluetooth data is little endian.
    serialized = struct.pack("<" + "B" * len(measurement), *measurement)
    self.measurement.changed(serialized)
