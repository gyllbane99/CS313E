#  File: TopoSort.py

#  Description:

#  Student Name: Brock Brennan

#  Student UT EID: btb989

#  Partner Name:

#  Partner UT EID:

#  Course Name: CS 313E

#  Unique Number:

#  Date Created:

#  Date Last Modified:

class Stack (object):
  def __init__ (self):
    self.stack = []

  # add an item to the top of the stack
  def push (self, item):
    self.stack.append (item)

  # remove an item from the top of the stack
  def pop (self):
    return self.stack.pop()

  # check the item on the top of the stack
  def peek (self):
    return self.stack[-1]

  # check if the stack if empty
  def is_empty (self):
    return (len (self.stack) == 0)

  # return the number of elements in the stack
  def size (self):
    return (len (self.stack))

class Queue (object):
  def __init__ (self):
    self.queue = []

  # add an item to the end of the queue
  def enqueue (self, item):
    self.queue.append (item)

  # remove an item from the beginning of the queue
  def dequeue (self):
    return (self.queue.pop(0))

  # check if the queue is empty
  def is_empty (self):
    return (len (self.queue) == 0)

  # return the size of the queue
  def size (self):
    return (len (self.queue))

  def peek(self):
    return self.queue[0]

class Vertex (object):
  def __init__ (self, label):
    self.label = label
    self.visited = False

  # determine if a vertex was visited
  def was_visited (self):
    return self.visited

  # determine the label of the vertex
  def get_label (self):
    return self.label

  # string representation of the vertex
  def __str__ (self):
    return str (self.label)



