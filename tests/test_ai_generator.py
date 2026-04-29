from haiku_forge.ai_generator import AIHaikuGenerator


class FakeMarkovModel:
    def __init__(self) -> None:
        self.lines = iter(["first", "second", "first", "third"])

    def generate_line(self, _target_syllables, _counter) -> str:
        return next(self.lines)


def test_generate_haiku_retries_duplicate_third_line() -> None:
    generator = AIHaikuGenerator()
    generator.markov_model = FakeMarkovModel()

    assert generator.generate_haiku() == ["first.", "second.", "third"]
