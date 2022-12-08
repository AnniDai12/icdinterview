import time
import struct


# implement a "named pipe" for exchanging double arrays between a C# and a Python process.
pipeName = "dataTransferred.dat"
import win32pipe, win32file


class PipeServer():
        def __init__(self, pipeName):
                self.pipe = win32pipe.CreateNamedPipe(
                        r'\\.\pipe\\' + pipeName,
                        win32pipe.PIPE_ACCESS_OUTBOUND,
                        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                        1, 65536, 65536,
                        0,
                        None)

        # blocks until a connection is established
        def connect(self):
                win32pipe.ConnectNamedPipe(self.pipe, None)



        # Message without tailing '\n'
        def write(self, message):
                try:
                        win32file.WriteFile(self.pipe, message.encode() + b'\n')
                except:
                        print("Error while writing to pipe, closing pipe")

        # send a double array to the C# process
        def sendDoubleArray(self, doubleArray):
                # send the size of the array
                self.write(str(len(doubleArray)))

                # send the array
                for i in range(len(doubleArray)):
                        self.write(str(doubleArray[i]))

                # send the end of the array
                self.write("end")


        def close(self):
                win32file.CloseHandle(self.pipe)


t = PipeServer("CSServer")

t.connect()

# declare a double array to send to the C# process
doubleArray = [1.1, 2.2, 3.3, 4.4, 5.5]

# keep the server alive forever
while True:
        # send the double array to the C# process
        t.sendDoubleArray(doubleArray)

        print(f"Python keeps sending the double array to the C# process, as follows: {doubleArray}")

        # wait for 1 second
        time.sleep(1)

        # check if the C# process is still alive
        if not t.pipe:
                break

        # check if pipe is closed from C# side
        try:
            win32file.ReadFile(t.pipe)
        except:
            break

t.write("Closing now")
t.close()