from transformers.constants import asconstants

import sys

z = [1, 2, 3]
class A(object):
    def a(s):
        return len(z)

def de():
    print sys.argv



b = asconstants(a=A(), z=z)(lambda: a.a())

z = [1,3]
import dis
print "Natural:"
# dis.dis(a)
print "\nTransformed:"
dis.dis(de)

print  b()
# prints: 2, 3