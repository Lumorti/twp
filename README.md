
# TWP - Thousand Word Picture

A one-to-one mapping of every English word to a unique colour.
This is optimised so that similar words are similar colours, with words generally matching the colour you'd expect.
Mapping v1.0 contains over 630,000 words, including names and verb conjugations.
Note than some words may have been optimised in a weird way, but in general they're pretty close.

This repo contains three main files:
 - mapping.json - the mapping as a JSON file (from word -> colour hex) 
 - inverse.json - the inverse mapping as a JSON file  (from colour hex -> word)
 - twp - a Python script for easy use/regeneration of this mapping

This uses the Python Natural Language Toolkit (NLTK) and its various word/colour lists (WordNet/CSS4/xkcd), 
along with colour association data scraped from from <http://www.cymbolism.com>. These data sets are only required if you want
to regenerate the mapping, see dependencies below.

## Example

The following is the conversion of the entirety of Emma by Jane Austen, which is in the public domain. 
After optimising it seems that green is the preferred colour of punctuation (including newlines), hence the prevalence.
This can be reverted back to the original text, albeit with some formatting changes.

![Emma by Jane Austen, converted to colours using TWP mapping v1.0](https://github.com/lumorti/twp/raw/master/emma.png "Example conversion of Emma")

## Dependencies

For simply using the mapping you'll need the following, some of which are probably already installed on your system:
 - Python3 (sudo apt install python3 pip)
 - matplotlib (pip3 install matplotlib)
 - numpy (pip3 install numpy)
 - pillow (pip3 install pillow)

If you want to tweak/regenerate the mapping you'll need the following:
 - nltk (pip3 install nltk)

## Usage

To convert a text file to an image using the word to colour mapping:

```bash
./twp in.txt out.png
```

To use the inverse mapping to approximately reverse this process:

```bash
./twp --invert in.png out.txt
./twp -i in.png out.txt
```

To just use the words given as arguments and then display:

```bash
./twp --words "summer is hot"
./twp -w "summer is hot"
```

Other flags and general usage can be viewed by not giving any arguments:

```bash
./twp
```

## Regenerating the Mapping

The mapping is generated using a fixed seed, so in theory performing these steps will recreate the exact mapping given here, assuming no major changes are done to the various datasets.

First the data file and mappings should be deleted if they exist:

```bash
rm -f data.json mapping.json inverse.json
```

Then the word list and word association data needs to be loaded, requiring NLTK:

```bash
./twp -1
```

Then the color association data needs to be scraped and processed:

```bash
./twp -2
```

Then the mapping needs to be initialised and optimised:

```bash
./twp -3
```

Then the inverse mapping needs to be regenerated:

```bash
./twp -4
```

As a one-liner, taking about half an hour ish:

```bash
rm -f data.json mapping.json inverse.json && ./twp -1 && ./twp -2 && ./twp -3 && ./twp -4
```
