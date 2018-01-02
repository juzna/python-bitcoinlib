
from .serialize import *

class CDiskTxPos(ImmutableSerializable):
    """Location of transaction on disk, used in Chainstate DB."""

    __slots__ = ['nFile', 'nPos', 'nTxOffset']

    def __init__(self, nFile=-1, nPos=0, nTxOffset=0):
        object.__setattr__(self, 'nFile', nFile)
        object.__setattr__(self, 'nPos', nPos)
        object.__setattr__(self, 'nTxOffset', nTxOffset)

    @classmethod
    def stream_deserialize(cls, f):
        nFile = VarIntSerializer.stream_deserialize(f)
        nPos = VarIntSerializer.stream_deserialize(f)
        nTxOffset = VarIntSerializer.stream_deserialize(f)
        return cls(nFile, nPos, nTxOffset)

    def stream_serialize(self, f):
        VarIntSerializer.stream_serialize(self.nFile, f)
        VarIntSerializer.stream_serialize(self.nPos, f)
        VarIntSerializer.stream_serialize(self.nTxOffset, f)

    def __repr__(self):
        return "CDiskTxPos(%d, %d, %d)" % (self.nFile, self.nPos, self.nTxOffset)
