import sys
from operator import attrgetter
from game import Game
from hand import Hand
from card import Card

rank_conversion = {'T':10, 'J':11, 'Q':12, 'K':13, "A":14}

def setup():
	num_players = sys.stdin.readline()
	game = Game(int(num_players))

	for line in sys.stdin:
		hand_elems = line.split()
		player  = int(hand_elems[0])
		hand = Hand(player)
		for i in range(1, len(hand_elems)):
			# creating the hand
			if rank_conversion.get(hand_elems[i][0]):
				rank = rank_conversion.get(hand_elems[i][0])
			else:
				rank = int(hand_elems[i][0])
			suit = hand_elems[i][1]
			card = Card(rank, suit)	
			hand.add_card(card)
		game.set_hand(player, hand)
	return game

game = setup()

def output(game):
	winners = game.eval_winner()
	winners_sorted =  sorted(winners, key=attrgetter('player'))
	output = ""
	for hand in winners_sorted:
		output += str(hand.player) + " "
	return output

if __name__ == '__main__':
  print output(game)
