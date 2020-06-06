
# TWP - Thousand Word Picture

A one-to-one mapping of every English word and name to a unique colour.
This is optimised so that similar words are similar colours, with words generally matching the colour you'd expect.

This repo contains two main files:
 - mapping.json - the mapping as a JSON file for easy creation of a hash table
 - twp - a Python script for easy use/regeneration of this mapping

This uses the Python Natural Language Toolkit (NLTK) and its various word/colour lists (WordNet/CSS4/xkcd), 
along with colour association data scraped from from <http://www.cymbolism.com>.

## Example


## Dependencies

For simply using the mapping, which are probably already installed on your system:
 - Python3 (sudo apt install python3 pip)
 - matplotlib (pip3 install matplotlib)
 - numpy (pip3 install numpy)

If you want to tweak/regenerate the mapping:
 - nltk (pip3 install nltk)

## Usage

To bring up a visualisation of a set of words:

```bash
./twp --disp "summer is hot, winter is cold"
```

To output to "output.png" instead:

```bash
./twp --save "summer is hot, winter is cold"
```

To output a color list to the terminal instead:

```bash
./twp --term "summer is hot, winter is cold"
```

To save a visualisation of a text file to "output.png":

```bash
./twp --save filename.txt
```

Other flags, including shorthands for the above commands, can be viewed using the help:

```bash
./twp --help
```

## Regenerating the Mapping

The mapping is generated using a fixed seed, so in theory performing these steps will recreate the exact mapping given here, assuming no major changes are done to the various datasets.

First the data file and mapping should be deleted:

```bash
rm data.json mapping.json
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
