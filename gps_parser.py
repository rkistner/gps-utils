import base64, struct, binascii

def angle(k):
    return 180.0/2147483647 * k
  
alts = []
f = open('gpsdata','r')
for line in map(lambda l: l.split(), f.readlines()):
  cmd = int(line[0], 16)
  data = binascii.unhexlify(line[1])
  #print hex(cmd), len(data), binascii.hexlify(data), data
  
  if cmd == 0x22:
    numbers = struct.unpack('<iiifii', data)
    
    lat, lon, alt = angle(numbers[0]), angle(numbers[1]), numbers[3]
    print "%.6f,%.6f,%.3f" % (lon, lat, alt)
  else:
    print "-----"

