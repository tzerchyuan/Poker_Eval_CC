from operator import attrgetter

class Hand:
	def __init__(self, player_id):
		self.cards = []
		self.player = player_id
		self.hand_rank = None

		self.high_card_rank = None
		self.mid_card_rank = None
		self.low_card_rank = None

		self.pair_rank = None
		self.odd_card_rank = None
	
	def add_card(self, card):
		''' adds cards to the hand '''
		self.cards.append(card)
		self.sort_rank

	def sort_rank(self):
		''' sorts the card in decreasing rank order '''
		self.cards.sort(key=attrgetter('rank'), reverse=True)
		self.high_card_rank= self.cards[0].rank

	def isFlush(self):
		''' checks if hand has a flush '''
		suit_set = set(card.suit for card in self.cards)
		if len(suit_set)==1:
			return True
		return False

	def isStraight(self):
		''' checks if hand has a straight '''
		rank_set = set(card.rank for card in self.cards)
		rank_range = max(rank_set) - min(rank_set) + 1
		if (rank_range == len(self.cards) and len(rank_set) == len(self.cards)):
			return True
		if 14 in rank_set:
			# if there is an Ace
			if self.isAceStraight(rank_set):
				self.high_card_rank = 3
				return True
		return False

	def isAceStraight(self, rank_set):
		''' checks if hand has a straight that starts with an ace '''
              	ace_set = set([14,3,2])
		return ace_set.issubset(rank_set) and len(ace_set) == len(rank_set)

	def isStraightFlush(self):
		''' checks if hand has a straight flush '''
		if (self.isStraight() and self.isFlush()):
			return True
		return False

	def isPair(self):
		''' 
		checks if hand has a pair
		if true, sets pair_rank and odd_card_rank
		'''
		rank_set = set(card.rank for card in self.cards)
		if len(rank_set) == 2:
			for i in range(len(self.cards)):
				rank_list = [card.rank for card in self.cards]
				assert(len(rank_list) == 3)
				rank_count = rank_list.count(rank_list[i])
				if rank_count == 2:
					self.pair_rank = self.cards[i].rank
				elif rank_count == 1:
					self.odd_card_rank = self.cards[i].rank
				else:
					assert(False, "Something is wrong with pairs!")

			assert(self.pair_rank != None)
			assert(self.odd_card_rank != None)
			return True
		return False

	def isThreeOfAKind(self):
		''' checks if hand has a three of a kind '''
		rank_set = set(card.rank for card in self.cards)
		if len(rank_set) == 1:
			return True
		return False

	def rank_hand(self):
		'''
		ranks hand and sets hand_rank attribute
		to approproate values
		'''
		self.sort_rank()
		if self.isStraightFlush():
			self.hand_rank = 1
			return

		if self.isThreeOfAKind():
			self.hand_rank = 2
			return

		if self.isStraight():
			self.hand_rank = 3
			return

		if self.isFlush():
			self.hand_rank = 4
			return

		if self.isPair():
			self.hand_rank = 5
			return

		# High card hand
		self.hand_rank = 6

		# setting mid and low card ranks
		self.mid_card_rank = self.cards[1].rank
		self.low_card_rank = self.cards[2].rank
		assert(self.mid_card_rank > self.low_card_rank)
