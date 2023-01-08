# FTMSRepeater
Server for receiving FTMS data and realying it as a BLE FTMS peripheral.
This server is originally intended to work with the Track My Indoor Workout FOSS (Free and Open Source) application.
The application can be given a server address, in which case it'll connect to that address and relay the FTMS data to it.
1. This way the workout can be picked up by multiple software even if your fitness machine is not capable of multiple BLE connections. (Most of the machines are not able to do that, enhanced ones like the Wahoo KICKR can handle multiple connections).
2. Another great use can be if an app does not support machines what TMIW (Track My Indoor Workout) supports, such as Kinomap does not support Precor Spinner Chrono Power or purely CSC sensor pair based DIY trainer setups (Kinomap seemed to only support power meter based setups for me).

The MVP (Minimum Viable Product) supports Linux right now, and requires some tech savviness to set up. Here is how I use it:
1. I tether my phone to my laptop via USB.
2. I start the server code on my laptop (currently binds to localhost port 65432).
3. I port forward the 65432 port from my laptop to my phone where I run the Track My Indoor Workout via `adb reverse tcp:65432 tcp:65432` (Android Debugger). This way the phone's localhost 65432 port will be forwarded to the laptop's 65432. See https://android.stackexchange.com/questions/66564/port-forwarding-during-usb-tethering
4. I specify `127.0.0.1:65432` TCP endpoint as the server on my phone (which is actually the forwarded server from my laptop).
5. After that the workout should be relayed. The extra BLE peripheral will show up in the BLE scans as device named "Indoor Bike" and will have an 0x1826 FTMS service with a 0x2AD2 Indoor Bike characteristic which will stream the workout live.

## Descriptor format for client applications
The FTMS packet stream is preceded by a 6 byte sequence so the server can set up for the upcoming FTMS format stream.
1. Version number
2. 0x18 (first byte of FTMS service UUID)
3. 0x26 (second byte of FTMS service UUID)
4. 0x2A (first byte of FTMS data characteristic UUID)
5. 0x?? (second byte of FTMS data characteristic UUID)
6. Fixed byte length of the upcoming FTMS service
