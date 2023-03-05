from __future__ import annotations

from pydantic import BaseModel, constr

from blx.regex import SHA256HEX_REGEX

__all__ = ["CID"]

BUFSIZE = 4 * 1024 * 1024


class CID(BaseModel):
    sha256hex: constr(regex=SHA256HEX_REGEX)

    def __eq__(self, x: CID):
        return x.sha256hex == self.sha256hex
