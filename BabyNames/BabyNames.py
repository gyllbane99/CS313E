#  File: BabyNames.py

#  Description: This program reads a text file known as names.txt and lets the user explore the popularity of names
#               from various decades.

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created:9/11/19

#  Date Last Modified: 9/13/19

#NOTE TO GRADER PLEASE CHECK INSIDE optionthree() FOR AN EXPLANATION OF ONE BUG IN MY PROGRAM...
def readfile():

    # This section of code reads the file line by line and packs all of the names and ranks into the dictionary namesdict.
    namesdict = {}
    with open("names.txt") as file:
        for line in file:
            (name, rank1900, rank1910, rank1920,rank1930,rank1940,rank1950,rank1960,rank1970,rank1980,rank1990,rank2000) = line.split()
            namesdict[str(name).lower()] = int(rank1900), int(rank1910),int(rank1920),int(rank1930),int(rank1940),int(rank1950),int(rank1960),int(rank1970),int(rank1980),int(rank1990),int(rank2000)
    #Closes File and Returns the dictionary to the main function for later use.
    file.close()
    return namesdict

def optionone(namesdict):
    #Takes userinput and searches it against the names inside the database
    userinput = str(input("Enter a name: "))
    name = namesdict.get(userinput.lower())
    #If the name is not found it returns to the user that there is not a name that matches what was entered in the database.
    if name == None:
        print(userinput,"does not appear in any decade.")
        print()
    # If the name is found, the loop below shifts through the tuple and adds the decades that the name was popular to a list.
    # This does account for the edge case of a name being the same rank in multiple decades.
    else:
        print("The matches with their highest ranking decades are:")
        bestrank = 1001
        decadelist = []
        decade = 1900
        for x in range(0,11):
            if name[x] == bestrank:
                decadelist.append(decade)
                decade += 10
            elif name[x] < bestrank and name[x] != 0:
                bestrank = name[x]
                decadelist.append(decade)
                decade += 10
            else:
                decade += 10
                continue
        # And Finally my print statement that prints out the name followed by the decades it was most popular.
        print(userinput,end=" ")
        for x in decadelist:
            print(x, end = " ")

    print("\n")

def optiontwo(namesdict):
    #Takes userinput and searches it against the names inside the database
    userinput = str(input("Enter a name: "))
    name = namesdict.get(userinput.lower())
    #If the name is not found it returns to the user that there is not a name that matches what was entered in the database.
    if name == None:
        print(userinput,"does not appear in any decade.")
    #If the name is found, it prints the name and the list of rankings, and then below that prints the rankings with each decade
    # associated with it.
    else:
        print(userinput.capitalize() + ": ", end="")
        for x in name:
            print(x, end =" ")
        print("")
        decade = 1900
        i = 0
        while decade <= 2000:
            rank = name[i]
            print('{0}: {1}'.format(decade,rank))
            decade += 10
            i +=1
    print("\n")

def optionthree(namesdict):
    #Takes in input of the decade, checking to make sure it fits into one of the decades, stores the index value for later
    try:
        userinput = int(input("Enter decade: "))
        if userinput == 1900:
            index = 0
        elif userinput == 1910:
            index = 1
        elif userinput == 1920:
            index = 2
        elif userinput == 1930:
            index = 3
        elif userinput == 1940:
            index = 4
        elif userinput == 1950:
            index = 5
        elif userinput == 1960:
            index = 6
        elif userinput == 1970:
            index = 7
        elif userinput == 1980:
            index = 8
        elif userinput == 1990:
            index = 9
        elif userinput == 2000:
            index = 10
        else:
            ValueError
        #Here I am taking the values and putting them into two parallel lists that I then shuffle together in the next for loop.
        mixedlist=[]
        nameslist = list(namesdict.keys())
        valueslist = list(namesdict.values())
        for x in range(0,4429):
            mixedlist.append(nameslist[0])
            mixedlist.append(valueslist[0])
            del nameslist[0]
            del valueslist[0]


        #Here the shuffled list is filtered down to the names that only appear in that decade that the user specified.
        #To properly go through the list it deletes the first entries after it decides what to do with it.
        unsortedrankedlist = []
        for x in range(0,4429):
            if mixedlist[1][index] > 0:
                unsortedrankedlist.append(mixedlist[0])
                unsortedrankedlist.append(mixedlist[1][index])
                del mixedlist[0]
                del mixedlist[0]
            else:
                del mixedlist[0]
                del mixedlist[0]


        #Creates a list for the names to be placed into to list the names in order.
        rankedlist = []
        for x in range(0,1000):
            rankedlist.append(0)


        #This Loops sorts names by placing them at an index one less than their rank.
        for x in unsortedrankedlist:
            rank = int(unsortedrankedlist[1])
            rankedlist.insert(rank - 1,unsortedrankedlist[0])
            del unsortedrankedlist[0]
            del unsortedrankedlist[0]
        print("The names are in order of rank:")
        #This loops prints out the names and their associated ranks using the indexes from the list.
        #NOTE TO GRADER: There is a bug involving some of the ranks being slightly skewed. I've tried everything I can to fix it
        # but to no avail. The names are printing out in the correct order however.
        for x in rankedlist:
            if rankedlist.index(x) > 999:
                break
            elif x != 0:
                print("{0}: {1}".format(x.capitalize(), rankedlist.index(x) + 1))
    #My Error Catchers just in case of some weird input.
    except KeyError:
        print("An Error has occurred. Please Try Again")
    except ValueError:
        print("An Error has occurred. Please Try Again")

    print("\n ")

