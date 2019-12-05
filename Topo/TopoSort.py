#  File: TopoSort.py

#  Description: This program using graphs and other classes to do a topo sort.

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name: Eric Ji

#  Partner UT EID: ej6638

#  Course Name: CS 313E

#  Unique Number: 50205

#  Date Created: 12/1/19

#  Date Last Modified: 12/2/19

class Stack(object):
    def __init__(self):
        self.stack = []

    # add an item to the top of the stack
    def push(self, item):
        self.stack.append(item)

    # remove an item from the top of the stack
    def pop(self):
        return self.stack.pop()

    # check what item is on top of the stack without removing it
    def peek(self):
        return self.stack[len(self.stack) - 1]

    # check if a stack is empty
    def is_empty(self):
        return (len(self.stack) == 0)

    # return the number of elements in the stack
    def size(self):
        return (len(self.stack))

    def is_inside(self, label):
        labels = []
        while (not self.is_empty()):
            labels.append(self.pop())
        labels.reverse()
        for val in labels:
            self.push(val)
        if (label in labels):
            return True
        return False

class Queue(object):
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return (self.queue.pop(0))

    def is_empty(self):
        return (len(self.queue) == 0)

    def size(self):
        return len(self.queue)

class Vertex(object):
    def __init__(self, label):
        self.label = label
        self.visited = False

    # determine if a vertex was visited
    def was_visited(self):
        return self.visited

    # determine the label of the vertex
    def get_label(self):
        return self.label

    # string representation of the vertex
    def __str__(self):
        return str(self.label)

class Graph(object):
    def __init__(self):
        self.Vertices = []
        self.adjMat = []

    # check if a vertex already exists in the graph
    def has_vertex(self, label):
        nVert = len(self.Vertices)
        for i in range(nVert):
            if (label == (self.Vertices[i]).get_label()):
                return True
        return False

    # given a label get the index of a vertex
    def get_index(self, label):
        nVert = len(self.Vertices)
        for i in range(nVert):
            if (label == (self.Vertices[i]).get_label()):
                return i
        return -1

    # add a Vertex with a given label to the graph
    def add_vertex(self, label):
        if (not self.has_vertex(label)):
            self.Vertices.append(Vertex(label))

        # add a new column in the adjacency matrix
        nVert = len(self.Vertices)
        for i in range(nVert - 1):
            (self.adjMat[i]).append(0)

        # add a new row for the new vertex
        new_row = []
        for i in range(nVert):
            new_row.append(0)
        self.adjMat.append(new_row)

    # add weighted directed edge to graph
    def add_directed_edge(self, start, finish, weight=1):
        self.adjMat[start][finish] = weight

    #deletes a vertex from graph
    def delete_vertex(self, vertexLabel):
        vertex_idx = self.get_index(vertexLabel)
        nVert = len(self.Vertices)

        for x in range(nVert):
            for y in range(vertex_idx, nVert - 1):
                self.adjMat[x][y] = self.adjMat[x][y + 1]
            self.adjMat[x].pop()

        self.adjMat.pop(vertex_idx)

        for x in self.Vertices:
            if x.label == vertexLabel:
                self.Vertices.remove(x)

    # determine if a directed graph has a cycle
    def has_cycle(self):
        nVert = len(self.Vertices)
        for v in range(nVert):
            # Create Stack
            theStack = Stack()

            # set Vertex as visited
            (self.Vertices[v]).visited = True
            theStack.push(v)

            # Similar to DFS
            while not theStack.is_empty():
                # get adj unvisited v
                u = self.cyclehelp(theStack,nVert)
                #Cycle Help returns 3 scenarios, -1 means that it got past both if statements, -2 means that the vertex was vistied and inside stack
                #otherwise it returns value
                if u < 0:
                    if u == -1:
                        u = theStack.pop()
                    if u == -2:
                        nVert = len(self.Vertices)
                        for i in range(nVert):
                            (self.Vertices[i]).visited = False
                        return True
                else:
                    (self.Vertices[u]).visited = True
                    theStack.push(u)

            # Reset Flags of vertices
            nVert = len(self.Vertices)
            for i in range(nVert):
                (self.Vertices[i]).visited = False
        return False

    #functions really similar to get adjacent, but using a stack it checks for cycle
    def cyclehelp(self, stack, nVert):
        s = stack.peek()
        for i in range(nVert):
            if self.adjMat[s][i] > 0 and (self.Vertices[i]).was_visited():
                if stack.is_inside(i):
                    return -2
            if self.adjMat[s][i] > 0 and not (self.Vertices[i]).was_visited():
                return i
        return -1

    # return a list of vertices after a topological sort
    def toposort(self):
        topo_visit = []
        dellist = []
        while len(self.Vertices) != 0:
            idx = 0
            while idx < len(self.Vertices):
                has_visit = False
                vertex = self.Vertices[idx].label
                for i in range(len(self.Vertices)):
                    if self.adjMat[i][idx] == 1:
                        has_visit = True
                        break
                if has_visit:
                    idx += 1
                else:
                    topo_visit.append(vertex)
                    dellist.append(vertex)
                    idx += 1
            while len(dellist) != 0:
                self.delete_vertex(dellist[0])
                dellist.pop(0)
        return topo_visit


def main():
    # create a Graph object
    theGraph = Graph()

    # open file for reading
    file = open("topo.txt", "r")

    # read the Vertices
    numVertices = int((file.readline()).strip())

    for i in range(numVertices):
        letter = (file.readline()).strip()
        theGraph.add_vertex(letter)

    # read the edges
    numEdges = int((file.readline()).strip())

    for i in range(numEdges):
        edge = (file.readline()).strip()
        edge = edge.split()
        start = theGraph.get_index(edge[0])
        finish = theGraph.get_index(edge[1])

        theGraph.add_directed_edge(start, finish)

    # test if a directed graph has a cycle
    if (theGraph.has_cycle()):
        print("The Graph has a cycle.")
    else:
        print("The Graph does not have a cycle.")

    # test topological sort
    if (not theGraph.has_cycle()):
        vertex_list = theGraph.toposort()
        print("\nList of vertices after toposort")
        print(vertex_list)


main()