class Graph (object):
  def __init__ (self):
    self.Vertices = []
    self.adjMat = []

  # check if a vertex is already in the graph
  def has_vertex (self, label):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (label == (self.Vertices[i]).get_label()):
        return True
    return False

  # given the label get the index of a vertex
  def get_index (self, label):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (label == (self.Vertices[i]).get_label()):
        return i
    return -1

  # add a Vertex with a given label to the graph
  def add_vertex (self, label):
    if (not self.has_vertex (label)):
      self.Vertices.append (Vertex (label))

    # add a new column in the adjacency matrix
    nVert = len (self.Vertices)
    for i in range (nVert - 1):
      (self.adjMat[i]).append (0)

    # add a new row for the new vertex
    new_row = []
    for i in range (nVert):
      new_row.append (0)
    self.adjMat.append (new_row)

  # add weighted directed edge to graph
  def add_directed_edge (self, start, finish, weight = 1):
    self.adjMat[start][finish] = weight
  # get a list of immediate neighbors that you can go to from a vertex
  # return a list of indices or an empty list if there are none
  def get_neighbors (self, vertexLabel):

    neighbors = []

    for i in range(len(self.Vertices)):
      if self.adjMat[self.get_index(vertexLabel)][i] > 0:
        neighbors.append(self.Vertices[i].label)
    return neighbors

  # return an unvisited vertex adjacent to vertex v (index)
  def get_adj_unvisited_vertex (self, v):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (self.adjMat[v][i] > 0) and (not (self.Vertices[i]).was_visited()):
        return i
    return -1

  # do a depth first search in a graph
  def dfs (self, v):
    # create the Stack
    theStack = Stack ()

    # mark the vertex v as visited and push it on the Stack
    (self.Vertices[v]).visited = True
    print (self.Vertices[v])
    theStack.push (v)

    # visit all the other vertices according to depth
    while (not theStack.is_empty()):
      # get an adjacent unvisited vertex
      u = self.get_adj_unvisited_vertex (theStack.peek())
      if (u == -1):
        u = theStack.pop()
      else:
        (self.Vertices[u]).visited = True
        print (self.Vertices[u])
        theStack.push (u)

    # the stack is empty, let us rest the flags
    nVert = len (self.Vertices)
    for i in range (nVert):
      (self.Vertices[i]).visited = False

  # do a breadth first search in a graph starting at vertex v (index)
  def bfs (self, v):
        # create the Queue
    theQueue = Queue()

    # mark the vertex v as visited and enqueue it
    (self.Vertices[v]).visited = True
    print (self.Vertices[v])
    theQueue.enqueue(v)

    # visit all the other vertices according to breadth
    while (not theQueue.is_empty()):
      # get an adjacent unvisited vertex
      u = self.get_adj_unvisited_vertex (theQueue.peek())
      if (u == -1):
        u = theQueue.dequeue()
      else:
        (self.Vertices[u]).visited = True
        print (self.Vertices[u])
        theQueue.enqueue(u)

    # the queue is empty, let us rest the flags
    nVert = len (self.Vertices)
    for i in range (nVert):
      (self.Vertices[i]).visited = False

  # delete an edge from the adjacency matrix
  # delete a single edge if the graph is directed
  # delete two edges if the graph is undirected
  def delete_edge (self, fromVertexLabel, toVertexLabel):
      v1 = self.get_index(fromVertexLabel)
      v2 = self.get_index(toVertexLabel)
      if self.adjMat[v1][v2] == self.adjMat[v2][v1]:
        self.adjMat[v1][v2] = 0
        self.adjMat[v2][v1] = 0
      else:
        self.adjMat[v1][v2] = 0

  # delete a vertex from the vertex list and all edges from and
  # to it in the adjacency matrix
  def delete_vertex (self, vertexLabel):

    vertex_idx = self.get_index(vertexLabel)
    nVert = len(self.Vertices)

    for x in range(nVert):
      for y in range(vertex_idx,nVert - 1):
        self.adjMat[x][y] = self.adjMat[x][y+1]
      self.adjMat[x].pop()

    self.adjMat.pop(vertex_idx)

    for city in self.Vertices:
      if city.label == vertexLabel:
        self.Vertices.remove(city)

  # determine if a directed graph has a cycle
  # this function should return a boolean and not print the result
  def has_cycle (self):
    stack = Stack()

    nVert = len(self.Vertices)
    for i in range(nVert):
      if ((self.Vertices[i]).visited == False):
        if (self.hasCycleHelper(i, stack)):
          return True
    return False

  def hasCycleHelper(self, v, stack):
    # mark vertex v as visited and push it on the stack
    (self.Vertices[v]).visited = True
    stack.push(self.Vertices[v])

    for item in self.get_neighbors(self.Vertices[v]):
      if (item.visited == False):
        if (self.hasCycleHelper(item, stack) == True):
          return True
      elif (stack[item] == True):
        return True

    # reset the flags
    nVert = len(self.Vertices)
    for i in range(nVert):
      (self.Vertices[i]).visited = False

    # pop the top element from the stack
    stack.pop()
    return False

  # return a list of vertices after a topological sort
  # this function should not print the list
  def toposort(self):
    if not self.has_cycle():
      vertices = []
      while (len(self.Vertices) > 0):
        i = 0
        for item in self.adjMat:
          if (sum(self.adjMat[i]) == 0):
            vertices.insert(0, (self.Vertices[i]).label)
            self.delete_vertex((self.Vertices[i]).label)
          else:
            i += 1
    return vertices

def main():
  # create a Graph object
  theGraph = Graph()

  #Read in file
  file = open("topo.txt", "r")
  totalVert = int(file.readline().strip())
  #Read in all of the vertices and add them to the graph
  for vert in range(totalVert):
    vertex = str(file.readline())
    vertex = vertex.strip()
    theGraph.add_vertex(vertex)

  totaledge = int(file.readline().strip())
  for item in range(totaledge):
    edge = file.readline()
    edge = edge.strip()
    edge = edge.split()
    theGraph.add_directed_edge(edge[0],edge[1],1)

  # test if a directed graph has a cycle
  if (theGraph.has_cycle()):
    print ("The Graph has a cycle.")
  else:
    print ("The Graph does not have a cycle.")

  # test topological sort
  if (not theGraph.has_cycle()):
    vertex_list = theGraph.toposort()
    print ("\nList of vertices after toposort")
    print (vertex_list)

main()
