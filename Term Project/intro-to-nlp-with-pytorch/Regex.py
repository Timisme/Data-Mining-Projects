import re
import numpy as np 
import pandas as pd 

# sentence = 'Start a sentaence and then bring it to an end'

# pattern = re.compile(r'\S')

# matches = pattern.finditer(sentence)

# for match in matches:
# 	print(match)

# \d match one digit
# . match any charactor  
# r'\d\d\d[-.]\d' match either pattern in the bracket 
# match digits between 1 and 5 and a to z --- r'[1-5a-z]'
# ^ match every that is not in the charactor set r'[^1-5a-z]'(非1-5且非a-z)
# https://www.youtube.com/watch?v=K8L6KVGG-7o

# (r'[a-zA-Z0-9_.+-]+@[...]+\.[com|net|...]+') -> ...@...\. com or net,

'''
.       - Any Character Except New Line
\d      - Digit (0-9)
\D      - Not a Digit (0-9)
\w      - Word Character (a-z, A-Z, 0-9, _)
\W      - Not a Word Character
\s      - Whitespace (space, tab, newline)
\S      - Not Whitespace (space, tab, newline)

\b      - Word Boundary
\B      - Not a Word Boundary
^       - Beginning of a String
$       - End of a String

[]      - Matches Characters in brackets
[^ ]    - Matches Characters NOT in brackets
|       - Either Or
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)


#### Sample Regexs ####

[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+
'''


data = np.array([['g','8']])
mask = [True, False]

print(data[mask])


