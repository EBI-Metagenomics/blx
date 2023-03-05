from functools import lru_cache
from pathlib import Path

from minio import Minio
from minio.error import S3Error

from blx.cid import CID
from blx.env import env
from blx.filepath import FilePath

__all__ = ["BLXApp"]


class BLXApp:
    def __init__(self):
        self._minio = get_minio()

    def has(self, cid: CID):
        try:
            self._minio.stat_object(env.BLX_BUCKET, cid.sha256hex)
        except S3Error as err:
            if err.code == "NoSuchKey":
                return False
            else:
                raise err
        return True

    def put(self, cid: CID, filename: FilePath, progress=None):
        file = Path(filename)
        self._minio.fput_object(env.BLX_BUCKET, cid.sha256hex, file, progress=progress)

    def get(self, cid: CID, filename: FilePath, progress=None):
        file = str(Path(filename))
        self._minio.fget_object(env.BLX_BUCKET, cid.sha256hex, file, progress=progress)


@lru_cache
def get_minio():
    return Minio(
        env.BLX_HOST, access_key=env.BLX_ACCESS_KEY, secret_key=env.BLX_SECRET_KEY
    )
