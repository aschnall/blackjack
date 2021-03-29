import random
import time
from pip._vendor.distlib.compat import raw_input

values = [11, 2, 3, 4, 5, 6, 7,  8, 9, 10, 10, 10, 10]
suits = ['clubs', 'diamonds', 'spades', 'hearts']
names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = []
money = 50
play = False
player_cards = []
dealer_cards = []
player_turn = True
dealer_turn = False
first_turn = True
player_has_ace = False
dealer_has_ace = False
question = 'Would you like to hit?'
question1 = 'Please confirm your $10 bet to play'
question2 = 'Do you want to play another hand?'

def initialize_deck():
    for suit in suits:
        for i in range(0, 13):
            deck.append({'suit': suit, 'value': values[i], 'name': names[i]})
    shuffle()

def shuffle():
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i - 1)
        hold_i = deck[i]
        hold_j = deck[j]
        deck[j] = hold_i
        deck[i] = hold_j
    deal()

def deal():
    #empty out player and dealer cards when moving to a new hand
    if len(player_cards) != 0:
        for i in range(0, len(player_cards)):
            player_cards.pop(0)

    if len(dealer_cards) != 0:
        for i in range(0, len(dealer_cards)):
            dealer_cards.pop(0)

    #deal the player 2 cards
    for i in range(0, 2):
        player_cards.append(deck[i])

    #remove the 2 cards dealt from the deck
    for j in range(0, 2):
        deck.pop(0)

    #deal the dealer 2 cards
    for k in range(0, 2):
        dealer_cards.append(deck[k])

    #remove the 2 cards dealt from the deck
    for n in range(0, 2):
        deck.pop(0)

    calculate_score()

def calculate_score():

    global player_score
    global dealer_score
    global player_has_ace
    global dealer_has_ace
    player_score = 0
    dealer_score = 0

    for card in player_cards:
        if card['name'] == 'Ace':
            player_has_ace = True
        player_score += card['value']

    #re-calculate player score if user has an ace and value should be 1 rather than 11
    if player_has_ace and player_score > 21:
        player_score = 0
        for card in player_cards:
            if card['name'] == 'Ace':
                card['value'] = 1
            player_score += card['value']

    for card in dealer_cards:
        if card['name'] == 'Ace':
            dealer_has_ace = True
        dealer_score += card['value']

    # re-calculate dealer score if user has an ace and value should be 1 rather than 11
    if dealer_has_ace and dealer_score > 21:
        dealer_score = 0
        for card in dealer_cards:
            if card['name'] == 'Ace':
                card['value'] = 1
            dealer_score += card['value']

def main():
    global play
    global money
    global first_turn
    if first_turn:
        print("Your starting balance is $" + str(money))
        player_reply = str(raw_input(question1 + ' (y/n): ')).lower().strip()
        if player_reply[0] == 'y':
            play = True
            first_turn = False
        elif player_reply[0] == 'n':
            print("Goodbye.")
            quit()
    while play:
        print("Shuffling and dealing cards. One moment please.\n")
        initialize_deck()
        time.sleep(2)
        print("You first card is: {} of {}".format(player_cards[0]['name'], player_cards[0]['suit']))
        time.sleep(1.5)
        print("You second card is: {} of {}".format(player_cards[1]['name'], player_cards[1]['suit']))
        time.sleep(1.5)
        print("The dealer is showing: {} of {}\n".format(dealer_cards[0]['name'], dealer_cards[0]['suit']))
        global player_turn
        global dealer_turn
        while player_turn:
            player_reply = str(raw_input(question + ' (y/n): ')).lower().strip()
            if player_reply[0] == 'y':
                player_cards.append(deck[0])
                deck.pop(0)
                calculate_score()
                print("You received a {} of {}\n".format(player_cards[len(player_cards) - 1]['name'],
                                                       player_cards[len(player_cards) - 1]['suit']))
                if player_score > 21:
                    print('You busted')
                    money -= 10
                    player_turn = False

            if player_reply[0] == 'n':
                player_turn = False
                dealer_turn = True

        print("Your score is:", player_score, "\n")
        if player_score <= 21:
            print("Dealer flips over: {} of {}".format(dealer_cards[1]['name'], dealer_cards[1]['suit']))
        time.sleep(2)
        while dealer_turn:
            if player_score < dealer_score <= 21:
                time.sleep(2)
                print("Dealer has:", dealer_score)
                time.sleep(1.5)
                print("Dealer wins\n")
                money -= 10
                break
            elif dealer_score < player_score <=21:
                time.sleep(2)
                print("Dealer has:", dealer_score)
                time.sleep(1)
                print("Dealer hits")
                dealer_cards.append(deck[0])
                deck.pop(0)
                calculate_score()
                time.sleep(2)
                print("Dealer received a {} of {}\n".format(dealer_cards[len(dealer_cards) - 1]['name'],
                                                       dealer_cards[len(dealer_cards) - 1]['suit']))
            elif dealer_score > 21:
                time.sleep(2)
                print("Dealer has:", dealer_score)
                time.sleep(1.5)
                print("Dealer busts. You Win!\n")
                money += 10
                break
            elif dealer_score == player_score and player_score < 21:
                time.sleep(2)
                print("Dealer has:", dealer_score)
                time.sleep(1.5)
                print("It's a push\n")
                break
        play = False
        time.sleep(1.5)
        print("You now have a balance of $" + str(money))
    if money > 0:
        player_reply = str(raw_input(question2 + ' (y/n): ')).lower().strip()
        if player_reply[0] == 'y':
            play = True
            player_turn = True
            dealer_turn = False
            main()
        elif player_reply[0] == 'n':
            print('Thanks for playing! Goodbye.')
    if money == 0:
        print('You have no more money. Goodbye.')

if __name__ == "__main__":
    main()


