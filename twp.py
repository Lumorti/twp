#!/usr/bin/python3

import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

# TODO
def processData():
    pass

# TODO
def optimiseMapping():
    pass

# Strip words ready for coversion to colours
def stripWords(words):

    newWords = []
    for i in range(len(words)):

        toAdd = []
        toAdd.append(words[i].lower().strip())

        toAdd[0] = toAdd[0].replace("\"", "")
        toAdd[0] = toAdd[0].replace(".", "")
        toAdd[0] = toAdd[0].replace(",", "")
        toAdd[0] = toAdd[0].replace("!", "")
        toAdd[0] = toAdd[0].replace("?", "")
        toAdd[0] = toAdd[0].replace(":", "")
        toAdd[0] = toAdd[0].replace(";", "")
        toAdd[0] = toAdd[0].replace("(", "").replace(")", "")

        if len(toAdd[0]) > 0:
            if toAdd[0][0] == "'":
                toAdd[0] = toAdd[0][1:]

        if len(toAdd[0]) > 0:
            if toAdd[0][-1] == "'":
                toAdd[0] = toAdd[0][:-1]

        if "-" in toAdd[0] and len(toAdd[0].replace("-", "")) >= 2:
            toAdd = toAdd[0].split("-")

        for j in range(len(toAdd)):
            toAdd[j] = toAdd[j].replace("-", "")
            if len(toAdd[j]) > 0:
                newWords.append(toAdd[j])

    return newWords

# Plot an array of colours, to a file if saveInstead
def plotCols(cols, saveInstead):

    # Initial guess at best dimensions
    total = len(cols)
    rootWidth = math.ceil(math.sqrt(total))
    height = total

    # Test different widths until find one that factors nicely
    for width in range(rootWidth, 1, -1):
        if total % width == 0:
            height = int(total / width)
            break

    # Convert to numpy data
    data = np.array(cols, dtype='uint8').reshape((height, width, 3))

    # Plot
    plt.imshow(data, interpolation='none')
    plt.axis('off')

    # Either show or save
    if saveInstead:
        plt.save("output.png")
    else:
        plt.show()

# Load a mapping from a file
def loadMapping(mapFile):
    mapping = {}
    with open(mapFile, "r") as f:
        mapping = json.load(f)
    return mapping

# Write a mapping to a file
def saveMapping(mapping, mapFile):
    with open(mapFile, "w") as f:
        json.dump(mapping, f)
        f.write("\n")

# Use a mapping to get the colours for a set of words
def useMapping(mapping, wordsToConvert):

    outputColours = []
    for word in wordsToConvert:
        if word in mapping.keys():
            outputColours.append(intToCol(mapping[word]))
        else:
            print("unknown word: " + word)
            outputColours.append((0, 0, 0))
    return outputColours

# Convert an integer (<= 255**3) to a colour tuple
def intToCol(i):
    r = int(i / 65536)
    rem = i % 65536
    g = int(rem / 256)
    rem = rem % 256
    b = rem
    return (r, g, b)

# Convert a colour tuple to an integer between 0 and 255**3
def colToInt(col):
    return col[0]*65536 + col[1]*256 + col[2]

def printHelp():

    print("TWP - Thousand Word Picture")
    print("")
    print("Description:")
    print(" Converts a word (or many) into colours.")
    print(" This uses a one-to-one mapping optimised to")
    print(" group similiar words together and have the")
    print(" colours represent the words as best as possible.")
    print("")
    print("Usage:")
    print(" ./twp [flags?] [\"words\"/filename]")
    print("")
    print("General Flags:")
    print(" --help  -h         output this message")
    print("")
    print("Output Flags:")
    print(" --disp  -d         display the resulting image (default)")
    print(" --save  -s         save the resulting image")
    print(" --term  -t         output as text instead of an image")
    print("")
    print("Dev Flags:")
    print(" --map   -m [file]  specify a mapping (default: map.json)")
    print(" --word  -w [file]  specify a word list (default: words.txt)")
    print(" --gen   -g         reset the mapping from the word list")
    print(" --opt   -o         optimise the mapping")

if __name__ == "__main__":

    # Param defaults
    action = "help"
    inputMode = "file"
    outputMode = "disp"
    mapFile = "map.json"
    wordFile = "words.txt"

    # The words/files to process
    wordArgs = []

    # Loop over the arguments given
    ind = 1
    while ind < len(sys.argv):
        arg = sys.argv[ind]

        # If asking for the help text
        if arg in ["--help", "-h"]:
            action = "help"
        elif arg in ["--save", "-s"]:
            outputMode = "save"
        elif arg in ["--term", "-t"]:
            outputMode = "term"
        elif arg in ["--gen", "-g"]:
            action = "gen"
        elif arg in ["--opt", "-o"]:
            action = "opt"
        elif arg in ["--map", "-m"]:
            mapFile = sys.argv[ind+1]
            ind += 1
        elif arg in ["--word", "-w"]:
            wordFile = sys.argv[ind+1]
            ind += 1

        # Otherwise it's either a word list or a filename
        else:
            if "." in arg:
                inputMode = "file"
                wordArgs.append(arg)
            else:
                inputMode = "words"
                wordArgs.extend(arg.split())
            if action == "help": action = "use"

        ind += 1

    # If asking for help
    if action == "help":
        printHelp()

    # Normal usage
    elif action == "use":

        # Load the mapping
        mapping = loadMapping(mapFile)

        # If using files
        if inputMode == "file":
            with open(wordArgs[0]) as f:
                wordsToConvert = f.read().strip().split()

        # If using quoted words
        elif inputMode == "words":
            wordsToConvert = wordArgs

        # Get rid of certain characters, force lowercase, split hyphons
        wordsToConvert = stripWords(wordsToConvert)

        # Use the mapping
        outputCols = useMapping(mapping, wordsToConvert)

        # Output the resulting colours as text
        if outputMode == "term":
            for index, word in enumerate(wordsToConvert):
                print(word + " -> " + repr(outputCols[index]))

        # Output the resulting colours as an image to the screen
        elif outputMode == "disp":
            plotCols(outputCols, False)

        # Output the resulting colours as an image to a file
        elif outputMode == "save":
            plotCols(outputCols, True)

    # Generating a new mapping
    elif action == "gen":

        # The unique words
        words = []

        # The mapping dict to be populated
        mapping = {}

        # Load the word list specified and get the words
        with open(wordFile, "r") as f:
            fileText = f.readlines()
            for line in fileText:
                words.extend(line.split())

        # Scaling factor for unique initial colours
        colIntPerIndex = int(255**3 / len(words))

        # Add metadata to the dictionary
        mapping[";:avgscore"] = 0
        mapping[";:minscore"] = 0
        mapping[";:maxscore"] = 0
        mapping[";:numwords"] = len(words)

        # For each word given
        for index, word in enumerate(words):

            # Generate a unique colour based on the index
            newColour = index * colIntPerIndex

            # Create the corresponding dictionary element
            mapping[word] = newColour

        # Save this new mapping
        saveMapping(mapping, mapFile)

    # Optimising an existing mapping
    elif action == "opt":
        pass








