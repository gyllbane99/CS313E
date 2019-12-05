#  File: BST_Cipher.py

#  Description: This program creates a simple encryption scheme using
#  a binary search tree. It encodes a sentence,
#  insert each letter into a binary tree using the
#  ASCII value as a comparative measure.

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name: Eric Ji

#  Partner UT EID: ej6638

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 11/18/19

#  Date Last Modified: 11/19/19

class Tree(object):
    # the init() function creates the binary search tree with the
    # encryption string. If the encryption string contains any
    # character other than the characters 'a' through 'z' or the
    # space character drop that character.
    def __init__(self, encrypt_str):
        self.root = None
        for char in encrypt_str:
            self.insert(char)

    # the insert() function adds a node containing a character in
    # the binary search tree. If the character already exists, it
    # does not add that character. There are no duplicate characters
    # in the binary search tree.
    def insert(self, ch):
        newnode = Node(ch)
        if self.root is None:
            self.root = newnode
        else:
            if not self.duplicate(ch):
                current = self.root
                while current is not None:
                    parent = current
                    if ch < current.data:
                        current = current.lChild
                    else:
                        current = current.rChild
                if ch < parent.data:
                    parent.lChild = newnode
                else:
                    parent.rChild = newnode

    # helper function that checks to see if there is a duplicate
    def duplicate(self, ch):
        current = self.root
        while current != None and current.data != ch:
            if ch < current.data:
                current = current.lChild
            else:
                current = current.rChild
        return current

    # the search() function will search for a character in the binary
    # search tree and return a string containing a series of lefts
    # (<) and rights (>) needed to reach that character. It will
    # return a blank string if the character does not exist in the tree.
    # It will return * if the character is the root of the tree.
    def search(self, ch):
        current = self.root
        if ch == current.data:
            return "*"
        else:
            encstr = ""
            while current is not None and current.data is not ch:
                if ch < current.data:
                    current = current.lChild
                    encstr += "<"
                else:
                    current = current.rChild
                    encstr += ">"
            return encstr

    # the traverse() function will take string composed of a series of
    # lefts (<) and rights (>) and return the corresponding
    # character in the binary search tree. It will return an empty string
    # if the input parameter does not lead to a valid character in the tree.
    def traverse(self, st):
        current = self.root
        if st is "*":
            return self.root.data
        for char in st:
            if char is "<":
                current = current.lChild
            elif char is ">":
                current = current.rChild
            else:
                return ""
        return current.data

    # the encrypt() function will take a string as input parameter, convert
    # it to lower case, and return the encrypted string. It will ignore
    # all digits, punctuation marks, and special characters.
    def encrypt (self, st):
        st = st.lower()
        enc_str = ""
        for item in st:
            item_enc = self.search(item)
            enc_str += item_enc + "!"
        return enc_str[0:-1]

    # the decrypt() function will take a string as input parameter, and
    # return the decrypted string.
    def decrypt(self, st):
        decrypt = ''
        ch = ''
        for item in range(len(st)):
            if st[item] == '!':
                decrypt += self.traverse(ch)
                ch = ''
            elif item == len(st)-1:
                ch += st[item]
                decrypt += self.traverse(ch)
            else:
                ch += st[item]
        return decrypt


class Node(object):
    def __init__(self, data):
        self.data = data
        self.lChild = None
        self.rChild = None


def main():
    encryptkey = str(input("Enter encryption key: "))
    encryptkey = encryptkey.lower()
    binarytree = Tree(encryptkey)
    print()

    encryptstring = str(input("Enter string to be encrypted: "))
    enscryptedstring = binarytree.encrypt(encryptstring)
    print("Encrypted string: ", enscryptedstring)
    print()

    decryptstring = str(input("Enter string to be decrypted: "))
    decryptedstring = binarytree.decrypt(decryptstring)
    print("Decrypted string: ", decryptedstring)


main()