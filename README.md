# FTMSRepeater
Server for receiving FTMS data and realying it as a BLE FTMS peripheral.
This server is originally intended to work with the Track My Indoor Workout FOSS application.
The application can be given a server address, in which case it'll connect that address and relays the FTMS data to it.
1. This way the workout can be picked up by multiple software even if your fitness machine is not capable of multiple BLE connections. (Most of the machines are not able to do that, enhanced ones like the Wahoo KICKR can handle multiple connections).
2. Another great use can be if an app does not support machines what TMIW supports, such as Kinomap does not support Precor Spinner Chrono Power or purely CSC sensor pair based DIY trainer setups (Kinomap seemed to only support power meter based setups for me).

The MVP (Minimum Viable Product) supports Linux right now, and requires some tech savvyness to set up. Here is how I use it:
1. I tether my phone to my laptop via USB.
2. I start the server code on my laptop (currently binds to localhost port 65432).
2. I port forward the 65432 port from my laptop to my phone where I run the Track My Indoor Workout via `adb` (Android Debugger). See https://android.stackexchange.com/questions/66564/port-forwarding-during-usb-tethering
3. I specify the localhost and that forwarded port endpoint as the server on my phone.
4. After that the workout should be relayed. The extra BLE peripheral will show up in the scans as named "Indoor Bike" and will have an 0x1826 FTMS service with a 0x2AD2 Inddor Bike characteristic which will stream the workout live.
