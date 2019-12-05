#  File: bridgevv.py

#  Description: This program takes a text file of numbers and returns the least amount of time it would take the group to
#               cross the bridge.

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name: Eric Ji

#  Partner UT EID: ej6638

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 10/3/19

#  Date Last Modified: 10/4/19

def shortestTime(caselist):
    #If there is only one person that has to cross, returns the time taken by that one person.
    if len(caselist) == 1:
        return caselist[0]
    #If there are only 2 people that need to cross, returns the time taken by the slowest of the two people.
    if len(caselist) == 2:
        if caselist[0] > caselist[1]:
            return caselist[0]
        if caselist[0] < caselist[1]:
            return caselist[1]

    #If more than 2 people need to cross the bridge, the function starts with the First Method
    if len(caselist) > 2:
        #Method 1
        methodonetotal = 0
        min = 60
        #Finds the fastest person in the case.
        for i in caselist:
            if i < min:
                min = i
        tot = 0
        #Finds time it takes fastest person to walk back and keeps track of how many return trips he makes.
        speedMult = len(caselist) - 2
        for i in caselist:
            if i != min:
                tot += i
        fastest = min * speedMult
        #Using First Method, This is the total time it would take to have the group cross the Bridge.
        methodonetotal = tot + fastest

        #Method 2
        strat2 = 0
        caselist.sort()
        #Finds Fastest 2 People in the case
        fast1 = caselist[0]
        fast2 = caselist[1]
        #Finds the initial Slowest 2 People in the Case
        slow1 = caselist[len(caselist) - 1]
        slow2 = caselist[len(caselist) - 2]
        crossed = []
        notCrossed = caselist
        secondmethodtotal = 0
        #As long as there are still people that have not crossed, it keeps running.
        while len(notCrossed) != 0:
            #If there is only 1 person left to cross and it is the fastest person
            if len(notCrossed) == 1 and fast1 in notCrossed:
                #Second fastest person comes back to retrieve fastest person
                tot += fast2
                notCrossed.append(fast2)
                #Second fastest person crosses with fastest person
                tot += fast2
                crossed.append(fast1)
                crossed.append(fast2)
                notCrossed.remove(fast1)
                notCrossed.remove(fast2)
            #If there is only 1 person left to cross
            if len(notCrossed) == 1 and fast1 in crossed:
                #Fastest person comes back to retrieve last person
                tot += fast1
                tot += notCrossed[0]
                notCrossed.remove(notCrossed[0])
            #If the fastest 2 have not crossed yet
            if fast1 in notCrossed and fast2 in notCrossed:
                #Fastest 2 people cross the bridge
                secondmethodtotal += fast2
                crossed.append(fast1)
                crossed.append(fast2)
                notCrossed.remove(fast1)
                notCrossed.remove(fast2)
            #If the fastest 2 crossed
            if fast1 in crossed and fast2 in crossed:
                #Fastest goes back to return flashlight
                secondmethodtotal += fast1
                crossed.remove(fast1)
                notCrossed.append(fast1)
                # 2 slowest people cross
                #If slow2 is the same person as fast2, this means that the fastest person and the slowest person is left
                if slow2 == fast2:
                    secondmethodtotal += slow1
                    notCrossed.remove(slow1)
                    notCrossed.remove(fast1)
                    break
                #If the fast1 is the same person as slow2, this means that only the fastest person is left
                elif fast1 == slow2:
                    secondmethodtotal += slow1
                    crossed.append(fast1)
                    crossed.append(slow1)
                    notCrossed.remove(fast1)
                    break
                else:
                    secondmethodtotal += slow1
                    crossed.append(slow1)
                    crossed.append(slow2)
                    notCrossed.remove(slow1)
                    notCrossed.remove(slow2)
                #assigns next 2 slowest of the people that have not crossed
                if len(notCrossed) == 1 and fast1 not in notCrossed:
                    tot += fast1
                    tot += notCrossed[0]
                    crossed.append(notCrossed[0])
                    notCrossed.remove(notCrossed[0])
                    break
                else:
                    notCrossed.sort()
                    slow1 = notCrossed[len(notCrossed) - 1]
                    slow2 = notCrossed[len(notCrossed) - 2]
            #If the fastest person has not crossed and the second fastest person crossed
            if fast1 not in crossed and fast2 in crossed:
                #Second fastest goes back
                secondmethodtotal += fast2
                #Fastest and second fastest cross
                secondmethodtotal += fast2
                crossed.append(fast1)
                notCrossed.remove(fast1)

        #Checks to see which strategy is faster and returns the value that is the lesser of the two.
        if methodonetotal < secondmethodtotal:
            return methodonetotal
        else:
            return secondmethodtotal


def main():
    file = open("bridge.txt",'r')
    #Reads the number of cases
    numofCases = int(file.readline())
    #Creates a list of the different cases.
    for i in range(numofCases):
        file.readline()
        numPeople = file.readline().split()
        numPeople = int(numPeople[0])
        list1 = []
        for x in range(numPeople):
            time = int(file.readline())
            list1.append(time)
        print(shortestTime(list1))
        print()




if __name__ == "__main__":
    main()