# -*- coding: utf-8 -*-
"""“NLP_Project1.ipynb”

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F_s8vlAoqbr5SRUu6QW4rFFatqn4wGv2
"""

import math
class Unigram:
  def __init__(self):
    self.unigramCounts = {"<unk>":0} #stores unigram[token] counts make sure UNK already initialized to 0
    self.vocabSet = set() #stores total vocab size
    self.totalCount = 0

#Increase count of a token or adds it to dictionary
  def addToken(self, token):
    if token not in self.unigramCounts: #If not already in the dictionary add it in with a count of 1 and increase the vocab size
      self.unigramCounts[token] = 0
      self.vocabSet.add(token)
    self.unigramCounts[token] += 1 #If already in dictionary increment its count by 1
    self.totalCount +=1

#Gets token count if it can't find it return the count of UNK unkown
  def getTokenCount(self, token):
    token = token.lower()
    if token not in self.unigramCounts:
      return self.unigramCounts["<unk>"]
    else:
      return self.unigramCounts[token]

#Converts an input line of space delineated text into a readable token array
  def convertLineToTokenArray(self, line):
    tokens = line.lower().split()
    tokens = ["<s>"] + tokens + ["</s>"] #add start and stop tokens to beginning and end of line
    return tokens

#Any token counts under the threshold are removed from the dictionary and their counts added to the UNK count
  def handleUnknownTokens(self, threshold):
    listOfTokens = list(self.unigramCounts.keys())
    listOfTokens.remove("<unk>")
    for token in listOfTokens:
      if self.getTokenCount(token) <= threshold:
        self.unigramCounts["<unk>"] += self.getTokenCount(token)
        del self.unigramCounts[token]

  def addArrayToUnigram(self, tokens):
    for token in tokens:
      self.addToken(token)

  def getVocabSize(self):
    return len(self.vocabSet)

  def trainFileGetCounts(self, filename):
    with open(filename, "r") as file:
      for line in file:
        tokenArray = self.convertLineToTokenArray(line)
        self.addArrayToUnigram(tokenArray)

  def getLaplaceSmoothedTokenProb(self, token, smoothAmount, vocabSize):
    return ((self.getTokenCount(token) + smoothAmount) / ((self.totalCount) + (smoothAmount*vocabSize)))

  def getPerplexityOnFile(self, filePath, smoothAmount):
    with open(filePath, "r") as file:
      totalLogProb = 0
      totalTokens = 0
      for line in file:
        tokenArray = self.convertLineToTokenArray(line)
        for token in tokenArray:
          prob = self.getLaplaceSmoothedTokenProb(token, smoothAmount, self.getVocabSize())
          totalLogProb += math.log(prob)
          totalTokens += 1
      avgLogProb = totalLogProb / totalTokens
      perplexity = math.exp(-avgLogProb)

      return perplexity

  def addCount(self, token, count):
    if token not in self.unigramCounts:
      self.unigramCounts[token] = 0
      self.vocabSet.add(token)
    self.totalCount += count
    self.unigramCounts[token] += count

class Bigram:
  def __init__(self):
    self.bigramCounts = {"<unk>":Unigram()}
    self.vocabSet = set()

  def convertLineToTokenArray(self, line):
    tokens = line.lower().split()
    tokens = ["<s>"] + tokens + ["</s>"]
    return tokens

  def addBigramTokens(self, firstToken, secondToken):
    if firstToken not in self.bigramCounts:
      self.bigramCounts[firstToken] = Unigram()
      self.vocabSet.add(firstToken)
    self.bigramCounts[firstToken].addToken(secondToken)

  def addArrayToBigram(self, tokens):
    for i in range(len(tokens)-1):
      self.addBigramTokens(tokens[i], tokens[i+1])

  def trainFileGetCounts(self, filePath):
    with open(filePath, "r") as file:
      for line in file:
        tokenArray = self.convertLineToTokenArray(line)
        self.addArrayToBigram(tokenArray)

  def getUnigram(self, firstToken):
    firstToken = firstToken.lower()
    if firstToken not in self.bigramCounts:
      return self.bigramCounts["<unk>"]
    else:
      return self.bigramCounts[firstToken]

  def getLSmoothedTokenProb(self, firstToken, secondToken, smoothAmount):
    vocabSize = len(self.vocabSet)
    unigram = self.getUnigram(firstToken)
    return unigram.getLaplaceSmoothedTokenProb(secondToken, smoothAmount, vocabSize)

  def getPerplexityOnFile(self, filePath, smoothing):
    with open(filePath, "r") as file:
      totalLogProb = 0
      totalTokens = 0
      for line in file:
        tokenArray = self.convertLineToTokenArray(line)
        for i in range(len(tokenArray)-1):
          prob = self.getLSmoothedTokenProb(tokenArray[i], tokenArray[i+1], smoothing)
          totalLogProb += math.log(prob)
          totalTokens += 1
      avgLogProb = totalLogProb / totalTokens
      perplexity = math.exp(-avgLogProb)

      return perplexity

  def handleUnknownTokens(self, threshold1, threshold2):
    listOfFirstTokens = list(self.bigramCounts.keys())
    listOfFirstTokens.remove("<unk>")
    for firstToken in listOfFirstTokens:
      unigram = self.getUnigram(firstToken)
      if unigram.totalCount <= threshold1:
        unigramTokens = list(unigram.unigramCounts.keys())
        for secondToken in unigramTokens:
          count=unigram.getTokenCount(secondToken)
          self.bigramCounts["<unk>"].addCount(secondToken, count)

        del self.bigramCounts[firstToken]
    for firstToken in self.bigramCounts:
      self.bigramCounts[firstToken].handleUnknownTokens(threshold2)

unigram = Unigram()
unigram.trainFileGetCounts("/content/drive/MyDrive/NLP_HW/train.txt")
unigram.handleUnknownTokens(1)
print(unigram.getLaplaceSmoothedTokenProb('The',5, unigram.getVocabSize()))
print(unigram.getPerplexityOnFile("/content/drive/MyDrive/NLP_HW/train.txt", 1))
print(unigram.getPerplexityOnFile("/content/drive/MyDrive/NLP_HW/val.txt", 1))

bigram = Bigram()
bigram.trainFileGetCounts("/content/drive/MyDrive/NLP_HW/train.txt")
bigram.handleUnknownTokens(20, 5)
print(bigram.getPerplexityOnFile("/content/drive/MyDrive/NLP_HW/train.txt", 2))