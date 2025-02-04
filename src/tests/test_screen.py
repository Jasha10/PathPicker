# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from pytest import mark, param

from tests.lib import screen_test_runner

EXPECTED_DIR = Path("./expected/")


@dataclass(frozen=True)
class ScreenTestCase:
    name: str
    input_file: str = "gitDiff.txt"
    inputs: list[str] = field(default_factory=list)
    args: list[str] = field(default_factory=list)
    screen_config: dict[str, int] = field(default_factory=dict)
    past_screen: int | None = None
    past_screens: list[int] | None = None
    with_attributes: bool = False
    validate_file_exists: bool = False


SCREEN_TEST_CASES: list[ScreenTestCase] = [
    ScreenTestCase("simpleLoadAndQuit"),
    ScreenTestCase(
        "tallLoadAndQuit",
        screen_config={
            "maxX": 140,
            "maxY": 60,
        },
    ),
    ScreenTestCase("selectFirst", inputs=["f"]),
    ScreenTestCase("selectFirstWithDown", inputs=["F"]),
    ScreenTestCase("selectDownSelect", inputs=["f", "j", "f"]),
    ScreenTestCase("selectWithDownSelect", inputs=["F", "f"]),
    ScreenTestCase("selectDownSelectInverse", inputs=["f", "j", "f", "A"]),
    ScreenTestCase("selectWithDownSelectInverse", inputs=["F", "F", "A"]),
    ScreenTestCase(
        "selectTwoCommandMode",
        input_file="absoluteGitDiff.txt",
        inputs=["f", "j", "f", "c"],
        past_screen=3,
    ),
    ScreenTestCase("selectAllFromArg", input_file="absoluteGitDiff.txt", args=["-a"]),
    ScreenTestCase("executeKeysEndKeySelectLast", args=["-e", "END", "f"]),
    # the last key "a" is so we quit from command mode
    # after seeing the warning
    ScreenTestCase(
        "selectCommandWithPassedCommand",
        input_file="absoluteGitDiff.txt",
        with_attributes=True,
        inputs=["f", "c", "a"],
        past_screen=1,
        args=["-c 'git add'"],
    ),
    ScreenTestCase("simpleWithAttributes", with_attributes=True),
    ScreenTestCase(
        "simpleSelectWithAttributes", with_attributes=True, inputs=["f", "j"]
    ),
    ScreenTestCase(
        "simpleSelectWithColor",
        input_file="gitDiffColor.txt",
        with_attributes=True,
        inputs=["f", "j"],
        screen_config={
            "maxX": 200,
            "maxY": 40,
        },
    ),
    ScreenTestCase(
        "gitDiffWithScroll", input_file="gitDiffNoStat.txt", inputs=["f", "j"]
    ),
    ScreenTestCase(
        "gitDiffWithScrollUp", input_file="gitLongDiff.txt", inputs=["k", "k"]
    ),
    ScreenTestCase(
        "gitDiffWithPageDown", input_file="gitLongDiff.txt", inputs=[" ", " "]
    ),
    ScreenTestCase(
        "gitDiffWithPageDownColor",
        input_file="gitLongDiffColor.txt",
        inputs=[" ", " "],
        with_attributes=True,
    ),
    ScreenTestCase(
        "gitDiffWithValidation",
        input_file="gitDiffSomeExist.txt",
        validate_file_exists=True,
        with_attributes=True,
    ),
    ScreenTestCase(
        "longFileNames",
        input_file="longFileNames.txt",
        validate_file_exists=False,
        with_attributes=False,
        screen_config={
            "maxX": 20,
            "maxY": 30,
        },
    ),
    ScreenTestCase(
        "longFileNamesWithBeforeTextBug",
        input_file="longFileNamesWithBeforeText.txt",
        validate_file_exists=False,
        with_attributes=False,
        inputs=["f"],
        screen_config={
            "maxX": 95,
            "maxY": 40,
        },
    ),
    ScreenTestCase(
        "dontWipeChrome",
        input_file="gitDiffColor.txt",
        with_attributes=True,
        validate_file_exists=False,
        inputs=["DOWN", "f", "f", "f", "UP"],
        screen_config={"maxX": 201, "maxY": 40},
        past_screens=[0, 1, 2, 3, 4],
    ),
    ScreenTestCase(
        "longFileTruncation",
        input_file="superLongFileNames.txt",
        with_attributes=True,
        inputs=["DOWN", "f"],
        screen_config={"maxX": 60, "maxY": 20},
    ),
    ScreenTestCase(
        "xModeWithSelect",
        input_file="gitDiff.txt",
        with_attributes=True,
        inputs=["x", "G", "J"],
    ),
    ScreenTestCase(
        "gitAbbreviatedFiles",
        input_file="gitAbbreviatedFiles.txt",
        with_attributes=True,
        inputs=["f", "j"],
    ),
    ScreenTestCase("selectAllBug", input_file="gitLongDiff.txt", inputs=["A"]),
    ScreenTestCase(
        "allInputBranch", input_file="gitBranch.txt", args=["-ai"], inputs=["j", "f"]
    ),
    ScreenTestCase(
        "abbreviatedLineSelect",
        input_file="longLineAbbreviated.txt",
        validate_file_exists=False,
        inputs=["j", "j", "f"],
    ),
    ScreenTestCase(
        "longListPageUpAndDown",
        input_file="longList.txt",
        inputs=["NPAGE", "NPAGE", "NPAGE", "PPAGE"],
        validate_file_exists=False,
    ),
    ScreenTestCase(
        "longListHomeKey",
        input_file="longList.txt",
        inputs=[" ", " ", "HOME"],
        with_attributes=True,
        validate_file_exists=False,
        screen_config={"maxY": 10},
    ),
    ScreenTestCase(
        "longListEndKey",
        input_file="longList.txt",
        inputs=["END"],
        with_attributes=True,
        validate_file_exists=False,
        screen_config={"maxY": 10},
    ),
    ScreenTestCase(
        "tonsOfFiles",
        input_file="tonsOfFiles.txt",
        inputs=["A", "c"],
        validate_file_exists=False,
        past_screen=1,
        screen_config={"maxY": 30},
    ),
    ScreenTestCase(
        "fileNameWithSpacesDescription",
        input_file="fileNamesWithSpaces.txt",
        inputs=["d"],
        validate_file_exists=True,
        screen_config={
            "maxX": 201,
        },
    ),
]

