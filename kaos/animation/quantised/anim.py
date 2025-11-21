import numpy as np

from numpy        import ushort, single
from mathutils    import Quaternion, Matrix
from dataclasses  import dataclass
from numpy.typing import NDArray

from .header      import AnimHeader
from ..helpers    import read_quantised_quaternion, read_quantised_scalar, matrix_from_12floats
from .sections    import Elements, StaticValues, DynamicRanges
from ....utils    import BinaryReader


@dataclass
class QuantisedFrame:
    translations: NDArray | None = None
    rotations   : NDArray | None = None
    scale       : NDArray | None = None
    floats      : NDArray | None = None

    # We don't use a class method because we initialise it manually to pass in the lists with static values beforehand
    def from_bytes(self, data: bytes, dynamic_elements: Elements, range_min: DynamicRanges, range_span: DynamicRanges) -> 'QuantisedFrame':
        reader = BinaryReader(data)

        #Now we read the actual frame data
        for idx, bone_element in enumerate(dynamic_elements.translations):
            self.translations[bone_element] = read_quantised_scalar(reader, range_min.translations[idx], range_span.translations[idx])

        for idx, bone_element in enumerate(dynamic_elements.rotations):
            end = bone_element + 3
            self.rotations[bone_element: end] = [reader.read_int16() for _ in range(3)]

        for idx, bone_element in enumerate(dynamic_elements.scale):
            self.scale[bone_element] = read_quantised_scalar(reader, range_min.scale[idx], range_span.scale[idx])

        for idx, bone_element in enumerate(dynamic_elements.floats):
            self.floats[bone_element] = read_quantised_scalar(reader, range_min.floats[idx], range_span.floats[idx])

        self.rotations = self.get_quaternions()

        return self
    
    def get_quaternions(self) -> list[Quaternion]:
        reader = BinaryReader(self.rotations.tobytes()[1:])
        count  = len(self.rotations) // 3
        return [read_quantised_quaternion(reader) for _ in range(count)]
    
    def get_translations(self) -> list[Matrix]:
        count  = len(self.translations) // 12
        return [matrix_from_12floats(self.translations[idx * 12: idx * 12 + 12]) for idx in range(count)]

class QuantisedAnimation:

    def __init__(self) -> None:
        # All ints in this format are ushorts
        self.header      = AnimHeader()
        self.tracks: int = 0

        self.static_elements  = Elements()
        self.dynamic_elements = Elements()

        self.static_values = Elements()
        self.range_min     = Elements()
        self.range_span    = Elements()

        self.frames: list[QuantisedFrame] = []
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'QuantisedAnimation':
        anim   = cls()
        reader = BinaryReader(data)

        pre_frame_size = reader.read_uint16()
        anim.header    = AnimHeader.from_bytes(reader)
        header         = anim.header

        reader.pos = header.static_element_offset
        anim.static_elements = Elements.from_bytes(reader, header.static_trs, header.static_rot, header.static_scl, header.static_floats)

        reader.pos = header.dynamic_element_offset
        anim.dynamic_elements = Elements.from_bytes(reader, header.dynamic_trs, header.dynamic_rot, header.dynamic_scl, header.dynamic_floats)

        reader.pos = header.static_values_offset
        anim.static_values = StaticValues.from_bytes(reader, header.static_trs, header.static_rot, header.static_scl, header.static_floats)

        reader.pos = header.dynamic_range_min_offset
        anim.range_min = DynamicRanges.from_bytes(reader, header.dynamic_trs, header.dynamic_scl, header.dynamic_floats)

        reader.pos = header.dynamic_range_span_offset
        anim.range_span = DynamicRanges.from_bytes(reader, header.dynamic_trs, header.dynamic_scl, header.dynamic_floats)
        
        #Inputting the static values into the pose arrays
        trs, rot, scl, floats = anim.create_pose_arrays()

        reader.pos   = pre_frame_size
        frame_offset = pre_frame_size
        for _ in range(header.frame_count):
            frame = QuantisedFrame(
                        translations=trs.copy(), 
                        rotations=rot.copy(), 
                        scale=scl.copy(), 
                        floats=floats.copy()
                    )
            
            frame_data = reader.data[frame_offset: frame_offset + header.frame_size]
            anim.frames.append(frame.from_bytes(frame_data, anim.dynamic_elements, anim.range_min, anim.range_span))
            frame_offset += header.frame_size
    
    def create_pose_arrays(self, bone_count: int | None=None) -> tuple[NDArray, ...]:

        def get_max_index(static_arr: NDArray, dynamic_arr: NDArray) -> int:
            indices = []
            if len(static_arr) > 0:
                indices.append(static_arr.max())
            if len(dynamic_arr) > 0:
                indices.append(dynamic_arr.max())
            return max(indices) if indices else -1

        if bone_count is None:
            bone_count = self.header.bone_count

        trs_len   = get_max_index(self.static_elements.translations, self.dynamic_elements.translations) + 1
        rot_len   = get_max_index(self.static_elements.rotations, self.dynamic_elements.rotations) + 1
        scl_len   = get_max_index(self.static_elements.scale, self.dynamic_elements.scale) + 1
        float_len = get_max_index(self.static_elements.floats, self.dynamic_elements.floats) + 1

        translations = np.zeros(trs_len, single)
        rotations    = np.zeros(rot_len + 2 if rot_len > 0 else 0, ushort)
        scale        = np.zeros(scl_len, single)
        floats       = np.zeros(float_len, single)

        for idx, bone_element in enumerate(self.static_elements.translations):
            translations[bone_element] = self.static_values.translations[idx]

        for idx, bone_element in enumerate(self.static_elements.rotations):
            end = bone_element + 3
            rotations[bone_element: end] = self.static_values.rotations[idx: idx + 3]

        for idx, bone_element in enumerate(self.static_elements.scale):
            scale[bone_element] = self.static_values.scale[idx]

        for idx, bone_element in enumerate(self.static_elements.floats):
            floats[bone_element] = self.static_values.floats[idx]

        return translations, rotations, scale, floats
