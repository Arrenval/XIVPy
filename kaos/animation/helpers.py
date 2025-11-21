from math      import sqrt
from mathutils import Quaternion, Matrix

from ...utils  import BinaryReader
import numpy as np

def read_quantised_quaternion(reader: BinaryReader) -> Quaternion:
    return dequantise_quaternion(reader.read_bytes(6))

def read_quantised_scalar(reader: BinaryReader, min: float, span: float) -> float:
    return dequantise_scalar(reader.read_uint16(), min, span)

# Smallest Tree: https://gafferongames.com/post/snapshot_compression/
def dequantise_quaternion(data: bytes) -> Quaternion:
    packed = int.from_bytes(data, byteorder='little')
    component_index = packed & 0x03              
    val_a = (packed >> 2) & 0x7FFF               
    val_b = (packed >> 17) & 0x7FFF              
    val_c = (packed >> 32) & 0x7FFF

    RANGE   = 0.7071067811865475
    MAX_VAL = 0x7FFF
    
    # Convert from unsigned to signed range
    a = ((val_a - MAX_VAL) / MAX_VAL) * RANGE
    b = ((val_b - MAX_VAL) / MAX_VAL) * RANGE
    c = ((val_c - MAX_VAL) / MAX_VAL) * RANGE
    
    d = sqrt(max(0.0, 1.0 - a*a - b*b - c*c))
    
    if component_index == 0:  
        quat = Quaternion([c, d, a, b]) 
    elif component_index == 1: 
        quat = Quaternion([c, a, d, b])  
    elif component_index == 2:  
        quat = Quaternion([c, a, b, d]) 
    else:                      
        quat = Quaternion([d, a, b, c])  
    
    if quat.w < 0: quat.negate()
    
    quat.normalize()
    return quat

def dequantise_scalar(scalar: int, min: float, span: float) -> float:
    normalised = scalar / 65535
    return min + normalised * span

def matrix_from_12floats(values) -> Matrix:
    return Matrix([
                    values[0:4],   
                    values[4:8],   
                    values[8:12],  
                    [0, 0, 0, 1]   
                ])