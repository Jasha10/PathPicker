import os
from typing import Any

from pytest import fixture

from pathpicker.output import join_files_into_command


@fixture
def files_and_line_numbers() -> list[tuple[str, int]]:
    return [
        ("/home/user/file1.txt", 1),
        ("/home/user/file2.txt", 2),
        ("/home/user/file3.txt", 3),
    ]


@fixture(params=["nvim", "nvr"])
def nvim_like_editor(request: Any) -> str:
    _editor = request.param
    assert isinstance(_editor, str)
    return _editor


def test_basic(
    files_and_line_numbers: list[tuple[str, int]], nvim_like_editor: str
) -> None:
    os.environ["FPP_EDITOR"] = nvim_like_editor
    os.environ["FPP_DISABLE_SPLIT"] = ""
    command = join_files_into_command(files_and_line_numbers)
    assert (
        command
        == f'{nvim_like_editor}  +1 /home/user/file1.txt +"vsp +2 /home/user/file2.txt" +"vsp +3 /home/user/file3.txt"'
    )


def test_FPP_DISABLE_SPLIT(
    files_and_line_numbers: list[tuple[str, int]], nvim_like_editor: str
) -> None:
    os.environ["FPP_EDITOR"] = nvim_like_editor
    os.environ["FPP_DISABLE_SPLIT"] = "1"
    command = join_files_into_command(files_and_line_numbers)
    assert (
        command
        == f"{nvim_like_editor}  +1 '/home/user/file1.txt' +2 '/home/user/file2.txt' +3 '/home/user/file3.txt'"
    )

def test_FPP_EDITOR_ENTRY_POINT(
    files_and_line_numbers: list[tuple[str, int]]
) -> None:
    os.environ["FPP_EDITOR_ENTRY_POINT"] = "test_editor_entry_point"
    command = join_files_into_command(files_and_line_numbers)
    assert (
        command
        == f"test_editor /home/user/file1.txt:1 /home/user/file2.txt:2 /home/user/file3.txt:3"
    )
