import numpy as np 

class Node(object):
	def __init__(self, depth, player, game, value = 0):
		self.depth = depth
		self.player = player
		self.game = game
		self.value = value
		self.children = []
		self.CreateChildren(player,game)

	def CreateChildren(self,player,game):
		if self.depth >= 0:
			for i in range(len(np.where(self.game == 0)[0])):
				move = [np.where(self.game == 0)[0][i],np.where(self.game == 0)[1][i]]
				#print('player1: ' + str(self.player))
				matrix = np.zeros([3,3])
				matrix[move[0],move[1]] = self.player
				v = self.game + matrix
				#print(i)
				#print('player2: ' + str(self.player))
				#input('v: ' + str(v))
				self.children.append(Node(self.depth - 1,-self.player,v,self.RealVal(v)))


	def RealVal(self,v):
		value = 0

		if np.all(v[[0,0,0],[0,1,2]] == 1) or np.all(v[[1,1,1],[0,1,2]] == 1) or np.all(v[[2,2,2],[0,1,2]] == 1): 	# 1 Rows
			value = self.depth + 1

		elif np.all(v[[0,1,2],[0,0,0]] == 1) or np.all(v[[0,1,2],[1,1,1]] == 1) or np.all(v[[0,1,2],[2,2,2]] == 1):			# 1 Collums
			value = self.depth + 1

		elif np.all(v[[0,1,2],[0,1,2]] == 1) or np.all(v[[0,1,2],[2,1,0]] == 1):			# 1 Diagonals
			value = self.depth + 1

		if np.all(v[[0,0,0],[0,1,2]] == -1) or np.all(v[[1,1,1],[0,1,2]] == -1) or np.all(v[[2,2,2],[0,1,2]] == -1): 	# -1 Rows
			value = -(self.depth + 1)

		elif np.all(v[[0,1,2],[0,0,0]] == -1) or np.all(v[[0,1,2],[1,1,1]] == -1) or np.all(v[[0,1,2],[2,2,2]] == -1):			# -1 Collums
			value = -(self.depth + 1)

		elif np.all(v[[0,1,2],[0,1,2]] == -1) or np.all(v[[0,1,2],[2,1,0]] == -1):			# -1 Diagonals
			value = -(self.depth + 1)

		return(value)

##=============================
## Algorithm

def MinMax(node, depth, player, alpha, beta):
	if ((depth == 0) or (abs(WinCheck(node.game)) == 1)):
		return node.value 						#If someone won or at the end of tree, output that state
	
	best_value = -10*player						# Else, the situation which give best_value. Work that out by going down the tree
	for child in node.children:
		if player == 1:
			new_value = -10
			new_value = max(new_value, MinMax(child, depth - 1, -player, alpha, beta))
			alpha = max(alpha, new_value)
		else:
			new_value = 10
			new_value = min(new_value, MinMax(child, depth - 1, -player, alpha, beta))
			beta = min(beta, new_value)	
		if alpha >= beta:
			return new_value


		if abs(10*player - new_value) < abs(10*player - best_value):
			best_value = new_value
	#print('Old game: ' + str(old_game))
	#input('New game: ' + str(new_game))		


	return best_value

##========================
## Implementation

def WinCheck(game):
	win = 0

	if np.all(game[[0,0,0],[0,1,2]] == 1) or np.all(game[[1,1,1],[0,1,2]] == 1) or np.all(game[[2,2,2],[0,1,2]] == 1): 	# 1 Rows
		win = 1

	elif np.all(game[[0,1,2],[0,0,0]] == 1) or np.all(game[[0,1,2],[1,1,1]] == 1) or np.all(game[[0,1,2],[2,2,2]] == 1):			# 1 Collums
		win = 1

	elif np.all(game[[0,1,2],[0,1,2]] == 1) or np.all(game[[0,1,2],[2,1,0]] == 1):			# 1 Diagonals
		win = 1

	if np.all(game[[0,0,0],[0,1,2]] == -1) or np.all(game[[1,1,1],[0,1,2]] == -1) or np.all(game[[2,2,2],[0,1,2]] == -1): 	# -1 Rows
		win = -1

	elif np.all(game[[0,1,2],[0,0,0]] == -1) or np.all(game[[0,1,2],[1,1,1]] == -1) or np.all(game[[0,1,2],[2,2,2]] == -1):			# -1 Collums
		win = -1

	elif np.all(game[[0,1,2],[0,1,2]] == -1) or np.all(game[[0,1,2],[2,1,0]] == -1):			# -1 Diagonals
		win = -1

	return(win)


if __name__ == '__main__':
	depth = 5
	current_player = 1
	game = np.zeros([3,3])
	turn = 1
	win = 0
	alpha = -10
	beta = 10

	while ((turn < 10) & (win == 0)):
		moves = range(len(np.where(game == 0)[0]))
		print('\nThis is turn', turn)
		print(game)
		while True:
			move = int(input('Pick a move:'))
			turn += 1
			if move in moves:
				break
			else:
				print('Not a valid move, try again:')

		move = [np.where(game == 0)[0][move],np.where(game == 0)[1][move]]

		game[move[0],move[1]] = current_player

		win = WinCheck(game)

		if ((win == 0) & (turn < 10)):
			current_player *= -1
			node = Node(depth, current_player, game)
			best_value = -current_player
			best_choice = 0
			for i in range(len(node.children)):
				n_child = node.children[i]
				new_value = MinMax(n_child, depth, -current_player, -10, 10)
				if (abs(10*current_player - new_value) <= abs(10*current_player - best_value)):
					best_value = new_value
					best_choice = i
			
			n_child = node.children[best_choice]
			game = n_child.game
			best_choice += 1
			print('Computer chose:' + str(game) + '\tBased on value:' + str(best_value))
			turn += 1
			win = WinCheck(game)
		
		if win == 1:
			input('You won!!')
		elif win == -1:
			input('You lost...')
		elif turn == 10:
			input('Draw.')
		else:
			current_player *= -1