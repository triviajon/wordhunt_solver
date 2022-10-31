# wordhunt_solver
solves wordhunt

This repo solves the popular "Wordhunt" game on iPhones. The idea behind the algorithm is simple: generate paths of some specified (optimal) length without checking if the path actually produces a word. The order in which paths are generated are based on the frequency on which each letter appears as the "first letter" of a word in the English dictionary. Then, check if these paths are valid. Return some number of words at a time, along with where they appear in the WordHunt instance (0 -> 1 -> ...). 

It's not very fast yet, and definitely has room for optimization. Unfortunately, the path generation problem is exptime since there is no way to quickly check that you have generated all possible paths without generating them entirely, so a faster algorithm depends on optimization of the code, not a different algorithm.

Have fun exploring!
