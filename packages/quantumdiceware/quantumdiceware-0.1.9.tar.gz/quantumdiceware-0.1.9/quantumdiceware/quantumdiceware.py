"""
Diceware passphrases generated from quantum random data.
http://github.com/justinsloan/qdg

Requires Python 3.6 or better

Features:
    - Simulates dice rolls by gathering quantum data.
    - Includes the complete standard Diceware wordlist.
    - Generate passphrases from custom wordlists.

Usage:
    >>> $ pip3 install quantumdiceware
    >>> $ qdg
    >>> $ qdg -c 6 > output.txt

Version History:
0.1.9 - 6 JAN 2018
- added '--version' option
- improved verbose mode printing
- updated documentation, switched to .rst format

0.1.8 - 5 JAN 2018
- first release build
"""

__version__ = "0.1.9"

import random
import argparse
import quantumrandom
import pkg_resources

# Specify the location of the word list inside the package
resource_name = __name__
path = "diceware_word_list.txt"
word_list_file = pkg_resources.resource_filename(resource_name, path)

# Build the argument parser
parser = argparse.ArgumentParser(
    description="Generate Diceware passphrases using quantum data.",
    epilog=f"QDG v.{__version__} | by Justin M. Sloan")
parser.add_argument("-c","--count",nargs="?",default=1,type=int, help="number of passphrases to generate")
parser.add_argument("-w","--words",nargs="?",default=6,type=int, help="number of words per passphrase")
parser.add_argument("-v","--verbose",action="store_true", help="increase output verbosity")
parser.add_argument("-l","--local",action="store_false", help="use local random data, no connection required (faster)")
parser.add_argument("-f","--file",nargs="?",default=word_list_file, help="specify the word list to use")
parser.add_argument("--version",action="version",version=f"QDG v.{__version__}")
args = parser.parse_args()

# Set the verbose status
if args.verbose:
    verbose = True
else:
    verbose = False

# Load the wordlist file
word_dict = {}
with open(args.file) as f:
    for line in f.readlines():
        index, word = line.strip().split('\t')
        word_dict[int(index)] = word


def p_verbose(text):
    if verbose:
        print(text)


def generate_diceware_phrase(word_count=6, quantum=True):
    """Generates a Diceware Passphrase of length N."""
    passphrase = []

    if quantum:
        p_verbose("Gathering quantum data...")
        data_count = word_count * 5
        quantum_data = quantumrandom.uint16(data_count)
        dice = (int("".join([str(y) for y in (quantum_data % 6) + 1])))
        roll = [str(dice)[i:i+5] for i in range(0, len(str(dice)), 5)]
        for i in roll:
            p_verbose(f"Dice Rolls: {i}")
            passphrase.append(word_dict[int(i)])
    else:
        p_verbose("Using local random data...")
        for words in range(0, word_count):
            this_index = 0
            for position in range(0, 5):
                digit = random.randint(1, 6)
                this_index += digit * pow(10, position)
            passphrase.append(word_dict[this_index])
            p_verbose(f"Dice Rolls: {this_index}")
    return ' '.join(passphrase)   


def main():
    """Takes optional arguments and prints passphrases."""

    # Loop until requested number of passphrases are generated
    for i in range(0,args.count):
        phrase = generate_diceware_phrase(args.words, args.local)
        print(phrase)
