#  File: Boxes.py

#  Description: This program takes a list of box dimensions and then passes through filters in order to figure out
#               the highest number of boxes that can nest and what subsets form those.

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name: Eric Ji

#  Partner UT EID: ej6638

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 10/17/19

#  Date Last Modified: 10/18/19


#Global Case List used to write the txt into
subsetcaselist = []
def readfile():
    #This reads the file and passes the data into a 2D list of dimensions and also sorts the list and cases.
    file= open("boxes.txt","r")
    numofboxes = int(file.readline())
    boxeslist = []
    for x in range(numofboxes):
        box = file.readline()
        box = box.strip("\n")
        boxdim = box.split(" ")
        #Sorts dimensions of each box.
        boxdim.sort()
        for i in range(len(boxdim)):
            boxdim[i] = int(boxdim[i])
        boxeslist.append(boxdim)
    #Sorts Boxes by First Coordinate
    boxeslist.sort()

    return boxeslist

def subset(a, b, lo):
    # Generate all subsets of a set and append them to a global list for a filter to sort through the subsets
    hi = len (a)
    if (lo == hi):
        subsetcaselist.append(b)
        return
    else:
        c = b[:]
        b.append (a[lo])
        subset(a, b, lo + 1)
        subset(a, c, lo + 1)

def filters():
    filteredlist = []
    #Filters out any cases that don't have enough boxes to form a subset.
    for case in range(len(subsetcaselist)):
        if len(subsetcaselist[case]) < 2:
            continue
        else:
            filteredlist.append(subsetcaselist[case])
    #Since we are only looking for the largest subsets, we sorted the cases by length and flipped the list
    #so that when we get our second filtered list, the longest cases will be first
    filteredlist.sort(key=len)
    filteredlist.reverse()

    filteredlist2 = []
    # Filters out any lists that don't make a full nest using nested helper function
    for a in filteredlist:
        nested(a, filteredlist2)
    #Takes note of longest case length as we will only need to display ones equal to the first one in our
    #sorted list. Also creating final list for displaying.
    longestcaselen = len(filteredlist2[0])
    finallist = []
    #This loop pulls all of the cases that are of equal length into our results list.
    for x in filteredlist2:
        if len(x) == longestcaselen:
            finallist.append(x)
        else:
            break
    #Flips the list back into proper order for displaying results.
    finallist.reverse()

    #If results list is empty, it prints not nesting boxes, else it displays the results passed into final list.
    if len(finallist) == 0:
        print("No Nesting Boxes")
    else:
        print("Largest Subset of Nesting Boxes")
        for x in finallist:
            for box in x:
                print(box)
            print()


def nested(a,filteredlist2):
    #This function goes through each individual case using the doesfit() helper function, if at any point the
    # helper function returns false, It does not append it to the second filtered list and removes it from out calculations
    for x in range(len(a)):
        try:
            if x == len(a):
                filteredlist2.append(a)
                return
            elif doesfit(a[x], a[x+1]):
                continue
            else:
                return
        except IndexError:
            filteredlist2.append(a)
            return


def doesfit(box1, box2):
    # Helper Function that returns true or false if a box will fit in another
    return box1[0] < box2[0] and box1[1] < box2[1] and box1[2] < box2[2]



def main():
    list = readfile()
    subsets = []
    subset(list,subsets,0)

    filters()



main()