# Chess
# Built on Nov. 27th, 2019 on a flight to Tokyo.
# hdominic@seas.upenn.edu

"""
8   -  -  -  -  -  -  -  -

7   -  -  -  -  -  -  -  -

6   -  -  -  -  -  -  -  -

5   -  -  -  -  -  -  -  -

4   -  -  -  -  -  -  -  -

3   -  -  -  -  -  -  -  -

2   -  -  -  -  -  -  -  -

1   -  -  -  -  -  -  -  -

    A  B  C  D  E  F  G  H
"""

"""
The game flow is as follows:
1. A user invokes the program and types in the name for each player.
2. Player 1 is always white, so they go first.
3. They choose the piece they'd like to move: ex "A2" moves the leftmost white pawn.
4. All possible moves from the selected piece are computed. If no possible moves
	exist for that piece, repeat step 3. Special movement rules apply when a
	pawn is moved the first time and for other unique situations.
	The pieces are computed with a recursive method, following each path outward for each
	piece until obstacles are encountered. Piece movement behavior is encoded with a "delta"
	attribute.
5. The user chooses the space for the move: ex: "A4" moves the pawn up 2 spaces.
6. The new board is printed. Win conditions are checked. If no win happens, we continue.
"""



print " \n \n "

# Game board
class Board(object):
	# A 2D array of piece locations
	# locations[row][col] where row 0 = 8 and col 0 = A. 
	# This input is translated in the Game class.

	def __init__(self, pieces):
		self.rows = []
		for x in range(8):
			self.rows.append([None]*8)
		for each_piece in pieces:
			self.rows[each_piece.loc.row][each_piece.loc.col] = each_piece
			each_piece.board = self

	def board_string(self):
		outputString = "\n"
		ticker = 0
		for eachRow in self.rows:
			label = str(8 - ticker)
			ticker += 1
			outputString += (label + "  ")
			for eachCol in eachRow:
				if eachCol is None:
					outputString += " .."
				else:
					if eachCol.team == 0:
						outputString += " W"
					elif eachCol.team == 1:
						outputString += " B"
					outputString += eachCol.piece_type
			outputString += "\n"
		outputString += "\n     A  B  C  D  E  F  G  H"
		return outputString

	def poll(self, row, col):
		# returns a tuple of the form (piece, in_bounds)
		if row < 0 or row > 7 or col < 0 or col > 7:
			return (None, False)
		else:
			return (self.rows[row][col], True)

class RowCol(object):
	def __init__(self, row, col):
		self.row = row
		self.col = col

class Move(object):
	def __init__(self, piece, target):
		self.piece = piece
		self.target = target
		self.net_points = 0
		self.row = self.target.row
		self.col = self.target.col
		# TODO: compute the net point value of the move

	def print_move(self):
		# print in the format "A1 -> B6"
		return rowcol_to_human(self.piece.loc) + " -> " + rowcol_to_human(self.target) + "\n\n"

def rowcol_to_human(rowcol):
	rc = rowcol
	if (rc.row < 0) or (rc.col < 0) or (rc.row > 7) or (rc.col > 7):
		return ""
	else:
		return ['A','B','C','D','E','F','G','H'][rc.col] + str(8 - rc.row)


def human_to_rowcol(input_str):
	col_conversion = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
	if input_str is None or len(input_str) is not 2 or int(input_str[1:]) is None or col_conversion[input_str[0:1].upper()] is None:
		return None

	row = 8 - int(input_str[1:])
	col = col_conversion[input_str[0:1].upper()]
	return RowCol(row, col)


# Piece class - one is created for each piece on the board
class Piece(object):
	def __init__(self, team, rowCol):
		self.team = team
		self.loc = rowCol
		self.is_alive = True
		self.first_move = True
		self.possible_moves = []

	def compute_moves(self, board):
		self.possible_moves = []
		for (dX, dY) in self.move_deltas:
			self.generate_move(self.loc, dY, dX, board)
		self.print_num_moves()

	def generate_move(self, starting_loc, dY, dX, board):
		target = RowCol(starting_loc.row + dY, starting_loc.col + dX)
		(move_valid, should_continue) = self.check_move(target, board)
		if move_valid:
			self.possible_moves.append(Move(self, target))
			if should_continue and self.piece_type in ('Q', 'R', 'B'):
				self.generate_move(target, dY, dX, board)
		else:
			pass

	# Returns a boolean tuple of the form
	# (move valid, continue checking in this direction)
	def check_move(self, target, board):
		(target_piece, in_bounds) = board.poll(target.row, target.col)
		if not in_bounds:
			return (False, False)
		elif target_piece is None:
			return (True, True) # Add and continue
		elif target_piece.team == self.team:
			return (False, False) # Not valid, stop
		elif target_piece.team != self.team:
			return (True, False) # Add but don't continue

	def print_num_moves(self):
		print str(len(self.possible_moves)) + " possible moves."

