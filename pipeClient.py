import time
import struct

f = open(r'\\.\pipe\dataTransfer', 'r+b', 0)
i = 1

arr = [1.1, 2.2, 3.3, 4.4, 5.5]

while True:
    s = 'Message from client: {0}'.format(arr)
    i += 1
    
    f.write(struct.pack('I', len(s)))       
    f.write(s.encode('ascii'))             
    f.flush()                              

    n = struct.unpack('I', f.read(4))[0]   
    s = f.read(n).decode('ascii')           
    f.seek(0)                               
    print(s)
    
    for i in range(len(arr)):
        arr[i] += 1.0

    time.sleep(2)