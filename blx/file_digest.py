from __future__ import annotations

import hashlib
import os
from io import BufferedReader
from pathlib import Path
from typing import Optional
from blx.cid import CID

from blx.filepath import FilePath

BUFSIZE = 4 * 1024 * 1024

__all__ = ["FileDigest", "FileChunk"]


class FileDigest:
    def __init__(self, filepath: FilePath):
        self._filepath = Path(filepath)
        size = os.path.getsize(self._filepath)
        self._nchunks = size // BUFSIZE + int(size % BUFSIZE != 0)
        self._file: Optional[BufferedReader] = None
        self._hash = hashlib.sha256()

    def open(self):
        self._file = open(self._filepath, "rb")

    def close(self):
        assert self._file
        self._file.close()

    @property
    def cid(self):
        return CID(sha256hex=self._hash.hexdigest())

    def __len__(self):
        return self._nchunks

    def __iter__(self):
        return self

    def __next__(self):
        assert self._file
        if chunk := self._file.read(BUFSIZE):
            return FileChunk(self._hash, chunk)
        raise StopIteration()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *_):
        self.close()


class FileChunk:
    def __init__(self, hash, chunk):
        self._hash = hash
        self._chunk = chunk

    def update(self):
        self._hash.update(self._chunk)
