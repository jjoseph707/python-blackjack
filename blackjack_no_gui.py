"""
v3:
- add ace (value 1 or 11)
- update functions to take 'player' or 'house'
- add play again function
"""

import random

class Card:
    #Initialize cards
    def __init__(self,suit,rank):
        #suit and rank are integers
        self.suit = suit
        self.rank = rank

    #Suit/rank attibutes
    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = ['Ace','2', '3', '4', '5', '6', '7',
    '8', '9', '10', 'Jack', 'Queen', 'King']

    #Handles comparison of Card(s) based on RANK ONLY
    # def __lt__(self,other):
        # if self.rank < other.rank: return 1
        # if self.rank == other.rank: return 0
        # if self.rank > other.rank: return -1

    #Handles string representation of Card
    def __str__(self):
        return f'{Card.rank_names[self.rank]} of {Card.suit_names[self.suit]}'

class Deck:
    #Initialize 52 card deck
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(13):
                self.cards.append(Card(suit,rank))

    #Deck printing
    def __str__(self):
        x = []
        for card in self.cards:
            x.append(str(card))
        return '\n'.join(x)

    #Remove/return top card in deck
    def take_top_card(self):
        return self.cards.pop(0)

    #Add specified card to bottom of deck
    def add_card(self,card):
        self.cards.append(card)

    #Shuffle deck(method)
    def shuffle_deck(self):
        return random.shuffle(self.cards)

    #Shuffled deck (property)
    # @property
    # def shuffled_deck(self):
    #     return random.shuffle(self.cards)

    #Sort deck by rank
    def sort_deck(self):
        return self.cards.sort()

    #Give x cards to hand
    def give_cards(self,amnt,hand):
        for x in range(amnt):
            hand.add_card(self.take_top_card())

    #Deal out to x new hands
    def deal_hands(self,cards,hands):
        new_hands = []
        for x in range(hands):
            new_hands.append(Hand(f'Hand {x}'))
        for x in new_hands:
            self.give_cards(cards,x)
        return new_hands

class Hand(Deck):
    #Initialize empty hand
    def __init__(self,label):
        self.cards = []
        self.label = label

