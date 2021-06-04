from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter


def static_code_check(filepath: str) -> tuple[int, list]:
    """Statically Checks the programming code

    Args:
        filepath (str): A file that has to be checked

    Returns:
        tuple[int, list]: returns a tuple of the score and the list of all messages
    """
    messages = StringIO()
    reporter = TextReporter(output=messages)
    results = Run(
        [filepath, "--msg-template='Line {line}: {msg} ({msg_id})"],
        reporter=reporter,
        do_exit=False,
    )  # Change Message format, remove Module test warning,
    score = results.linter.stats["global_note"] * 10
    messages = messages.getvalue().rsplit("\n", 4)[0].split("\n")
    return int(score), messages[1 : len(messages) - 1]
