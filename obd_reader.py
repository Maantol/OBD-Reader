import obd
import sys
import time

obd.logger.setLevel(obd.logging.DEBUG)

#Currently working on macOS environment. Bluetooth COM port hard coded for macOS. Otherwise switching to auto-connect mode which tries to go USB mode.
def connect_to_obd():
    print("Attempting to connect to OBD2 adapter via USB")
    
    usb_connection = obd.OBD()
    
    if usb_connection.is_connected():
        print("USB connection successful")
        return usb_connection
    
    #bluetooth_connection = obd.OBD("/dev/tty.Bluetooth-Incoming-Port")
    # if bluetooth_connection.is_connected():
    #     print("Default macOS Bluetooth connection successful")
    #     return bluetooth_connection
   
#If connection is successful, the function reads RPM data from the OBD2 adapter. This is the basic setting to get if everything is working.
def read_rpm(obd_connection):
    print("Trying to retrieve RPM data...")
    try:
        while True:
            rpm_response = obd_connection.query(obd.commands['RPM'])
            if rpm_response.value is not None:
                print(f"RPM: {rpm_response.value}")
            else:
                print("No data received")
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nExiting program. Connection closed.")


def main():
    obd_connection = connect_to_obd()

    if obd_connection is not None:
        print("Connection successful")
        read_rpm(obd_connection)
    else:
        sys.exit("Unable to connect to OBD2 adapter. Exiting program.")


if __name__ == "__main__":
    main()