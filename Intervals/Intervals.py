#  File: Intervals.py

#  Description: This program takes intervals from a text file, orders them and then collapses the intervals that overlaps.

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 9/8/2019

#  Date Last Modified: 9/9/2018


def readfile():

    #Reads file and removes new line character
    file = open("Intervals.txt", "r")
    intervalslist = file.readlines()

    intervalslist = [x.replace('\n', '') for x in intervalslist ]
    intervalslist.sort
    return intervalslist

def converttotuple(intervalslist):
    #Converts items of the list into tuples and splits them using the space in the middle.
    intervalslisttuple = []
    for item in intervalslist:
        smallint = []
        x = item.split(" ")
        firstnumber = int(x[0])
        secondnumber = int(x[1])
        smallint.append(firstnumber)
        smallint.append(secondnumber)
        x = tuple(smallint)

        intervalslisttuple.append(x)
    return intervalslisttuple

def collapsetheintervals(intervalslist):
    # Takes each tuple piece by piece and compares the values then files them into the final list for printing.
    collapsedlist = []
    for tup in intervalslist:
        if collapsedlist:
            lower = collapsedlist[-1]

            if tup[0] <= lower[1]:
                highest = max(lower[1], tup[1])

                collapsedlist[-1] = (lower[0], highest)
            else:
                collapsedlist.append(tup)
        else:
            collapsedlist.append(tup)
    return collapsedlist

def printfinalList(collapsedlist):
    #Prints the intervals out
    print("Non-intersecting Intervals:")
    for tup in (collapsedlist):
        print((tup),end="\n")

def main():
    #Read all of the intervals off of the file and then set them in a list
    intervals = readfile()
    #Convert the elements of the lists to ints and then place them into tuples.
    tup = converttotuple(intervals)
    #Sort the Tuple List
    tup.sort()
    #Collapse the possible intervals
    collapsed = collapsetheintervals(tup)
    #Prints out the intervals in proper format
    printfinalList(collapsed)


main()
