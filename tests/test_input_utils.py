from haiku_forge.input_utils import InputValidator


def test_get_yes_or_no_reprompts_until_valid(monkeypatch, capsys) -> None:
    answers = iter(["maybe", "Y"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert InputValidator.get_yes_or_no("Continue? ") == "y"
    assert "Please enter 'y' or 'n'." in capsys.readouterr().out
