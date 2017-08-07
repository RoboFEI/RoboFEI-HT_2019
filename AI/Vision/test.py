import sys
import time

a = 0
for x in range (0,3):
    a = a + 1
    b = ("Loading" + "." * a)
    # \r prints a carriage return first, so `b` is printed on top of the previous line.
    sys.stdout.write('\r'+b)
    raw_input()
    time.sleep(1)
    raw_input()
    sys.stdout.flush()
    raw_input()
print (a)