class Blackjack():
    #Initialize deck
    def __init__(self):
        #Deck
        self.deck = Deck()
        self.deck.shuffle_deck()
        #Player
        self.hand = Hand('Player hand')
        self.score_ace_1 = 0
        self.score_ace_2 = 0
        self.card_count = 2
        #House
        self.house_hand = Hand('House hand')
        self.house_score_ace_1 = 0
        self.house_score_ace_2 = 0
        self.house_card_count = 2
        #Check for player bust/blackjack
        self.player_status = ''

    #card scores (ACE = 1)
    score_list_1 = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:10,11:10,12:10}

    #card scores (ACE = 11)
    score_list_2 = {0:11,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:10,11:10,12:10}

    #Hand builder
    def build_hand(self,h):
        if h == 'player':
            self.deck.give_cards(self.card_count,self.hand)
        if h == 'house':
            self.deck.give_cards(self.house_card_count,self.house_hand)

    #Check for ace
    def check_ace(self,h):
        if h == 'player':
            for card in self.hand.cards:
                if card.rank == 0:
                    return True
            return False
        if h == 'house':
            for card in self.house_hand.cards:
                if card.rank == 0:
                    return True
            return False

    #Check for initial blackjack
    def check_inital_blackjack(self,h):
        self.score_counter_1(h)
        self.score_counter_2(h)
        if h == 'player':
            if self.score_ace_1 == 21 or self.score_ace_2 == 21:
                return True
        if h == 'house':
            if self.house_score_ace_1 == 21 or self.house_score_ace_2 == 21:
                return True

    #Check for 21
    def check_blackjack(self,h):
        self.score_counter_1(h)
        self.score_counter_2(h)
        if h == 'player':
            if self.score_ace_1 == 21 or self.score_ace_2 == 21:
                return True
        if h == 'house':
            if self.house_score_ace_1 == 21 or self.house_score_ace_2 == 21:
                return True

    #Check for bust
    def check_bust(self,h):
        self.score_counter_1(h)
        if h == 'player':
            if self.score_ace_1 > 21:
                return True
        if h == 'house':
            if self.house_score_ace_1 > 21:
                return True

    #Add card to hand
    def hit(self,h):
        if h == 'player':
            self.card_count+=1
            self.deck.give_cards(1,self.hand)
        if h == 'house':
            self.house_card_count+=1
            self.deck.give_cards(1,self.house_hand)

    #Count score (ACE = 1)
    def score_counter_1(self,h):
        if h == 'player':
            self.score_ace_1=0
            for x in range(self.card_count):
                add = Blackjack.score_list_1[self.hand.cards[x].rank]
                self.score_ace_1+=add
                #return self.score here so value isnt NoneType
            return self.score_ace_1
        if h == 'house':
            self.house_score_ace_1=0
            for x in range(self.house_card_count):
                add = Blackjack.score_list_1[self.house_hand.cards[x].rank]
                self.house_score_ace_1+=add
                #return self.score here so value isnt NoneType
            return self.house_score_ace_1

    #Count score (ACE = 11)
    def score_counter_2(self,h):
        if h == 'player':
            self.score_ace_2=0
            for x in range(self.card_count):
                add = Blackjack.score_list_2[self.hand.cards[x].rank]
                self.score_ace_2+=add
                #return self.score here so value isnt NoneType
            return self.score_ace_2
        if h == 'house':
            self.house_score_ace_2=0
            for x in range(self.house_card_count):
                add = Blackjack.score_list_2[self.house_hand.cards[x].rank]
                self.house_score_ace_2+=add
                #return self.score here so value isnt NoneType
            return self.house_score_ace_2

    #Player turn
    def player_turn(self):
        #Check for initial blackjack
        if self.check_inital_blackjack('player'):
            print('------HAND------')
            print(self.hand)
            print('----------------')
            print('Blackjack!...WIN')
            self.player_status = 'blackjack'
            return
        while True:
            print('------HAND------')
            print(self.hand)
            print('----------------')
            #Checks for blackjack
            # if self.check_ace():
            if self.check_blackjack('player'):
                break
            #Checks for bust
            if self.check_bust('player'):
                print('bust...LOSS')
                self.player_status = 'bust'
                break
            choice = input('stand or hit?: ')
            if choice == 'hit':
                self.hit('player')
            if choice == 'stand':
                self.score_counter_1('player')
                self.score_counter_2('player')
                break

    #House turn loop
    def house_turn(self):
        #Exit if player gets blackjack/bust
        if self.player_status in ['blackjack','bust']:
            return
        #Exit with loss if house gets immediate blackjack
        if self.check_inital_blackjack('house'):
            print('---HOUSE HAND---')
            print(self.house_hand)
            print('----------------')
            print('House blackjack....LOSS')
            # self.player_status = 'house blackjack'
            return
        while self.house_score_ace_1 < 17:
            self.house_card_count+=1
            self.deck.give_cards(1,self.house_hand)
            self.score_counter_1('house')
            self.score_counter_2('house')
        #house bust - win
        if self.house_score_ace_1 > 21 and self.house_score_ace_2 >21:
            print('---HOUSE HAND---')
            print(self.house_hand)
            print('----------------')
            print('House bust...WIN')
            return
        #greater score than house - win
        if (self.house_score_ace_1 < self.score_ace_1) or (self.house_score_ace_2 < self.score_ace_1) or (self.house_score_ace_1 < self.score_ace_2) or (self.house_score_ace_2 < self.score_ace_2):
            print('---HOUSE HAND---')
            print(self.house_hand)
            print('----------------')
            print('House beat...WIN')
            return
        #smaller score than house - lose
        elif (self.house_score_ace_1 > self.score_ace_1) or (self.house_score_ace_2 > self.score_ace_1) or (self.house_score_ace_1 > self.score_ace_2) or (self.house_score_ace_2 > self.score_ace_2):
            print('---HOUSE HAND---')
            print(self.house_hand)
            print('----------------')
            print('Player beat...LOSS')
            return
        #else tie
        else:
            print('---HOUSE HAND---')
            print(self.house_hand)
            print('----------------')
            print('Equal hands...TIE')
            return

    #Play again
    def play_again(self):
        prompt = input('Play again?: ')
        if prompt == 'yes':
            print('---------NEW GAME----------')
            Blackjack.play_blackjack()

    def play_blackjack():
        #Initialize game
        game1 = Blackjack()
        #Build initial hand
        game1.build_hand('player')
        #Player turn
        game1.player_turn()
        # #Build house hand
        game1.build_hand('house')
        #House turn
        game1.house_turn()
        #Play again?
        game1.play_again()

Blackjack.play_blackjack()
