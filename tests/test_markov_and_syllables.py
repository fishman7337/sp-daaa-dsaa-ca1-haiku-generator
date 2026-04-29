import random

from haiku_forge.ai_markov import MarkovChainModel
from haiku_forge.ai_syllables import SyllableCounter


def test_syllable_counter_returns_known_word_count() -> None:
    counter = SyllableCounter()

    assert counter.get_syllable_count("autumn.") == 2


def test_markov_model_trains_cleaned_bigram_keys() -> None:
    model = MarkovChainModel()

    model.train(["Red, yellow leaves"])

    assert model.model["red"] == ["yellow"]
    assert model.model["yellow"] == ["leaves"]


def test_markov_generation_returns_capitalised_line() -> None:
    random.seed(7)
    model = MarkovChainModel()
    model.fallback_words = ["sun", "moon", "leaf"]

    line = model.generate_line(3, SyllableCounter())

    assert line
    assert line[0].isupper()
