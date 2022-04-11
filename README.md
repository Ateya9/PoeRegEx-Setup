# PoeRegEx-Setup

## Purpose
The overall purpose of this program is to take a list of items which are made up of one or more strings, and come up with a short regular expression that matches each string in those items, but none of the strings in the others. Each regular expression also should not match anything in a 'banned words' list. 

The practical application of this is to take in a list of all map mods that appear in PoE, and get a list of their matching regular expressions. A user can then pick the mods they don't want on their maps, paste the regular expression into the search bar, and the maps with those mods will be highlighted so they can be rerolled.

This program could also be used to build a list of regular expressions for each item base type for the purposes of Gwennen gambling.
