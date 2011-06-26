import binascii, time, datetime, exceptions

def sendhex(out, h):
    out.write(binascii.unhexlify(h.replace(' ','')))

def read(stream):
    data = ''
    while True:
        c = stream.read(1)
        if len(c) == 0:
            return None, None
        if ord(c) == 0x10:
            if len(data) == 0:
                continue
            d = stream.read(1)
            if ord(d) == 0x03:
                break
            elif ord(d) == 0x10:
                data += d
            else:
                raise exceptions.Exception("Invalid sequence: %d %d" % (ord(c), ord(d)))
        else:
            data += c
    print binascii.hexlify(data)
    cmd = ord(data[0])
    length = ord(data[1])
    cs = sum(map(ord, data)) & 0xff
    if cs != 0:
        raise exceptions.Exception("Checksum failed: %d" % (cs))
    data = data[2:-1]
    if len(data) != length:
        raise exceptions.Exception("Expected data of length %d but was %d" % (length, len(data)))
            
    return cmd, data

import serial, struct
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
fout = open("gpsdata","w")

sendhex(ser, "10 0A 02 06 00 EE 10 03")
cmd, data = read(ser)
print >> fout, hex(cmd), binascii.hexlify(data)

counter = 0
while(True):
    counter += 1
    sendhex(ser, "10 06 02 22 00 D6 10 03")
    cmd, data = read(ser)
    if data is None:
        break
    
    print >> fout, hex(cmd), binascii.hexlify(data)
    fout.flush()
    
ser.close()
