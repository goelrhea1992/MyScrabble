import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = [('a', 1), ('c', 3), ('b', 3), ('e', 1), ('d', 2), ('g', 2), ('f', 4), ('i', 1), ('h', 4), ('k', 5), ('j', 8), ('m', 3), ('l', 1), ('o', 1), ('n', 1), ('q', 10), ('p', 3), ('s', 1), ('r', 1), ('u', 1), ('t', 1), ('w', 4), ('v', 4), ('y', 4), ('x', 8), ('z', 10)]

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def checkXInFreqList(freq,x):
	"""
	This function checks whether x exists as a key in some tuple(x,_) of freq list 
	return True or False
	"""
	count=0
	for i in freq:
		if i[0] == x:	
			return True, count
		count = count + 1
	return False, len(freq) + 1


def getFrequencyList(sequence):
    """
    Returns a list of lists where the first element of inner list are elements of the sequence
    and second element of inner list are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    
    return: dictionary
    """
    # freqs: list [[element_type -> int]]
    freq = []
    for x in sequence:
	 bl, index = checkXInFreqList(freq, x)
	 if not bl:
		freq.append([x, 1])
	 else:
		freq[index][1] += 1
    return freq


def getWordScore(word, n):
    """
        Returns the score for a word. Assumes the word is a
        valid word.
        
        The score for a word is the sum of the points for letters
        in the word, multiplied by the length of the word,  plus 50
        points if all n letters are used on the first go.
        
        Letters are scored as in Scrabble; A is worth 1, B is
        worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.
        
        word: string (lowercase letters)
           n: integer (maximum hand size; i.e., hand size required for additional points)
        
        returns: int >= 0
    """
    value=0
    for letter in word:
		for i in range(len(SCRABBLE_LETTER_VALUES)):
			if letter == SCRABBLE_LETTER_VALUES[i][0]:
				value += SCRABBLE_LETTER_VALUES[i][1]
    value = value * len(word)
    if len(word) == n:
		value = value + 50
    print "\nThe value of the word is: ", value
    return value


def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       displayHand([['a',1],['x',2],['l',3], ['e',1])
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: list (string -> int)
    """
    for pair in hand:
        for j in range(pair[1]):
            print pair[0],
    print


def dealHand(n):
    """
    Returns a new object, hand, containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.#

    Hands are represented as nested lists. The first element of each nested list is
    letter and the second element of list is the number of times the
    particular letter is repeated in that hand.#

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand=[]
    numVowels = n / 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0, len(VOWELS))]
 	bl, index = checkXInFreqList(hand, x)
        if not bl:
		    hand.append([x, 1])
        else:
        	hand[index][1] += 1

    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0, len(CONSONANTS))]
	bl, index = checkXInFreqList(hand, x)
        if not bl:
		    hand.append([x, 1])
        else:
        	hand[index][1] += 1
                
    return hand


def updateHand(hand, word):
    """
        Assumes that 'hand' has all the letters in word.
        In other words, this assumes that however many times
        a letter appears in 'word', 'hand' has at least as
        many of that letter in it.
        
        Updates the hand: uses up the letters in the given word
        and returns the new hand, without those letters in it.
        
        word: string
        hand: list (string -> int)
        returns: list (string -> int)
    """
    for letter in word:
		for i in range(len(hand)):
			if letter == hand[i][0]:
				hand[i][1] -= 1
    return hand

import copy
def isValidWord(word, hand, wordList):
    """
        Returns True if word is in the wordList and is entirely
        composed of letters in the hand. Otherwise, returns False.
        Does not mutate hand or wordList.
        
        word: string
        hand: list (string -> int)
        wordList: list of lowercase strings
    """
   
    hand2 = copy.deepcopy(hand)
    flag = 0
    for entry in (wordList):
		if word == entry:
			flag = 1
    if flag == 1:
		for letter in word:
			flag1 = 0
			for i in range(len(hand2)):
				if letter == hand2[i][0]:
					if hand2[i][1] > 0:
						flag1 = 1
						hand2[i][1] -= 1
					else: 
						return False
			if flag1 == 0:
				return False
		return True
    else:
		return False


def playHand(hand, wordList):
    """
        Allows the user to play the given hand, as follows:
        
        * The hand is displayed.
        
        * The user may input a word.
        
        * An invalid word is rejected, and a message is displayed asking
        the user to choose another word.
        
        * When a valid word is entered, it uses up letters from the hand.
        
        * After every valid word: the score for that word is displayed,
        the remaining letters in the hand are displayed, and the user
        is asked to input another word.
        
        * The sum of the word scores is displayed when the hand finishes.
        
        * The hand finishes when there are no more unused letters.
        The user can also finish playing the hand by inputing a single
        period (the string '.') instead of a word.
        
        hand: list (string -> int)
        wordList: list of lowercase strings
    """
    n = len(hand)
    fScore = 0
    word = ' '
    while word != '.':
        print "\nCurrent Hand: ",
        displayHand(hand)
        word = raw_input("\nEnter word, or a (.) to indicate that you are finished: ")
        if word == '.':
            return
        if isValidWord(word, hand, wordList) == False:
            print "\nInvalid word, please try again."
        else:
            score = getWordScore(word,n)
            fScore += score
            hand = updateHand(hand,word)
            print "This word (", word, ") scored", score, "points. Total: ", fScore, "points"
    print "\nTotal Score: ", fScore


def playGame(wordList):
    """
        Allow the user to play an arbitrary number of hands.
        
        * Asks the user to input 'n' or 'r' or 'e'.
        
        * If the user inputs 'n', let the user play a new (random) hand.
        When done playing the hand, ask the 'n' or 'e' question again.
        
        * If the user inputs 'r', let the user play the last hand again.
        
        * If the user inputs 'e', exit the game.
        
        * If the user inputs anything else, ask them again.
    """
    flag = 1
    ans = raw_input("Enter 'n' to play a new hand, 'r' to play the lasthand, 'e' to exit the game: ")
    while flag != 0:
        if ans == 'n':
            hand = dealHand(HAND_SIZE)
            hand2 = copy.deepcopy(hand)
            playHand(hand2, wordList)
            ans = raw_input("\nEnter 'n' to play new hand, 'e' to exit the game: ")
            continue
        elif ans == 'r':
            playHand(hand2)
        elif ans == 'e':
            flag = 0
        else:
            print "\nInvalid Entry. Please input again."
    print "\nExiting...\n"


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)

