from __future__ import annotations

import importlib.metadata
import re
from pathlib import Path
from typing import Optional

import typer
from rich.progress import track
from typer import Argument, Exit, Option, Typer, echo

from blx.cid import CID
from blx.client import get_client
from blx.file_digest import FileDigest
from blx.progress import Progress
from blx.regex import SHA256HEX_REGEX
from blx.service_exit import service_exit

__all__ = ["app"]


app = Typer(
    add_completion=False,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


def regex_match(regex):
    def callback(value):
        if re.match(regex, value):
            return value
        raise typer.BadParameter(f"Does not match {regex}")

    return callback


O_PROGRESS = Option(True, "--progress/--no-progress", help="Display progress bar.")
O_CID = Argument(..., callback=regex_match(SHA256HEX_REGEX))


@app.callback(invoke_without_command=True)
def cli(version: Optional[bool] = Option(None, "--version", is_eager=True)):
    if version:
        echo(importlib.metadata.version(__package__))


@app.command()
def has(cid: str):
    """
    Check if file exists.
    """
    raise Exit(0 if get_client().has(CID(sha256hex=cid)) else 1)


@app.command()
def cid(path: Path, progress: bool = O_PROGRESS):
    """
    CID of file.
    """
    with service_exit():
        digest = FileDigest(path)
        with digest:
            for chunk in track(digest, "Hash", disable=not progress):
                chunk.update()
            echo(digest.cid.sha256hex)


@app.command()
def put(path: Path, progress: bool = O_PROGRESS):
    """
    Upload file.
    """
    with service_exit():
        digest = FileDigest(path)
        with digest:
            for chunk in track(digest, "Hash", disable=not progress):
                chunk.update()
        cid = digest.cid

        clt = get_client()
        if clt.has(cid):
            raise Exit()

        with Progress("Upload", disable=not progress) as pbar:
            try:
                clt.put(cid, path, pbar)
            finally:
                pbar.shutdown()


@app.command()
def get(cid: str, path: Path, progress: bool = O_PROGRESS):
    """
    Download file.
    """
    with service_exit():
        clt = get_client()
        if not clt.has(CID(sha256hex=cid)):
            raise Exit(1)

        with Progress("Download", disable=not progress) as pbar:
            try:
                clt.get(CID(sha256hex=cid), path, pbar)
            finally:
                pbar.shutdown()
