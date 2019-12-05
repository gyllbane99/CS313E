#  File: Reducible.py

#  Description: Takes a large file of words, Hashes them, then prints the longest word that can be reduced

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name: Eric Ji

#  Partner UT EID: ej6638

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 10/26/19

#  Date Last Modified:10/28/19

# takes as input a positive integer n
# returns True if n is prime and False otherwise
def is_prime ( n ):
  if (n == 1):
    return False

  limit = int (n ** 0.5) + 1
  div = 2
  while (div < limit):
    if (n % div == 0):
      return False
    div += 1
  return True
# takes as input a string in lower case and the size
# of the hash table and returns the index the string
# will hash into
def hash_word (s, size):
  hash_idx = 0
  for j in range (len(s)):
    letter = ord (s[j]) - 96
    hash_idx = (hash_idx * 26 + letter) % size
  return hash_idx
# takes as input a string in lower case and the constant
# for double hashing and returns the step size for that
# string
def step_size (s, const):
  string_id = hash_word(s,len(s))
  step = const - (string_id % const)
  return step
# takes as input a string and a hash table and enters
# the string in the hash table, it resolves collisions
# by double hashing
def insert_word (s, hash_table):
    string_id = hash_word(s,len(hash_table))
    while True:
        #Checks to see if the spot is empty
        if hash_table[string_id] == "":
            hash_table[string_id] = s
            return
        #IF it is not, double hash time
        else:
            step = step_size(s, 13)
            string_id += step
# takes as input a string and a hash table and returns True
# if the string is in the hash table and False otherwise
def find_word (s, hash_table):
    string_id = hash_word(s,len(hash_table))
    if s == hash_table[string_id]:
        return True
    return False
# recursively finds if a word is reducible, if the word is
# reducible it enters it into the hash memo and returns True
# and False otherwise
def is_reducible (s, hash_table, hash_memo):
    if s == "a" or s == "o" or s == "i":
        return True
    elif find_word(s,hash_memo):
        return True
    elif not find_word(s,hash_table) or s == "":
        return False
    else:
        for i in range(len(s)):
            new_string = s[ : i ] + s[ i + 1 : ]
            if is_reducible(new_string,hash_table, hash_memo):
                string_id = hash_word(s,len(hash_memo))

                hash_memo[string_id] = s

                return True
# goes through a list of words and returns a list of words
# that have the maximum length
def get_longest_words(string_list):
    longestwordlist = []
    string_list.sort(key=len)
    string_list.reverse()

    longestword = len(string_list[0])
    for x in string_list:
        if len(x) < longestword:
            break
        else:
            longestwordlist.append(x)

    return longestwordlist

def main():
  # create an empty word_list
    word_list = []
  # open the file words.txt
    in_file = open("words.txt", "r")
  # read words from words.txt and append to word_list
  # I had to hard code the length of the word_list otherwise it would skip
  # every other word for some reason.
    for line in in_file:
        line = line.strip()
        word_list.append(line)
  # close file words.txt
    in_file.close()
  # find length of word_list
    length = len(word_list)
  # determine prime number N that is greater than twice
  # the length of the word_list
    N = 2 * length
    while True:
        prime = is_prime(N)
        if prime == False:
            N +=1
        else:
            break
  # create and empty hash_list
    hash_list = []
  # populate the hash_list with N blank strings
    for x in range(0,N):
        hash_list.append("")
  # hash each word in word_list into hash_list
  # for collisions use double hashing
    for x in word_list:
        insert_word(x,hash_list)
  # create an empty hash_memo
    hash_memo = []
  # populate the hash_memo with M blank strings
    for x in range(0, 27011):
        hash_memo.append("")
  # create and empty list reducible_words
    reducible_words = []
  # for each word in the word_list recursively determine
  # if it is reducible, if it is, add it to reducible_words
    for word in word_list:
        if is_reducible(word, hash_list, hash_memo):
            reducible_words.append(word)
  # find words of the maximum length in reducible_words
    longest = get_longest_words(reducible_words)
  # print the words of maximum length in alphabetical order
  # one word per line
    for x in longest:
        print(x)
# This line above main is for grading purposes. It will not
# affect how your code will run while you develop and test it.
# DO NOT REMOVE THE LINE ABOVE MAIN
if __name__ == "__main__":
  main()
