from operator import attrgetter

class Game:
	def __init__(self, num_players):
		self.num_players = num_players
		self.hands = []
		self.top_hands = []
		self.hand_table = {}
		self.populate_table();

	def set_hand(self, player, hand):
		''' assigns hand to a player '''
		assert player == hand.player
		self.hands.append(hand)
		self.hand_table[player] = hand

	def populate_table(self):
		''' initializes the hand table'''
		for i in range(self.num_players):
			self.hand_table[i] = {}

	def get_hand(self, player):
		''' getter method for a player's hand'''
		return self.hand_table[player]

	def eval_sort_hands(self):
		''' ranks and sorts the hands in the game'''
		for hand in self.hands:
			hand.rank_hand()
		self.hands.sort(key=attrgetter('hand_rank'))

	def eval_top_hands(self):
		''' acquiring the potential winning hand(s) '''
		self.eval_sort_hands()
		hand_set = set()
	 	for hand in self.hands:
			hand_set.add(hand.hand_rank)
			if len(hand_set) > 1:
				break
			else:
				self.top_hands.append(hand)

	def eval_winner(self):
		'''
		evaluates the potential winning hands
		and returns a list of winning hand(s)
		'''
		self.eval_top_hands()
		assert len(self.top_hands) > 0
		if len(self.top_hands)>1:
			# there is a tie among the hands
			rank = self.top_hands[0].hand_rank
			if rank == 1:
				# straight flush
				return self.solve_straight_flush()
			elif rank == 2:
				# three of a kind
				return self.solve_three_of_a_kind()
			elif rank == 3:
				# straight
				return self.solve_straight()
			elif rank == 4:
				# flush
				return self.solve_flush()
			elif rank == 5:
				# pair
				return self.solve_pairs()
			elif rank == 6:
				# high card
				return self.solve_high_card()
			else:
				assert False, "No way, Jose! Hand rank is invalid"
		else:
			return [self.top_hands[0]]


	def solve_generic(self, attr, collection):
		''' 
		sort in terms of attribute in a given collection
		returns a sorted list
		'''
                collection.sort(key=attrgetter(attr), reverse=True)
                winners = []
                top_set = set()
                for hand in collection:
                        top_set.add(getattr(hand, attr))
                        if len(top_set) > 1:
                                break
                        else:
                                winners.append(hand)
                return winners
					
	def solve_straight_flush(self):
		''' 
		solves a straight flush tie
		returns a list of winning hand(s)
		'''
		return self.solve_generic('high_card_rank', self.top_hands)

	def solve_three_of_a_kind(self):
		'''
		solves a three of a kind tie
		return a list of winning hands(s)
		'''
		return self.solve_generic('high_card_rank', self.top_hands)

	def solve_straight(self):
		'''
		solves a straight tie
		returns a list of winning hand(s)
		'''
		return self.solve_generic('high_card_rank', self.top_hands)
	
	def solve_flush(self):
		'''
		solves a flush tie
		returns a list of winning hand(s)
		'''
		return self.solve_high_card()

	def solve_pairs(self):
		'''
		solves a pair tie
		returns a list of winning hand(s)
		'''
		# sort in terms of pair_rank
		winners = self.solve_generic('pair_rank', self.top_hands)

		if len(winners) > 1:
			# sort and compare the odd card
			return self.solve_generic('odd_card_rank', winners)
		return winners
	
	def solve_high_card(self):
		'''
		solves a high card tie
		returns a list of winning hand(s)
		'''
		first_round = self.solve_generic('high_card_rank', self.top_hands)
		# high card tie 
		if len(first_round) > 1:
			second_round = self.solve_generic('mid_card_rank', first_round)
			# mid card tie
			if len(second_round) >1:
				return self.solve_generic('low_card_rank', second_round)
			return second_round
		return first_round
