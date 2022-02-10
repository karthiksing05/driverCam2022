"""
STILL BROKEN; TRANSFER NOT READY YET...
need to fix the other side (java on roborio) to take the dataList
"""

import usb.core
import usb.util

import threading

import os

class ThreadedTransfer(object):

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x0424, idProduct=0xec00)

        self.sent = False

    def get_dev(self):

        if not self.dev:
            try:
                output = os.popen("lsusb -D /dev/bus/usb/001/005").read() # find the port that RoboRio is connected to
                # in most cases, the port will be the one above.

                idVendor = hex(int(output.split("idVendor")[1][:17].strip(), base=16))
                idProduct = hex(int(output.split("idProduct")[1][:17].strip(), base=16))

                self.dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)

                return True
            
            except Exception as e:
                print(f"Exception caused by: {e}")
                return False

        else:
            print(f"device already found, --> {self.dev}")

    def send(self, data) -> bool:
        tries = 0
        while tries < 5:
            tries += 1
            for config in self.dev:
                config.set()
                for intf in config:
                    for ep in intf:
                        if ep.bEndpointAddress:
                            self.dev.write(ep.bEndpointAddress, data, intf.bInterfaceNumber)
                            self.sent = True
                            break
            else:
                self.sent = False
                print(f"USB Not Found, trying again... ({tries} tries so far)")

        return self.sent

    def threadSend(self, data) -> bool:
        self.thread = threading.Thread(target=self.send, args=(data))
        self.thread.daemon = True
        self.thread.start()
        
        self.thread.join()
