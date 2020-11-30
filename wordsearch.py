'''
    Efficiently find start and end coordinates for words in a wordsearch

    Sample output:
        {'c': ((0, 0), (0, 0)),
        'car': ((0, 0), (0, 2)),
        'carpet': ((0, 0), (0, 5)),
        'cat': ((0, 0), (2, 0))}
'''

class WordsearchSolver():
    vectors = [
        (+1, 0 ), # right       >
        (0, +1 ), # down        v
        (+1, +1), # down, right \
        (+1, -1)  # up, right   /
    ]

    def __init__(self, grid):
        self.grid = grid

    def addWord(self, word, reversed):
        node = self.lookup
        label = word
        if reversed:
            word = word[::-1]
        for c in word:
            if c not in node:
                node[c] = {}
            node = node[c]
        if reversed:
            node["<"] = label
        else:
            node[">"] = label

    def next(self, x, y, vector):
        x += vector[0]
        y += vector[1]
        if x >= len(grid[0]) or y >= len(grid) or y < 0 or x < 0:
            return None, None
        return x, y

    def findFromHere(self, x, y, grid):
        for direction in self.vectors:
            self.findFromHereVector(x, y, direction, grid)

    def findFromHereVector(self, x, y, direction, grid):
        startPoint = (x, y)
        node = self.lookup
        while True:
            c = grid[y][x]
            if c not in node:
                break
            node = node[c]
            # reversed first so that pallindromes will favour forwards
            if '<' in node:
                word = node['<']
                self.results[word] = ((x,y), startPoint)
            if '>' in node: # can be both (eg. dog, god)
                word = node['>']
                self.results[word] = (startPoint, (x,y))
            x, y = self.next(x, y, direction)
            if x == None:
                break

    def findInWords(self, words):
        # prepare lookup tree
        self.lookup = {}
        self.results = {}
        for word in words:
            self.addWord(word, True)
            self.addWord(word, False)

        # Find words by assuming each square is a start (or end) of one or more words
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.findFromHere(x, y, self.grid)
        return self.results


if __name__ == "__main__":
    import pprint

    grid = [
        "catblah",
        "aogblah",
        "rogblah",
        "pogodoo",
        "eogftat",
        "togfooo",
    ]

    ws = WordsearchSolver(grid)
    r = ws.findInWords(['c', 'car', 'carpet', 'cat', 'tat'])
    pprint.pprint(r)
    r = ws.findInWords(['dog', 'god'])
    pprint.pprint(r)