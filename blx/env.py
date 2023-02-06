from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

__all__ = ["Env", "env"]


@dataclass
class Env:
    BLX_BUCKET: str
    BLX_HOST: str
    BLX_ACCESS_KEY: str
    BLX_SECRET_KEY: str


load_dotenv()

env = Env(
    os.getenv("BLX_BUCKET", "blx"),
    os.getenv("BLX_HOST", "s3.danilohorta.me"),
    os.getenv("BLX_ACCESS_KEY", ""),
    os.getenv("BLX_SECRET_KEY", ""),
)