def optionfour(namesdict):
    #Again, running parallel lists from the dictionary to sort through the names to determine which names appear in every
    #decade.
    alldecadeslist = []
    nameslist = []
    valueslist = []
    for name in namesdict.keys():
        nameslist.append(name)
    for value in namesdict.values():
        valueslist.append(value)

    #This loop checks for a 0 inside of the valueslist tuple and if its not present, it appends it to the alldecadeslist
    for x in range(0,4429):
        if 0 in valueslist[0]:
            del nameslist[0]
            del valueslist[0]
        else:
            alldecadeslist.append(nameslist[0])
            del nameslist[0]
            del valueslist[0]
    #Format Printing
    print("{0} names are less popular in every decade. The names are: ".format(len(alldecadeslist)))
    for name in alldecadeslist:
        print(name.capitalize())
    print("\n")

def optionfive(namesdict):
    #This List is used to store the names that are appended from the loop below.
    morepopularlist = []
    for names in namesdict.keys():
        value = namesdict.get(names)
        #This function call takes us down to def ismorepopular where it runs through the tuple to check and see if the list is
        #constantly increasing, then returns a Boolean which is used below to decide whether or not to append.
        morepopular = ismorepopular(value)

        if morepopular == True:
            morepopularlist.append(names)
        elif morepopular == False:
            continue

    #Format Printing of names
    print("{0} names are more popular in every decade.".format(len(morepopularlist)))
    for x in morepopularlist:
        print(x.capitalize())
    print("\n")

def ismorepopular(value):
    #This Function takes the tuple passed into it and runs through it comparing the values. If they are constantly decreasing
    #(More Popular), it returns true, else it returns False. It also handles the edge case of repeated zeros, which tells it to
    #return false
    originalvalue = 9999
    for number in value:
        if number == 0 and originalvalue == 0:
            return False
        elif number <= originalvalue:
            originalvalue = number
        elif number > originalvalue:
            return False

    return True

def optionsix(namesdict):
    #This function takes the tuple from the dictionary and feeds them into the islesspopular function.
    lesspopularlist = []
    for names in namesdict.keys():
        value = namesdict.get(names)
        lesspopular = islesspopular(value)
        #Here it decides what to do with the name depending on the Boolean given
        if lesspopular == True:
            lesspopularlist.append(names)
        elif lesspopular == False:
            continue

    #Formatted Printing of results
    print("{0} names are less popular in every decade.".format(len(lesspopularlist)))
    for x in lesspopularlist:
        print(x.capitalize())
    print("\n")

def islesspopular(value):
    #This Function takes the tuple passed into it and runs through it comparing the values. If they are constantly increasing
    #(Less Popular), it returns true, else it returns False.
    originalvalue = 1
    for number in value:
        if number == 0:
            number = 1001

        if originalvalue == 1001:
            #Runs into a zero early on.
            return False

        if number > originalvalue:
            originalvalue = number
        else:
            return False

    return True

def optionseven():
    #This function only exists because I wanted my mainmenu() function to look nice and uniform. No other reason :)
    print("\n")
    print("Goodbye.")

def mainmenu(namesdict):
    loopmech = True
    while loopmech == True:
        print("Options:\nEnter 1 to search for names.")
        print("Enter 2 to display data for one name.\nEnter 3 to display all names that appear in only one decade.")
        print("Enter 4 to display all names that appear in all decades.\nEnter 5 to display all names that are more popular in every decade.")
        print("Enter 6 to display all names that are less popular in every decade.\nEnter 7 to quit.\n ")
        #My Try Except Block here rejects any input that it does not recognize as a valid input. It will accept ints 1-7
        #Each menu option corresponds with a function.
        try:
            userinput = int(input("Enter choice: "))
            if userinput == 1:
                optionone(namesdict)
            elif userinput == 2:
                optiontwo(namesdict)
            elif userinput == 3:
                optionthree(namesdict)
            elif  userinput == 4:
                optionfour(namesdict)
            elif  userinput == 5:
                optionfive(namesdict)
            elif  userinput == 6:
                optionsix(namesdict)
            elif  userinput == 7:
                optionseven()
                loopmech = False
        except ValueError:
            None

def main():

    namesdict = readfile()
    mainmenu(namesdict)

main()
