import bitcoin
import os
import re
import struct


class BlockChain(object):
    """Loader of blocks from .blk files on disk."""

    def __init__(self, blocks_dir):
        """

        Args:
            blocks_dir: path to directory containing blk*.dat files
        """
        self.dir = blocks_dir

    def get_files(self):
        """Finds all of .blk files, sorted."""
        files = os.listdir(self.dir)
        files = [f for f in files if f.startswith("blk") and f.endswith(".dat")]
        files = map(lambda x: os.path.join(self.dir, x), files)
        return sorted(files)

    def get_block_at_pos(self, nFile, nPos):
        """Reads a block from file.

        Args:
            nFile: int, number of .blk file
            nPos: int, offset of the block in file

        Returns: CBlock
        """
        path = self.dir + '/blk%05d.dat' % nFile
        f = open(path, 'rb')
        f.seek(nPos)
        return bitcoin.core.CBlock.stream_deserialize(f)

    @staticmethod
    def read_blocks_from_file(f):
        """Yields blocks from bitcoin core blk file.

        Params:
            f: File

        Yields: (pos-in-file, CBlock)
        """
        while True:
            # Skip empty space until a block magic is found.
            # Most of the time, each block immediately follows the previous one. Sometimes,
            # however, there can be a gap, probably when bitcoind crashes.
            magic = None
            while magic is None or magic == b'\x00\x00\x00\x00':
                magic = f.read(4)
                if magic == b"":  # nothing read, end of file
                    return

            assert magic == bitcoin.params.MESSAGE_START, 'expected=%x, got=%x' % (
                int.from_bytes(bitcoin.params.MESSAGE_START, 'big'), int.from_bytes(magic, 'big'))
            size, = struct.unpack("<I", f.read(4))

            pos = f.tell()
            b = bitcoin.core.CBlock.stream_deserialize(f)
            yield pos, b

    def read_all_blocks(self):
        """Read all block contained in Blockchain.

        Yields: (nFile, nPos, CBlock)
          - nFile is number of .blk file
          - nPos is offset of the block within the file
        """
        for path in self.get_files():
            filename = os.path.basename(path)
            m = re.match('blk(\d+)\.dat', filename)
            nFile = int(m.group(1))
            for nPos, block in self.read_blocks_from_file(open(path, 'rb')):
                yield nFile, nPos, block
