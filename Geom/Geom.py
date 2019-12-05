#  File: Geom.py

#  Description: This program takes inputs and returns a bunch of calculations for Geometry

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name: Eric Ji

#  Partner UT EID: ej6638

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 9/18/19

#  Date Last Modified: 9/20/19

import math

class Point(object):
    # constructor
    # x and y are floats
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # get distance
    # other is a Point object
    def dist(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    # get a string representation of a Point object
    # takes no arguments
    # returns a string
    def __str__(self):
        return '(' + str(self.x) + ", " + str(self.y) + ")"

    # test for equality
    # other is a Point object
    # returns a Boolean
    def __eq__(self, other):
        tol = 1.0e-8
        return ((abs(self.x - other.x) < tol) and (abs(self.y - other.y) < tol))


class Circle(object):
    # constructor
    # x, y, and radius are floats
    def __init__(self, radius=1, x=0, y=0):
        self.radius = radius
        self.center = Point(x, y)

    # compute cirumference
    def circumference(self):
        return 2.0 * math.pi * self.radius

    # compute area
    def area(self):
        return math.pi * self.radius * self.radius

    # determine if point is strictly inside circle
    def point_inside(self, p):
        return (self.center.dist(p) < self.radius)

    # determine if a circle is strictly inside this circle
    def circle_inside(self, c):
        distance = self.center.dist(c.center)
        return (distance + c.radius) < self.radius

    # determine if a circle c overlaps this circle (non-zero area of overlap)
    # but neither is completely inside the other
    # the only argument c is a Circle object
    # returns a boolean
    def circle_overlap(self, c):
        distance = self.center.dist(c.center)
        radiussum = self.radius + c.radius
        if distance == radiussum or distance > radiussum:
            return False
        if distance < radiussum:
            return True

    # determine the smallest circle that circumscribes a rectangle
    # the circle goes through all the vertices of the rectangle
    # the only argument, r, is a rectangle object
    def circle_circumscribe(self, r):
        centerpoint = Point(r.center.x, r.center.y)

        radius = centerpoint.dist(r.ul)
        circum = Circle(radius, r.center.x, r.center.y)
        return circum


    # string representation of a circle
    # takes no arguments and returns a string
    def __str__(self):
        return "Radius: " + str(round(self.radius, 2)) + ", Center: " + str(self.center)

    # test for equality of radius
    # the only argument, other, is a circle
    # returns a boolean
    def __eq__(self, other):
        tol = 1.0e-8
        return(abs(self.radius) - abs(other.radius)) < tol


class Rectangle(object):
    # constructor
    def __init__(self, ul_x=0, ul_y=1, lr_x=1, lr_y=0):
        if ((ul_x < lr_x) and (ul_y > lr_y)):
            self.ul = Point(ul_x, ul_y)
            self.lr = Point(lr_x, lr_y)
        else:
            self.ul = Point(0, 1)
            self.lr = Point(1, 0)
        self.center = Point(self.ul.x - ((self.ul.x - self.lr.x) // 2), (self.ul.y - abs((self.ul.y - self.lr.y) // 2)))
    # determine length of Rectangle (distance along the x axis)
    # takes no arguments, returns a float
    def length(self):
        length = self.ul.x - self.lr.x
        return length
    # determine width of Rectangle (distance along the y axis)
    # takes no arguments, returns a float
    def width(self):
        width = self.ul.y - self.lr.y
        return width
    # determine the perimeter
    # takes no arguments, returns a float
    def perimeter(self):
        lengths = 2 * abs(self.length())
        widths = 2 * abs(self.width())
        perimeter = lengths + widths
        return perimeter
    # determine the area
    # takes no arguments, returns a float
    def area(self):
        area = abs(self.length()) * abs(self.width())
        return area
    # determine if a point is strictly inside the Rectangle
    # takes a point object p as an argument, returns a boolean
    def point_inside(self, p):
        if self.ul.dist(p) < self.lr.x and self.lr.dist(p) < self.ul.y:
            return True
        else:
            return False
    # determine if another Rectangle is strictly inside this Rectangle
    # takes a rectangle object r as an argument, returns a boolean
    # should return False if self and r are equal
    def rectangle_inside(self, r):
        if r.ul.y < self.ul.y and r.lr.y > self.lr.y and r.ul.x > self.ul.x and r.lr.x < self.lr.x:
            return True
        else:
            return False
    # determine if two Rectangles overlap (non-zero area of overlap)
    # takes a rectangle object r as an argument returns a boolean
    def rectangle_overlap(self, r):
        if self.point_inside(r.ul) or self.point_inside(r.lr):
            return True
        elif self.ul.x < r.ul.x and self.ul.y < r.ul.y and self.ul.y > r.lr.y and self.lr.x > r.ul.x:
            return True
        elif self.ul.y > r.lr.y and r.ul.x < self.lr.x:
            return True
        elif r.ul.y > self.lr.y and r.lr.x > self.ul.x:
            return True
        else:
            return False

    # determine the smallest rectangle that circumscribes a circle
    # sides of the rectangle are tangents to circle c
    # takes a circle object c as input and returns a rectangle object
    def rectangle_circumscribe(self, c):
        ul_x = c.center.x - c.radius
        ul_y = c.center.y + c.radius
        lr_x = c.center.x + c.radius
        lr_y = c.center.y - c.radius
        rect = Rectangle(ul_x, ul_y, lr_x, lr_y)
        return rect
    # give string representation of a rectangle
    # takes no arguments, returns a string
    def __str__(self):
        return "UL: " + str(self.ul) + ", LR: " + str(self.lr)

    # determine if two rectangles have the same length and width
    # takes a rectangle other as argument and returns a boolean
    def __eq__(self, other):
        tol = 1.0e-8
        return abs(self.length()- abs(other.length())) < tol and abs(self.width()- abs(other.width())) < tol


def main():
# open the file geom.txt

    file = open('geom.txt', 'r')
    coord = []
    for x in file.readlines():
        string = x[0:34]
        string = string.split()
        string = list(map(float, string))
        coord.append(string)

# create Point objects P and Q
    p = Point(coord[0][0],coord[0][1])
    q = Point(coord[1][0],coord[1][1])

# print the coordinates of the points P and Q
    print("Coordinates of P:",p)
    print("Coordinates of Q:",q)
# find the distance between the points P and Q
    pqdistance = Point.dist(p,q)
    print("Distance between P and Q:", round(pqdistance, 2))
# create two Circle objects C and D
    c = Circle(coord[2][0],coord[2][1],coord[2][2])
    d = Circle(coord[3][0],coord[3][1],coord[3][2])
# print C and D
    print("Circle C:",c)
    print("Circle D:",d)

# compute the circumference of C
    ccircum = c.circumference()
    print("Circumference of C:",round(ccircum , 2))

# compute the area of D
    darea = d.area()
    print("Area of D:",round(darea, 2))
# determine if P is strictly inside C
    pointinside = c.point_inside(p)
    if pointinside == True:
        print("P is inside C")
    elif pointinside == False:
        print("P is not inside C")
    else:
        print("Error")
# determine if C is strictly inside D
    circleinside = d.circle_inside(c)
    if circleinside == True:
        print("C is inside D")
    elif circleinside == False:
        print("C is not inside D")
    else:
        print("Error")

# determine if C and D intersect (non zero area of intersection)
    circleintersect = d.circle_overlap(d)
    if circleintersect == True:
        print("C does intersect D")
    elif circleintersect == False:
        print("C does not intersect D")
    else:
        print("Error")

# determine if C and D are equal (have the same radius)
    cradius = c.radius
    dradius = d.radius
    if cradius == dradius:
        print("C is equal to D")
    else:
        print("C is not equal to D")
# create two rectangle objects G and H
    g = Rectangle(coord[4][0],coord[4][1],coord[4][2],coord[4][3])
    h = Rectangle(coord[5][0],coord[5][1],coord[5][2],coord[5][3])
# print the two rectangles G and H
    print("Rectangle G:", g)
    print("Rectangle H:", h)

# determine the length of G (distance along x axis)
    glength = g.length()
    print("Length of G:", abs(glength))
# determine the width of H (distance along y axis)
    hwidth = h.length()
    print("Width of H:", abs(hwidth))
# determine the perimeter of G
    gperimeter = g.perimeter()
    print("Perimeter of G:",gperimeter)
# determine the area of H
    harea = h.area()
    print("Area of H:", harea)

# determine if point P is strictly inside rectangle G
    pointinsiderect = g.point_inside(p)
    if pointinsiderect == True:
        print("P is inside G")
    elif pointinsiderect == False:
        print("P is not inside G")
    else:
        print("Error")
# determine if rectangle G is strictly inside rectangle H
    ginsideh = g.rectangle_inside(h)
    if ginsideh == True:
        print("G is inside H")
    elif ginsideh == False:
        print("G is not inside H")
    else:
        print("Error")
# determine if rectangles G and H overlap (non-zero area of overlap)
    ghoverlap = g.rectangle_overlap(h)
    if ghoverlap == True:
        print("G does overlap H")
    elif ghoverlap == False:
        print("G does not overlap H")
    else:
        print("Error")
# find the smallest circle that circumscribes rectangle G
# goes through the four vertices of the rectangle
    circum = c.circle_circumscribe(g)
    print("Circle that circumscribes G:", circum)
# find the smallest rectangle that circumscribes circle D
# all four sides of the rectangle are tangents to the circle
    circumrect = Rectangle()
    print("Rectangle that circumscribes D:", circumrect.rectangle_circumscribe(d))
# determine if the two rectangles have the same length and width
    rectequal = g.__eq__(h)
    if rectequal == True:
        print("Rectangle G is equal to H")
    elif rectequal == False:
        print("Rectangle G is not equal to H")
    else:
        print("Error")
# close the file geom.txt
    file.close()
# This line above main is for grading purposes. It will not affect how
# your code will run while you develop and test it.
# DO NOT REMOVE THE LINE ABOVE MAIN
if __name__ == "__main__":
    main()