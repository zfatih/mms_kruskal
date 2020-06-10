from tkinter import *
import threading
from time import sleep
from collections import defaultdict 
from math import sqrt
from random import seed, randint
import sys

seed()

root = Tk()
root.title("Kruskal animacija")
root.resizable(False, False)
root.wm_geometry('1050x800')

background = "#494c52"
nodeTaken = "#248f1e"
nodeNotTaken = "white"
edgeTaken = "#c96a44"
nodeCheck = "red"
edgeCheck = "red"

c = Canvas(root, height=800, width=800, bg=background)
c.pack(side=LEFT)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(root, height=800, width=200, font=20, yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT)

scrollbar.config(command=listbox.yview)
  
class Point:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
    
    def dist(self, p):
        return sqrt((self.x-p.x)**2+(self.y-p.y)**2)

    def draw(self, r, color):
        return [c.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill = color),
                c.create_text(self.x, self.y, font = "Times 20", text=str(self.index))]


class Graph: 
  
    def __init__(self,vertices, points): 
        self.V= vertices 
        self.points = points
        self.graph = []
   
    def addEdge(self,u,v,w): 
        self.graph.append([u,v,w]) 
  
    def find(self, parent, i): 
        if parent[i] == i: 
            return i 
        return self.find(parent, parent[i]) 
  
    def union(self, parent, rank, x, y): 
        xroot = self.find(parent, x) 
        yroot = self.find(parent, y) 
  
        if rank[xroot] < rank[yroot]: 
            parent[xroot] = yroot 
        elif rank[xroot] > rank[yroot]: 
            parent[yroot] = xroot 
  
        else : 
            parent[yroot] = xroot 
            rank[xroot] += 1

    def drawEdge(self, p1, p2, color):
        return c.create_line(p1.x, p1.y, p2.x, p2.y, width=5, fill=color)
  
    def KruskalMST(self): 
  
        result =[] 
  
        i = 0 
        e = 0 

        listbox.insert(END, "Nesortirane veze:")
        listbox.insert(END, "(cvor1, cvor2) = udaljenost")
        for node in self.graph:
            u,v,w = node
            listbox.insert(END, "("+str(u)+","+str(v)+") = "+str(round(w, 2)))
  
        sleep(2)

        self.graph =  sorted(self.graph,key=lambda item: item[2]) 

        listbox.delete(0, END)
        listbox.insert(END, "Sortirane veze:")
        listbox.insert(END, "(cvor1, cvor2) = udaljenost")
        for node in self.graph:
            u,v,w = node
            listbox.insert(END, "("+str(u)+","+str(v)+") = "+str(round(w, 2)))
  
        parent = [] ; rank = [] 
  
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0) 
      
        while e < self.V -1 : 
            listbox.itemconfig(i+2, {'bg': '#ebebeb'})
            u,v,w =  self.graph[i] 
            p1 = self.points[u]
            p2 = self.points[v]
            testEdge = self.drawEdge(p1, p2, edgeCheck)
            testNode1 = p1.draw(20, nodeCheck)
            testNode2 = p2.draw(20, nodeCheck)
            i = i + 1
            x = self.find(parent, u) 
            y = self.find(parent ,v) 
  
            sleep(1)

            if x != y: 
                e = e + 1     
                result.append([u,v,w]) 
                self.drawEdge(p1, p2, edgeTaken)
                self.union(parent, rank, x, y)   
                listbox.itemconfig(i+1, {'bg': 'white', 'fg': 'green'})
            else:
                listbox.itemconfig(i+1, {'bg': 'white', 'fg': 'red'})
                c.delete(testEdge)
                c.delete(testNode1[0])
                c.delete(testNode1[1])
                c.delete(testNode2[0])
                c.delete(testNode2[1])

            p1.draw(20, nodeTaken)
            p2.draw(20, nodeTaken) 
  

def thread_function(n):
    try:

        tacke = []

        for i in range(0, n):
            dobar = False
            while dobar == False:
                x = Point(randint(50, 750), randint(50, 750), i)
                dobar = True
                for j in tacke:
                    if x.dist(j) < 50:
                        dobar = False
                    
            tacke.append(x)

        size =  n
        g = Graph(size, tacke)
        for i in range(0, size):
            g.points[i].draw(20, nodeNotTaken)
            for j in range(0, size):
                if i < j:
                    g.addEdge(i, j, tacke[i].dist(tacke[j]))
        
        g.KruskalMST() 
    except:
        return
        
numberOrVerticies = int(sys.argv[1])

x = threading.Thread(target=thread_function, args=(numberOrVerticies,))
x.start()

def on_closing():
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
