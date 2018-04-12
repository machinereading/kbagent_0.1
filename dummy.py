
from nltk.corpus import framenet as fn

fs = fn.frames()

for i in fs:
    print(i.FE)
    break
