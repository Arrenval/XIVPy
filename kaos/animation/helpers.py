from numpy        import single
from mathutils    import Matrix
from numpy.typing import NDArray 

import numpy as np


def dequantise_quaternions(quat_data: NDArray, bone_count: int, rot_indices: NDArray, bindings: NDArray) -> NDArray:
    quaternions = np.zeros((bone_count, quat_data.shape[1], 4))
    quaternions[:, :, 3] = 1.0

    x_indices = rot_indices      
    y_indices = rot_indices + 1  
    z_indices = rot_indices + 2  

    x_val = quat_data[x_indices, :]
    y_val = quat_data[y_indices, :]
    z_val = quat_data[z_indices, :]
    
    comp_idx = ((y_val >> 14) & 2) | ((x_val >> 15) & 1)
    sign_bit = (z_val >> 15) != 0
    
    MASK_15BIT = 0x7FFF  
    x_quant = x_val & MASK_15BIT
    y_quant = y_val & MASK_15BIT
    z_quant = z_val & MASK_15BIT

    MIDPOINT = 16383 
    x_signed = x_quant.astype(np.int32) - MIDPOINT
    y_signed = y_quant.astype(np.int32) - MIDPOINT
    z_signed = z_quant.astype(np.int32) - MIDPOINT

    FRACTAL = single(0.000043161)
    a = x_signed * FRACTAL
    b = y_signed * FRACTAL
    c = z_signed * FRACTAL

    d_squared = 1.0 - a*a - b*b - c*c
    d_squared = np.maximum(d_squared, 0.0)

    d = np.sqrt(d_squared)
    d = np.where(sign_bit, -d, d)
    
    for idx_value in range(4):
        mask = (comp_idx == idx_value)
        if not np.any(mask):
            continue  
        
        if idx_value == 0:  
            quaternions[bindings, :, 0][mask] = d[mask]
            quaternions[bindings, :, 1][mask] = a[mask]
            quaternions[bindings, :, 2][mask] = b[mask]
            quaternions[bindings, :, 3][mask] = c[mask]
        elif idx_value == 1:  
            quaternions[bindings, :, 0][mask] = a[mask]
            quaternions[bindings, :, 1][mask] = d[mask]
            quaternions[bindings, :, 2][mask] = b[mask]
            quaternions[bindings, :, 3][mask] = c[mask]
        elif idx_value == 2:  
            quaternions[bindings, :, 0][mask] = a[mask]
            quaternions[bindings, :, 1][mask] = b[mask]
            quaternions[bindings, :, 2][mask] = d[mask]
            quaternions[bindings, :, 3][mask] = c[mask]
        else: 
            quaternions[bindings, :, 0][mask] = a[mask]
            quaternions[bindings, :, 1][mask] = b[mask]
            quaternions[bindings, :, 2][mask] = c[mask]
            quaternions[bindings, :, 3][mask] = d[mask]
    
    w_negative  = quaternions[:, :, 3] < 0
    quaternions = np.where(w_negative[:, :, np.newaxis], -quaternions, quaternions)

    magnitudes = np.sqrt(np.sum(quaternions ** 2, axis=2))
    quaternions_normalized = quaternions / magnitudes[:, :, np.newaxis]

    return quaternions_normalized

def dequantise_scalars(scalars: NDArray, min: NDArray, span: NDArray) -> NDArray:
    normalised = scalars / single(65535)
    return min[:, None] + normalised * span[:, None]

def matrix_from_12floats(values) -> Matrix:
    return Matrix([
                    values[0:4],   
                    values[4:8],   
                    values[8:12],  
                    [0, 0, 0, 1]   
                ])