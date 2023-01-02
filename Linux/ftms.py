from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from ftms_state import FTMSState

import struct

class FTMSService(Service):
  state = FTMSState.WAITING_FOR_DESCRIPTOR

  def __init__(self):
    # Base 16 service UUID, This should be a primary service.
    super().__init__("1826", True)
    self.state = FTMSState.WAITING_FOR_DESCRIPTOR

  @characteristic("2AD2", CharFlags.NOTIFY)
  def ride_measurement(self, options):
    # This function is called when the characteristic is read.
    # Since this characteristic is notify only this function is a placeholder.
    # You don't need this function Python 3.9+ (See PEP 614).
    # You can generally ignore the options argument 
    # (see Advanced Characteristics and Descriptors Documentation).
    pass

  @characteristic("2AD1", CharFlags.NOTIFY)
  def paddle_measurement(self, options):
    # This function is called when the characteristic is read.
    # Since this characteristic is notify only this function is a placeholder.
    # You don't need this function Python 3.9+ (See PEP 614).
    # You can generally ignore the options argument 
    # (see Advanced Characteristics and Descriptors Documentation).
    pass

  def update_measurement(self, measurement):
    # Call this when you get a new Inddor Bike data reading.
    # Note that notification is asynchronous (you must await something at some point after calling this).

    # Bluetooth data is little endian.
    # Currently the data contains FTMS data format including the flags
    serialized = struct.pack("<" + "B" * len(measurement), *measurement)
    if self.state == FTMSState.RIDING:
      self.ride_measurement.changed(serialized)
    elif self.state == FTMSState.PADDLING:
      self.paddle_measurement.changed(serialized)
