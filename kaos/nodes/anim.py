from typing import TYPE_CHECKING, Literal, overload

if TYPE_CHECKING:
    from .core import Node, hkReferencedObjectNode


    class hkaAnimationContainerNode(hkReferencedObjectNode):

        @overload
        def __getitem__(self, key: Literal["skeletons"]) -> list[int]: ...  # hkaSkeleton
        @overload
        def __getitem__(self, key: Literal["animations"]) -> list[int]: ...  # hkaAnimation
        @overload
        def __getitem__(self, key: Literal["bindings"]) -> list[int]: ...  # hkaAnimationBinding
        @overload
        def __getitem__(self, key: Literal["attachments"]) -> list[int]: ...  # hkaBoneAttachment
        @overload
        def __getitem__(self, key: Literal["skins"]) -> list[int]: ...  # hkaMeshBinding

        @overload
        def __setitem__(self, key: Literal["skeletons"], value: list[int]) -> None: ...  # hkaSkeleton
        @overload
        def __setitem__(self, key: Literal["animations"], value: list[int]) -> None: ...  # hkaAnimation
        @overload
        def __setitem__(self, key: Literal["bindings"], value: list[int]) -> None: ...  # hkaAnimationBinding
        @overload
        def __setitem__(self, key: Literal["attachments"], value: list[int]) -> None: ...  # hkaBoneAttachment
        @overload
        def __setitem__(self, key: Literal["skins"], value: list[int]) -> None: ...  # hkaMeshBinding

    class hkaBoneNode(Node):

        @overload
        def __getitem__(self, key: Literal["name"]) -> str: ...
        @overload
        def __getitem__(self, key: Literal["lockTranslation"]) -> int: ...

        @overload
        def __setitem__(self, key: Literal["name"], value: str) -> None: ...
        @overload
        def __setitem__(self, key: Literal["lockTranslation"], value: int) -> None: ...

    class hkaSkeletonNode(hkReferencedObjectNode):

        @overload
        def __getitem__(self, key: Literal["name"]) -> str: ...
        @overload
        def __getitem__(self, key: Literal["parentIndices"]) -> list[int]: ...
        @overload
        def __getitem__(self, key: Literal["bones"]) -> list[int]: ...  # hkaBone
        @overload
        def __getitem__(self, key: Literal["referencePose"]) -> list[list[float]]: ...
        @overload
        def __getitem__(self, key: Literal["referenceFloats"]) -> list[float]: ...
        @overload
        def __getitem__(self, key: Literal["floatSlots"]) -> list[str]: ...
        @overload
        def __getitem__(self, key: Literal["localFrames"]) -> list[int]: ...  # hkaSkeletonLocalFrameOnBone

        @overload
        def __setitem__(self, key: Literal["name"], value: str) -> None: ...
        @overload
        def __setitem__(self, key: Literal["parentIndices"], value: list[int]) -> None: ...
        @overload
        def __setitem__(self, key: Literal["bones"], value: list[int]) -> None: ...  # hkaBone
        @overload
        def __setitem__(self, key: Literal["referencePose"], value: list[list[float]]) -> None: ...
        @overload
        def __setitem__(self, key: Literal["referenceFloats"], value: list[float]) -> None: ...
        @overload
        def __setitem__(self, key: Literal["floatSlots"], value: list[str]) -> None: ...
        @overload
        def __setitem__(self, key: Literal["localFrames"], value: list[int]) -> None: ...  # hkaSkeletonLocalFrameOnBone

    class hkaSkeletonMapperNode(hkReferencedObjectNode):

        @overload
        def __getitem__(self, key: Literal["mapping"]) -> int:...  # hkaSkeletonMapperData

        @overload
        def __setitem__(self, key: Literal["mapping"], value: int) -> None:...  # hkaSkeletonMapperData

    class hkaSkeletonMapperDataNode(Node):

        @overload
        def __getitem__(self, key: Literal["skeletonA"]) -> int:...  # hkaSkeleton
        @overload
        def __getitem__(self, key: Literal["skeletonB"]) -> int:...  # hkaSkeleton
        @overload
        def __getitem__(self, key: Literal["simpleMappings"]) -> list[int]:...  # hkaSkeletonMapperDataSimpleMapping
        @overload
        def __getitem__(self, key: Literal["chainMappings"]) -> list[int]:...  # hkaSkeletonMapperDataChainMapping
        @overload
        def __getitem__(self, key: Literal["unmappedBones"]) -> list[int]:...
        @overload
        def __getitem__(self, key: Literal["extractedMotionMapping"]) -> list[float]:...
        @overload
        def __getitem__(self, key: Literal["keepUnmappedLocal"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["mappingType"]) -> int:...

        @overload
        def __setitem__(self, key: Literal["skeletonA"], value: int) -> None:...  # hkaSkeleton
        @overload
        def __setitem__(self, key: Literal["skeletonB"], value: int) -> None:...  # hkaSkeleton
        @overload
        def __setitem__(self, key: Literal["simpleMappings"], value: list[int]) -> None:...  # hkaSkeletonMapperDataSimpleMapping
        @overload
        def __setitem__(self, key: Literal["chainMappings"], value: list[int]) -> None:...  # hkaSkeletonMapperDataChainMapping
        @overload
        def __setitem__(self, key: Literal["unmappedBones"], value: list[int]) -> None:...
        @overload
        def __setitem__(self, key: Literal["extractedMotionMapping"], value: list[float]) -> None:...
        @overload
        def __setitem__(self, key: Literal["keepUnmappedLocal"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["mappingType"], value: int) -> None:...

    class hkaSkeletonMapperDataChainMappingNode(Node):

        @overload
        def __getitem__(self, key: Literal["startBoneA"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["endBoneA"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["startBoneB"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["endBoneB"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["startAFromBTransform"]) -> list[float]:...
        @overload
        def __getitem__(self, key: Literal["endAFromBTransform"]) -> list[float]:...

        @overload
        def __setitem__(self, key: Literal["startBoneA"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["endBoneA"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["startBoneB"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["endBoneB"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["startAFromBTransform"], value: list[float]) -> None:...
        @overload
        def __setitem__(self, key: Literal["endAFromBTransform"], value: list[float]) -> None:...

    class hkaSkeletonMapperDataSimpleMappingNode(Node):

        @overload
        def __getitem__(self, key: Literal["boneA"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["boneB"]) -> int:...
        @overload
        def __getitem__(self, key: Literal["aFromBTransform"]) -> list[float]:...

        @overload
        def __setitem__(self, key: Literal["boneA"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["boneB"], value: int) -> None:...
        @overload
        def __setitem__(self, key: Literal["aFromBTransform"], value: list[float]) -> None:...
