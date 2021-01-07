#!/usr/bin/python3

from pwn import *

INT_BITS = 32

def left_Circular_rotate(afterRotation,n):
    return (afterRotation<<n) | (afterRotation>>(INT_BITS-n))

finalCompareValue = 0x216e6957
subtractedVlue = 0x12d70fde

afterRotation = finalCompareValue + subtractedVlue
beforeRotation = left_Circular_rotate(afterRotation,int(0x10))
beforeRotation &= 0xffffffff    #only 32 bit is required therefore mask all the bits except last 32 bits

beforeRotation = p32(beforeRotation)
print(beforeRotation)

