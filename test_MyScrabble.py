from MyScrabble import *
import copy
#
# Test code
#

def test_dealHand():
    """
    Unit test for dealHand.
    """
    
    # (A)
    # Basic test, see if the right kind of nested list is
    # being returned.
    hand = dealHand(HAND_SIZE)
    if not type(hand) is list:
        print "FAILURE: test_dealHand()"
        print "\tUnexpected return type:", type(hand)
        
        return # exit function

    num = 0
    for k in hand:
        if (not type(k[0]) is str) or (not type(k[1]) is int):
            print "FAILURE: test_dealHand()"
            print "\tUnexpected type of nested list: string -> int expected, but was", type(k[0]), "->", type(k[1])

            return # exit function
        elif not k[0] in "abcdefghijklmnopqrstuvwxyz":
            print "FAILURE: test_dealHand()"
            print "\tnested list first element are not lowercase letters."

            return # exit function
        else:
            num += k[1]
            
    if num != HAND_SIZE:
            print "FAILURE: test_dealHand()"
            print "\tdealHand() returned more letters than it was asked to."
            print "\tAsked for a hand of size", HAND_SIZE, "but it returned a hand of size", num

            return # exit function
        
    # (B)
    # Tests randomness..
    repeats = 0
    hand1 = dealHand(HAND_SIZE)
    for i in range(20):                
         hand2 = dealHand(HAND_SIZE)
         if hand1 == hand2:
            repeats += 1
         hand1 = hand2
        
    if repeats > 10:
        print "FAILURE: test_dealHand()"
        print "\tSame hand returned", repeats, "times by dealHand(). This is HIGHLY unlikely."
        print "\tIs the dealHand implementation really using random numbers?"

        return # exit function
    
    print "SUCCESS: test_dealHand()"

def test_getWordScore():
    """
    Unit test for getWordScore
    """
    failure = False
    # dictionary of words and scores
    words = {("", 7):0, ("it", 7):4, ("was", 7):18, ("scored", 7):54, ("waybill", 7):155, ("outgnaw", 7):127, ("outgnawn", 8):146}
    for (word, n) in words.keys():
        score = getWordScore(word, n)
        if score != words[(word, n)]:
            print "FAILURE: test_getWordScore()"
            print "\tExpected", words[(word, n)], "points but got '" + str(score) + "' for word '" + word + "', n=" + str(n)
            failure = True
    if not failure:
        print "SUCCESS: test_getWordScore()"



def test_updateHand():
    """
    Unit test for updateHand
    """
    # test 1
    hand1 = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
    word = "quail"
    hand = []
    for j in hand1.items():
        hand.append(list(j))

    hand2 = updateHand(copy.deepcopy(hand), word)
    expectedHand1 = [['l',1],['m',1]]
    expectedHand2 = [['a',0],['i',0],['l',1],['m',1],['q',0],['u',0]]
    if hand2.sort() != expectedHand1.sort() and hand2.sort() != expectedHand2.sort():
        print "FAILURE: test_updateHand('"+ word +"', " + str(hand) + ")"
        print "\tReturned: ", hand2, "-- but expected:", expectedHand1, "or", expectedHand2

        return # exit function
        
    # test 2
    hand1 = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    word = "evil"
    hand = []
    for j in hand1.items():
        hand.append(list(j))

    hand2 = updateHand(copy.deepcopy(hand), word)
    expectedHand1 = [['l',1],['n',1],['v',1]]
    expectedHand2 = [['e',0],['i',0],['l',1],['n',1],['v',1]]
    if hand2.sort() != expectedHand1.sort() and hand2.sort() != expectedHand2.sort():
        print "FAILURE: test_updateHand('"+ word +"', " + str(hand) + ")"        
        print "\tReturned: ", hand2, "-- but expected:", expectedHand1, "or", expectedHand2

        return # exit function

    # test 3
    hand1 = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    word = "hello"
    hand = []
    for j in hand1.items():
        hand.append(list(j))

    hand2 = updateHand(copy.deepcopy(hand), word)
    expectedHand1 = []
    expectedHand2 = [['h',0],['e',0],['l',0],['o',0]]
    if hand2.sort() != expectedHand1.sort() and hand2.sort() != expectedHand2.sort():
        print "FAILURE: test_updateHand('"+ word +"', " + str(hand) + ")"                
        print "\tReturned: ", hand2, "-- but expected:", expectedHand1, "or", expectedHand2
        
        return # exit function

    print "SUCCESS: test_updateHand()"

def test_isValidWord(word_list):
    """
    Unit test for isValidWord
    """
    failure=False
    # test 1
    word = "hello"
    hand = getFrequencyList(word)

    if not isValidWord(word, hand, word_list):
        print "FAILURE: test_isValidWord()"
        print "\tExpected True, but got False for word: '" + word + "' and hand:", hand

        failure = True

    # test 2
    hand = [['r',1],['a',3],['p',2],['e',1],['t',1],['u',1]]
    word = "rapture"

    if  isValidWord(word, hand, word_list):
        print "FAILURE: test_isValidWord()"
        print "\tExpected False, but got True for word: '" + word + "' and hand:", hand

        failure = True        

    # test 3
    hand = [['n',1],['h',1],['o',1],['y',1],['d',1],['w',1],['e',2]]
    word = "honey"

    if  not isValidWord(word, hand, word_list):
        print "FAILURE: test_isValidWord()"
        print "\tExpected True, but got False for word: '"+ word +"' and hand:", hand

        failure = True                        

    # test 4
    hand = [['r',1],['a',3],['p',2],['t',1],['u',2]]
    word = "honey"

    if  isValidWord(word, hand, word_list):
        print "FAILURE: test_isValidWord()"
        print "\tExpected False, but got True for word: '" + word + "' and hand:", hand
        
        failure = True

    # test 5
    hand = [['e',1],['v',2],['n',1],['i',1],['l',2]]
    word = "evil"
    
    if  not isValidWord(word, hand, word_list):
        print "FAILURE: test_isValidWord()"
        print "\tExpected True, but got False for word: '" + word + "' and hand:", hand
       
        failure = True
        
    # test 6
    word = "even"

    if  isValidWord(word, hand, word_list):
        print "FAILURE: test_isValidWord()"
        print "\tExpected False, but got True for word: '" + word + "' and hand:", hand
        print "\t(If this is the only failure, make sure isValidWord() isn't mutating its inputs)"        
        
        failure = True        

    if not failure:
        print "SUCCESS: test_isValidWord()"


word_list = load_words()
print "----------------------------------------------------------------------"
print "Testing getWordScore..."
test_getWordScore()
print "----------------------------------------------------------------------"
print "Testing updateHand..."
test_updateHand()
print "----------------------------------------------------------------------"
print "Testing isValidWord..."
test_isValidWord(word_list)
print "----------------------------------------------------------------------"
print "All done!"