assert len(SCREEN_TEST_CASES) == len(
    set(test_case.name for test_case in SCREEN_TEST_CASES)
)  # assert no cases were copy-pasta'd


class TestScreenLogic:
    @mark.parametrize(
        "test_case",
        [param(test_case, id=test_case.name) for test_case in SCREEN_TEST_CASES],
    )
    def test_screen_inputs(self, test_case: ScreenTestCase) -> None:
        char_inputs = ["q"]  # we always quit at the end
        char_inputs = test_case.inputs + char_inputs

        args = test_case.args
        screen_data = screen_test_runner.get_rows_from_screen_run(
            input_file=test_case.input_file,
            char_inputs=char_inputs,
            screen_config=test_case.screen_config,
            print_screen=False,
            past_screen=test_case.past_screen,
            past_screens=test_case.past_screens,
            args=args,
            validate_file_exists=test_case.validate_file_exists,
            all_input=("-ai" in args or "--all-input" in args),
        )

        self.compare_to_expected(test_case, screen_data)

    def compare_to_expected(
        self, test_case: ScreenTestCase, screen_data: tuple[list[str], list[str]]
    ) -> None:
        self.maybe_make_expected_dir()
        actual_lines, _actual_attributes = screen_data

        if test_case.with_attributes:
            self.compare_lines_and_attributes_to_expected(test_case.name, screen_data)
        else:
            self.compare_lines_to_expected(test_case.name, actual_lines)

    def compare_lines_and_attributes_to_expected(
        self, test_name: str, screen_data: tuple[list[str], list[str]]
    ) -> None:
        actual_lines, actual_attributes = screen_data
        actual_merged_lines: list[str] = []
        for actual_line, attribute_line in zip(actual_lines, actual_attributes):
            actual_merged_lines.append(actual_line)
            actual_merged_lines.append(attribute_line)

        self.output_if_not_file(test_name, "\n".join(actual_merged_lines))
        expected_file = self.get_expected_file(test_name)
        expected_merged_lines = expected_file.read_text().split("\n")
        self.assert_equal_lines(test_name, actual_merged_lines, expected_merged_lines)

    def compare_lines_to_expected(
        self, test_name: str, actual_lines: list[str]
    ) -> None:
        self.output_if_not_file(test_name, "\n".join(actual_lines))

        file = open(self.get_expected_file(test_name))
        expected_lines = file.read().split("\n")
        file.close()

        self.assert_equal_lines(test_name, actual_lines, expected_lines)

    def output_if_not_file(self, test_name: str, output: str) -> None:
        expected_file = self.get_expected_file(test_name)
        if not expected_file.is_file():
            print(f"Could not find file {expected_file} so outputting...")
            expected_file.write_text(output)
            assert (
                False
            ), f"File outputted, please inspect {expected_file} for correctness"

    def assert_equal_lines(
        self, test_name: str, actual_lines: list[str], expected_lines: list[str]
    ) -> None:
        self.assert_equal_num_lines(test_name, actual_lines, expected_lines)
        expected_file = self.get_expected_file(test_name)
        glob_needle = " (glob)"
        for index, expected_line in enumerate(expected_lines):
            actual_line = actual_lines[index]
            error_message = (
                f"Line {index + 1} did not match for test {expected_file}:\n\n"
                f'Expected:"{expected_line}"\nActual  :"{actual_line}"'
            )
            if expected_line.endswith(glob_needle):
                self.assert_equal_with_glob(
                    expected_line[: -len(glob_needle)], actual_line, error_message
                )
            else:
                assert expected_line == actual_line, error_message

    def assert_equal_num_lines(
        self, test_name: str, actual_lines: list[str], expected_lines: list[str]
    ) -> None:
        assert len(actual_lines) == len(expected_lines), (
            f"{test_name} test: Actual lines was {len(actual_lines)} "
            f"but expected lines was {len(expected_lines)}"
        )

    def assert_equal_with_glob(
        self, expected_line: str, actual_line: str, error_message: str
    ) -> None:
        # Escape all regex symbols and replace "*" with ".*"
        pattern = ".*".join(map(re.escape, expected_line.split("*")))
        assert re.match(pattern, actual_line), error_message

    @staticmethod
    def get_expected_file(test_name: str) -> Path:
        return Path(os.path.join(EXPECTED_DIR, test_name + ".txt"))

    @staticmethod
    def maybe_make_expected_dir() -> None:
        if not os.path.isdir(EXPECTED_DIR):
            os.makedirs(EXPECTED_DIR)
