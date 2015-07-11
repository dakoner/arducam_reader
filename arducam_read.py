import time
import serial
import optparse
import logging
parser = optparse.OptionParser('arducam_read')
parser.add_option(
    '--device', type='string', default='/dev/ttyACM0',
    help='serial device to read from')
parser.add_option('--baudrate', type='int', default=921600, help='baud rate')
parser.add_option(
    '--rtscts', action='store_true', default=False, help='enable rtscts')
parser.add_option(
    '--dsrdtr', action='store_true', default=False, help='enable dsrdtr')
parser.add_option(
    '--xonxoff', action='store_true', default=False, help='enable xonxoff')

def main(opts):
    logging.basicConfig(level=logging.INFO)

    port = serial.Serial(
        opts.device, opts.baudrate,
        dsrdtr=opts.dsrdtr, rtscts=opts.rtscts,
        xonxoff=opts.xonxoff)
    f = open("test.jpg", "w")
    s = port.readline()
    print "ArduCAM Start!:", s
    assert(s.startswith('ArduCAM Start!'))
    s = port.readline()
    print "OV5642 detected.:", s
    assert(s.startswith("OV5642 detected."))
    time.sleep(0.2)
    port.write(chr(0x10))
    s = port.readline()
    print "s=", s
    s = port.readline()
    print "s=", s
    write = False
    last = None
    while(True):
        r = port.read(1)
        if last:
            if ord(r) == 0xd8 and ord(last) == 0xff:
                print "Saw header"
                f.write(last)
                write = True

            if write:
                f.write(r)
            if ord(r) == 0xd9 and ord(last) == 0xff:
                print "Saw footer"
                break
        last = r
    f.close()
        
if __name__ == '__main__':
  opts, args = parser.parse_args()
  main(opts)

