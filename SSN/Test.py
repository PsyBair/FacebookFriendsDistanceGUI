
'''import numpy as np
from random import randrange


keywords = []
for x in open("Keywords.txt", "r"):
    keywords.append(x.replace('\n', ''))

locs = np.load("locs.npy", allow_pickle=True)
wow = ""
for x in locs:
    numOfKeywords = randrange(10)
    wordList = []
    for i in range(0, numOfKeywords):
        word = randrange(len(keywords))
        wordList.append(keywords[word])
    t = f"{int(x)}, {','.join(wordList)}\n"
    wow = wow + t

file1 = open("tweets_Keywords.txt", "a")
file1.write(wow)
file1.close()

#text = np.loadtxt(fname='tweets_Keywords.txt', delimiter=', ', dtype='U')
#print(text)
#np.save("gowalla_Keywords.npy", text)
'''