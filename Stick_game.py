class Node(object):
	def __init__(self, depth, player, remaining_sticks, choices, value = 0):
		self.depth = depth
		self.player = player
		self.remaining_sticks = remaining_sticks
		self.value = value
		self.children = []
		self.CreateChildren(choices)

	def CreateChildren(self,choices):
		if self.depth >= 0:
			for i in range(1,choices + 1):
				v = self.remaining_sticks - i
				self.children.append(Node(self.depth - 1,-self.player,v,choices,self.RealVal(v)))


	def RealVal(self, value):
		if (value == 0):
			return self.player
		elif (value < 0):
			return -self.player
		return 0

##=============================
## Algorithm

def MinMax(node, depth, player):
	if (depth == 0) or (abs(node.value) == 1):
		return node.value 							#If someone won or at the end of tree, output win state
	
	i_bestValue = -player							# Else, the situation which give i_bestValue. Work that out by going down the tree

	for child in node.children:
		new_value = MinMax(child, depth - 1, -player)
		if abs(player - new_value) < abs(player - i_bestValue):
			i_bestValue = new_value
			if i_bestValue*player == 1:
				break

	return i_bestValue

##========================
## Implementation

def WinCheck(remaining_sticks, player):
	if remaining_sticks <= 0:
		if player == 1:
			if remaining_sticks == 0:
				input("YOU WIN!!!!!")
			else:
				input("TOO MANY!!!!!")
		else:
			if remaining_sticks == 0:
				input("YOU LOSE!!!!!")
			else:
				input("COMP ERROR!!!!!")

		return 0 

	return 1

if __name__ == '__main__':
	stick_total = 100
	depth = 5
	current_player = 1
	choices = 5

	while (stick_total > 0):
		print('\n%d sticks remain. How many would you like to pick up?:' %stick_total)
		while True:
			choice = int(float(input('\n Pick a number between 1 and ' + str(choices) + ':')))
			if choice in range(1,choices + 1):
				stick_total -= int(float(choice))
				break
			else:
				print('Not valid a choice. Please pick again')

		if WinCheck(stick_total, current_player):
			current_player *= -1
			node = Node(depth, current_player, stick_total, choices)
			bestChoice = -100
			i_bestValue = -current_player

			for i in range(len(node.children)):
				n_child = node.children[i]
				new_value = MinMax(n_child, depth, -current_player)
				if (abs(current_player - new_value) <= abs(current_player - i_bestValue)):
					i_bestValue = new_value
					bestChoice = i
			
			bestChoice += 1
			print('Computer chose:' + str(bestChoice) + '\tBased on value:' + str(i_bestValue))
			stick_total -= bestChoice
			WinCheck(stick_total, current_player)
			current_player *= -1