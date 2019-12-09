# Chess

To run: `python ./chess.py`

---

### Group Members
* Dominic Holmes (hdominic@seas)

### Project Description
The project is a version of chess, implemented on the command line. The game flow is as follows:
1. A user invokes the program and types in the name for each player.
2. Player 1 is always white, so they go first.
3. They choose the piece they'd like to move: ex "A2" moves the leftmost white pawn.
4. All possible moves from the selected piece are computed. If no possible moves exist for that piece, repeat step 3. Special movement rules apply when a pawn is moved the first time and for other unique situations. The pieces are computed with a recursive method, following each path outward for each piece until obstacles are encountered. Piece movement behavior is encoded with a "delta" attribute, which allows us to encode piece movement behavior in a space-efficient way.
5. The user chooses the space for the move: ex: "A4" moves the pawn up 2 spaces.
6. The new board is printed. Win conditions are checked. If no win happens, we continue. If a king is taken, the game ends with the winning player's name being printed.

### Code Description
In order of appearance:
* The Board class contains information about piece position, as well as print statements.
* The RowCol and Move classes are helper classes to clean up movement code.
* The Piece class contains movement generation functions, including a function that generates possible moves based on the piece type and the given "move deltas" that each piece includes.
* The Pawn, Rook, King, etc classes contain delta encodings for each piece; this describes their movement behavior. The Pawn class movement had to be encoded manually, because its behavior is so different and situational.
* The Game class contains functions for actually running the game and interacting with the command line user.
* At the very end of the file, `new_game()` is called.