# Piece subclasses
class Pawn(Piece):
	piece_type = 'P'
	def compute_moves(self, board):
		self.possible_moves = []
		heading = (-1 + (self.team * 2)) #To define pawn movement direction

		row = self.loc.row
		col = self.loc.col

		# Straight ahead 1 space
		(target, in_bounds) = board.poll(row + heading, col)
		if target is None and in_bounds:
			self.possible_moves.append(Move(self, RowCol(row + heading, col)))

		# Straight ahead 2 spaces
		if self.first_move and target is None and in_bounds:
			(target, in_bounds) = board.poll(row + (heading * 2), col)
			if target is None and in_bounds:
				self.possible_moves.append(Move(self, RowCol(row + (heading * 2), col)))

		# To either side, only if enemies occupy those spaces
		(target_l, in_bounds_l) = board.poll(row + heading, col - 1)
		if target_l is not None and target_l.team != self.team and in_bounds_l:
			self.possible_moves.append(Move(self, RowCol(row + heading, col - 1)))

		(target_r, in_bounds_r) = board.poll(row + heading, col + 1)
		if target_r is not None and target_r.team != self.team and in_bounds_r:
			self.possible_moves.append(Move(self, RowCol(row + heading, col + 1)))

		print str(len(self.possible_moves)) + " possible moves"


class Rook(Piece):
	piece_type = 'R'
	move_deltas = [(1,0),(-1,0),(0,1),(0,-1)]

class Horse(Piece):
	piece_type = 'H'
	move_deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

class Bishop(Piece):
	piece_type = 'B'
	move_deltas = [(1,1),(1,-1),(-1,1),(-1,-1)]

class Queen(Piece):
	piece_type = 'Q'
	move_deltas = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

class King(Piece):
	piece_type = 'K'
	move_deltas = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]


def initialize_pieces():
	pieces = []
	for team in [0,1]:
		front_line = (6 - (5 * team))
		rear_guard = (7 - (7 * team))
		pieces.append(King(team, RowCol(rear_guard, 4)))
		pieces.append(Queen(team, RowCol(rear_guard, 3)))
		pieces.append(Bishop(team, RowCol(rear_guard, 2)))
		pieces.append(Bishop(team, RowCol(rear_guard, 5)))
		pieces.append(Horse(team, RowCol(rear_guard, 1)))
		pieces.append(Horse(team, RowCol(rear_guard, 6)))
		pieces.append(Rook(team, RowCol(rear_guard, 0)))
		pieces.append(Rook(team, RowCol(rear_guard, 7)))
		for pawn_num in range(0,8):
			pieces.append(Pawn(team, RowCol(front_line, pawn_num)))
	return pieces

class Game(object):

	def __init__(self, p1, p2):
		self.white = p1
		self.black = p2

		self.is_white_turn = True
		self.is_game_over = False
		self.winner = None

		self.pieces_list = initialize_pieces()
		self.board = Board(self.pieces_list)

		print(self.white + " is White.")
		print(self.black + " is Black.")

		self.run_game()

	def run_game(self):
		while (self.is_game_over is not True):
			if self.is_white_turn:
				print(self.white + "\'s turn.")
				self.run_human_turn(0)
			else:
				print(self.black + "\'s turn.")
				self.run_human_turn(1)
			self.is_white_turn = not self.is_white_turn
		print(self.victory_string(self.winner))

	def victory_string(self, winner):
		base_string = "Game Over. " + self.winner + " wins!"
		return base_string

	def run_human_turn(self, team):
		print self.board.board_string() + "\n"
		input_piece_str = raw_input("Which piece would you like to move (ex: A4)? ")
		piece_loc = human_to_rowcol(input_piece_str)

		if piece_loc is None:
			print("Invalid input. Please try again.")
			self.run_human_turn(team)
		elif self.board.poll(piece_loc.row, piece_loc.col)[0] is None:
			print "No piece exists at that point! Please try again."
			self.run_human_turn(team)
		elif self.board.poll(piece_loc.row, piece_loc.col)[0].team != team:
			print "You do not own that piece! Please try again."
			self.run_human_turn(team)
		elif self.board.poll(piece_loc.row, piece_loc.col)[0].team == team:
			active_piece = self.board.poll(piece_loc.row, piece_loc.col)[0]
			active_piece.compute_moves(self.board)
			if active_piece.possible_moves == []:
				print("That piece has no possible moves. Please select another.")
				self.run_human_turn(team)
			else:
				input_target_str = raw_input("Where would you like to move this piece? ")
				target_loc = human_to_rowcol(input_target_str)
				is_valid_move = False
				valid_move = None
				for poss_move in active_piece.possible_moves:
					if (poss_move.row == target_loc.row and poss_move.col == target_loc.col):
						is_valid_move = True
						valid_move = poss_move

				(target, out_of_bounds) = self.board.poll(target_loc.row, target_loc.col)
				if is_valid_move and target is None and valid_move is not None:
					self.board.rows[target_loc.row][target_loc.col] = active_piece
					self.board.rows[active_piece.loc.row][active_piece.loc.col] = None
					print valid_move.print_move()
					active_piece.loc = RowCol(target_loc.row, target_loc.col)
					active_piece.first_move = False
				elif is_valid_move and target is not None and valid_move is not None:
					self.board.rows[target_loc.row][target_loc.col] = active_piece
					self.board.rows[active_piece.loc.row][active_piece.loc.col] = None
					active_piece.loc = RowCol(target_loc.row, target_loc.col)
					print valid_move.print_move()
					active_piece.first_move = False
					target.is_alive = False
					if target.piece_type == 'K':
						print("The king is dead.")
						self.is_game_over = True
						if active_piece.team == 0:
							self.winner = self.white
						else:
							self.winner = self.black
				else:
					print "That isn't a valid move! Please try again."
					self.run_human_turn(team)





def new_game():
	p1 = raw_input("What is player 1's name? ")
	p2 = raw_input("What is player 2's name? ")
	game = Game(p1, p2)


new_game()
