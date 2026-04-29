# Model Card

## Model Name

HaikuForge AI Markov Haiku Generator

## Model Type

Rule-assisted bigram Markov chain with syllable-count constraints.

## Intended Use

The generator is intended for coursework demonstration and creative haiku-like
text generation. It is not a production natural language generation model.

## Training Data

The model trains at runtime on haiku lines selected by the user. Sample haiku
files are provided in `data/samples`.

## Inputs and Outputs

- Input: A plain text haiku training file.
- Output: Three generated lines with 5, 7, and 5 syllable targets.

## Limitations

- The model only learns adjacent word transitions.
- Generated lines may be grammatically awkward.
- Syllable counts depend on the built-in dictionary and user-provided fallback input.
- Randomness means output varies between runs unless the caller controls the random seed.

## Ethical and Safety Notes

The model does not call external APIs, collect personal data, or access the
network. Generated text should still be reviewed before submission or sharing.
