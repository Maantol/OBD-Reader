import obd
import sys
import time
import configparser

obd.logger.setLevel(obd.logging.DEBUG)

#This function tries to connect to the OBD2 adapter via USB. If the connection is successful, the function returns the connection object.
def connect_to_obd(port):
    print(f"Attempting to connect to OBD2 adapter on {port}")

    usb_connection = obd.OBD(port)
    
    if usb_connection.is_connected():
        print("USB connection successful")
        return usb_connection
    
    #Currently working on macOS environment. Bluetooth COM port hard coded for macOS. Otherwise switching to auto-connect mode which tries to go USB mode.
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
                print(f"RPM: {rpm_response.value}, flush=True", end="")
                time.sleep(1)
            else:
                print("No data received")
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nExiting program. Connection closed.")


def main():
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    port = config['device']['port']
    
    obd_connection = connect_to_obd(port)
    
    
    if obd_connection is not None:
        print("Connection successful")
        read_rpm(obd_connection)
    else:
        sys.exit("Unable to connect to OBD2 adapter. Exiting program.")


if __name__ == "__main__":
    main()