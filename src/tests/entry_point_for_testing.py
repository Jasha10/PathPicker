def compose_command(files_and_line_numbers: list[tuple[str, int]]) -> str:
    return "test_editor " + " ".join(
        [f"{file}:{line}" for file, line in files_and_line_numbers]
    )
