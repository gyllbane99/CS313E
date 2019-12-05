#  File: Queens.py

#  Description:

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name:

#  Partner UT EID:

#  Course Name: CS 313E

#  Unique Number:

#  Date Created:

#  Date Last Modified:

class Queens (object):
  # initialize the board
  def __init__ (self, n = 8):
    self.board = []
    self.n = n
    self.numofSol = 0
    for i in range (self.n):
      row = []
      for j in range (self.n):
        row.append ('*')
      self.board.append (row)

  # print the board
  def print_board (self):
    for i in range (self.n):
      for j in range (self.n):
        print (self.board[i][j], end = ' ')
      print ()



  # check if no queen captures another
  def is_valid (self, row, col):
    for i in range (self.n):
      if (self.board[row][i] == 'Q' or self.board[i][col] == 'Q'):
        return False
    for i in range (self.n):
      for j in range (self.n):
        row_diff = abs (row - i)
        col_diff = abs (col - j)
        if (row_diff == col_diff) and (self.board[i][j] == 'Q'):
          return False
    return True

  # do a recursive backtracking solution
  def recursive_solve (self, col):
    if (col == self.n):
      return True
    else:
      for i in range (self.n):
        if (self.is_valid(i, col)):
          self.board[i][col] = 'Q'
          if (self.recursive_solve (col + 1)):
            return True
          self.board[i][col] = '*'
      return False

  # if the problem has a solution print the board
  def solve(self, n):

      if (n == self.n):
          self.numofSol += 1
          self.print_board()
          print()
      else:
          for i in range (self.n):
              if (self.is_valid(i,n)):
                  self.board[i][n] = "Q"
                  self.solve(n + 1)
                  self.board[i][n] = "*"
      return self.numofSol

def main():

  # Asks the user for input of size of board and only accepts ints between 1 and 8
  while True:
    n = int(input("Enter the size of board: "))
    if n >= 1 and n <=8:
      break
    else:
      print("Please enter a number between 1 and 8")
  print()
  # create a regular chess board
  game = Queens(n)

  # place the queens on the board

  # if n equals two or three, there are no solutions and this if block states that and stops the program
  if n == 2 or n == 3:
    print("There are 0 solutions for a {0} x {0} board".format(n))
  else:

    numofSol = game.solve(0)
    print("There are {0} solutions for a {1} x {1} board".format(numofSol,n))
main()
