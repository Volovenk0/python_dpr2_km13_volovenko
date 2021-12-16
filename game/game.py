import math
import random
import string
from functools import reduce

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def load_words():
    
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def get_word_score(word, n):
    score = HAND_SIZE*len(word) - 3*(n-len(word))
    return reduce(lambda x,y:x+SCRABBLE_LETTER_VALUES[y],word.lower(),0)*(score if score>=1 else 1)

def display_hand(hand):
    print("Current hand: ", end=' ')
    for letter in hand.keys():
        
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()
    
def deal_hand(n):
    hand={}
    num_vowels = int(math.ceil(n / 3))
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    hand['*']=1
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    return hand

def update_hand(hand, word):
    update_hand_dict = hand.copy()
    for letter in word.lower():
        if letter in update_hand_dict:
            if update_hand_dict[letter]>1:
                update_hand_dict[letter] -=1
            else:
                update_hand_dict.pop(letter)
    return update_hand_dict

def is_valid_word(word, hand, word_list):
    word_find=False
    for elem in word_list:
        if len(elem)!=len(word):
            continue
        else:
            find=True
            replacement=False
            for i in range(len(elem)):
                if (elem[i]==word.lower()[i] or (elem[i] in VOWELS) and replacement==False and word.lower()[i]=="*")==False:
                    find=False
                    break
                elif  (elem[i] in VOWELS) and word.lower()[i]=="*":
                    replacement=True
        if find:
           word_find=True
           break 
    if word_find:
        word_dict=get_frequency_dict(word.lower())
        for key in word_dict:
            if (key in hand)==False:
                return False
            elif word_dict[key]>hand[key]:
                return False
    else:
        return False
    return True

def calculate_handlen(hand):
    return reduce(lambda x,y:x+hand[y],hand.keys(),0)

def play_hand(hand, word_list):
    play=True
    while play==True:
        left_hand = hand.copy()
        total_scope=0
        while calculate_handlen(left_hand)>0:
             display_hand(left_hand)
             input_word = input('Enter word, or “!!” to indicate that you are finished: ')
             if input_word=="!!":
                 break
             elif is_valid_word(input_word,hand,word_list):
                 current_points = get_word_score(input_word, len(input_word))
                 total_scope+=current_points
                 print(input_word+" earned "+str(current_points)+ " points. Total: "+str(total_scope)+" points")
                 left_hand = update_hand(left_hand, input_word)
             else:
                 print('Word is not valid')
                 left_hand = update_hand(left_hand, input_word)
                 
        if calculate_handlen(left_hand)==0:
            print('Ran out of letters. Total score: '+str(total_scope)+' points')
        else:
            print("Total score for this hand: "+ str(total_scope))
        replay=input("Would you like to replay the hand? ")
        if replay!="yes":
            play=False 
    return total_scope

def substitute_hand(hand, letter):
    letter_for_change=''  
    if letter in VOWELS:
        letter_in_hand = True
        while letter_in_hand:
            letter_for_change = VOWELS[random.randint(0,len(VOWELS)-1)]
            if (letter_for_change in hand)==False:
                letter_in_hand = False
    else:
        letter_in_hand = True
        while letter_in_hand:
            letter_for_change = CONSONANTS[random.randint(0,len(CONSONANTS)-1)]
            if (letter_for_change in hand)==False:
                letter_in_hand = False
    update_hand_dict = hand.copy()
    value = hand[letter]
    update_hand_dict.pop(letter)
    update_hand_dict[letter_for_change] = value        
    return update_hand_dict              

def play_game(word_list):
    total_scope=0
    number_hands=0
    valid_number=True
    while valid_number: 
        try: 
            number_hands = int(input("Enter total number of hands: "))
            valid_number = False
        except:
            print("You've entered not number!")
    for i in range(number_hands):
        current_hand = deal_hand(HAND_SIZE)
        display_hand(current_hand)
        subs = input ("Would you like to substitute a letter? ")
        if subs == 'yes':
            letter = input('Which letter would you like to replace: ')
            current_hand = substitute_hand(current_hand, letter)
        total_scope+=play_hand(current_hand, word_list)
    print("Total score over all hands: "+ str(total_scope))
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)