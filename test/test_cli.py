import os
from pathlib import Path

from typer.testing import CliRunner

from blx.cli import app

runner = CliRunner()

HELLO_FILE_NAME = "hello.txt"
HELLO_FILE_CID = "486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7"
HELLO_FILE_CONTENT = "world"


def write_hello_file():
    with open(HELLO_FILE_NAME, "w") as f:
        f.write(HELLO_FILE_CONTENT)


def test_put(tmp_path: Path):
    os.chdir(tmp_path)
    write_hello_file()
    result = runner.invoke(app, ["put", "--no-progress", HELLO_FILE_NAME])
    assert result.exit_code == 0
    assert len(result.stdout.strip()) == 0


def test_has():
    result = runner.invoke(app, ["has", HELLO_FILE_CID])
    assert result.exit_code == 0
    assert len(result.stdout.strip()) == 0


def test_cid(tmp_path: Path):
    os.chdir(tmp_path)
    write_hello_file()
    result = runner.invoke(app, ["cid", "--no-progress", HELLO_FILE_NAME])
    assert result.exit_code == 0
    assert result.stdout.strip() == HELLO_FILE_CID


def test_get(tmp_path: Path):
    os.chdir(tmp_path)
    result = runner.invoke(
        app, ["get", "--no-progress", HELLO_FILE_CID, HELLO_FILE_NAME]
    )
    assert result.exit_code == 0
    assert len(result.stdout.strip()) == 0
    assert Path(HELLO_FILE_NAME).exists()
