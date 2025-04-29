from tkinter import *
from tkinter import messagebox
import threading
from time import sleep
from collections import defaultdict 
from math import sqrt
from random import seed, randint
import sys
import copy
import queue

seed()

root = Tk()
root.title("Kruskal animation")
root.resizable(False, False)
root.wm_geometry('1050x800')

background = "#494c52"
nodeTaken = "#248f1e"
nodeNotTaken = "white"
edgeTaken = "#c96a44"
nodeCheck = "red"
edgeCheck = "red"

font = "Arial 13"
fontButton = "Helvetica 9"

c = Canvas(root, height=800, width=800, bg=background)
c.pack(side=LEFT)

q = queue.Queue()

def stepBack():
    q.put("stepBack")

def speedUp():
    q.put("speedUp")

def slowDown():
    q.put("slowDown")

def pause():
    q.put("pause")

def play():
    q.put("play")


backButton = Button(root, text = "Step back", command = stepBack, anchor = W, font=fontButton)
backButton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
backButton_window = c.create_window(10, 10, anchor=NW, window=backButton)

speedUpButton = Button(root, text = "Speed up", command = speedUp, anchor = W, font=fontButton)
speedUpButton.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
speedUpButton_window = c.create_window(97, 10, anchor=NW, window=speedUpButton)

slowDownButton = Button(root, text = "Slow down", command = slowDown, anchor = W, font=fontButton)
slowDownButton.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
slowDownButton_window = c.create_window(142+7, 10, anchor=NW, window=slowDownButton)

pauseButton = Button(root, text = "Pause", command = pause, anchor = W, font=fontButton)
pauseButton.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
pauseButton_window = c.create_window(194+7, 10, anchor=NW, window=pauseButton)

playButton = Button(root, text = "Continue", command = play, anchor = W, font=fontButton)
playButton.configure(width = 6, activebackground = "#33B5E5", relief = FLAT)
playButton_window = c.create_window(246+7, 10, anchor=NW, window=playButton)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(root, height=800, width=200, font=font, yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT)

scrollbar.config(command=listbox.yview)

buttonFrame = Frame(root)
buttonFrame.pack(side=TOP, anchor=NE)

b1 = Button(buttonFrame, text="button")
b1.pack(side=TOP)

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

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.drawn = False

    def draw(self):
        if self.drawn == False:
            self.line = c.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, width=5, fill=edgeTaken)
            self.p1Oval = self.p1.draw(20, nodeTaken)
            self.p2Oval = self.p2.draw(20, nodeTaken)
            self.drawn = True

    def unDraw(self, fresh = False):
        if fresh == False:
            line = c.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, width=5, fill=edgeCheck)
            p1Oval = self.p1.draw(20, nodeCheck)
            p2Oval = self.p2.draw(20, nodeCheck)
            sleep(0.1)
            c.delete(line)
            c.delete(p1Oval[0])
            c.delete(p1Oval[1])
            c.delete(p2Oval[0])
            c.delete(p2Oval[1])

        if self.drawn:
            c.delete(self.line)
            c.delete(self.p1Oval[0])
            c.delete(self.p1Oval[1])
            c.delete(self.p2Oval[0])
            c.delete(self.p2Oval[1])
            self.drawn = False
            


class Graph: 
    def __init__(self, vertices, points): 
        self.V= vertices 
        self.points = points
        self.graph = []
        self.steps = []
        self.edges = []
        self.sleepTime = 10
        self.hasCompletedOnce = False
   
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

    def generateSteps(self):
        result = [] 
        i = 0 
        e = 0 
        parent = [] ; rank = [] 
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0) 
      
        while e < self.V -1 : 
            stateBefore = {
                'result': copy.deepcopy(result),
                'parent': copy.deepcopy(parent),
                'rank': copy.deepcopy(rank)
            }

            u,v,w =  self.graph[i] 

            x = self.find(parent, u) 
            y = self.find(parent, v) 

            if x != y: 
                e = e + 1     
                result.append([u,v,w]) 
                self.union(parent, rank, x, y)   
                
            self.steps.append({
                'stateBefore': stateBefore,
            })

            i = i + 1

        stateBefore = {
            'result': copy.deepcopy(result),
            'parent': copy.deepcopy(parent),
            'rank': copy.deepcopy(rank)
        }

        self.steps.append({
            'stateBefore': stateBefore
        })

    def KruskalMST(self): 
        i = 0 
        state = self.steps[i]['stateBefore']

        while len(state['result']) < self.V - 1 : 
            listbox.itemconfig(i+2, {'bg': '#ebebeb'})

            u,v,w =  self.graph[i] 
            p1 = self.points[u]
            p2 = self.points[v]
            testEdge = self.drawEdge(p1, p2, edgeCheck)
            testNode1 = p1.draw(20, nodeCheck)
            testNode2 = p2.draw(20, nodeCheck)
  
            sleep(self.sleepTime / 10)

            stateAfter = self.steps[i+1]['stateBefore']
            
            if len(state['result']) == len(stateAfter['result']):
                listbox.itemconfig(i+2, {'bg': 'white', 'fg': 'red'})
            else:
                self.edges[i].draw()
                listbox.itemconfig(i+2, {'bg': 'white', 'fg': 'green'})

            c.delete(testEdge)
            c.delete(testNode1[0])
            c.delete(testNode1[1])
            c.delete(testNode2[0])
            c.delete(testNode2[1])                

            fresh = i
            noAction = True

            paused = False
            if q.empty() == False:
                while q.empty() == False:
                    sleep(0.1)
                    action = q.get()
                    if action == "speedUp":
                        slowDownButton["state"] = NORMAL
                        if self.sleepTime == 4:
                            speedUpButton["state"] = DISABLED
                        if self.sleepTime >= 4:
                            self.sleepTime = self.sleepTime - 2
                    if action == "slowDown":
                        speedUpButton["state"] = NORMAL
                        if self.sleepTime == 14:
                            slowDownButton["state"] = DISABLED
                        if self.sleepTime <= 14:
                            self.sleepTime = self.sleepTime + 2
                    if action == "stepBack":
                        noAction = False
                        if i > 0:
                            if fresh == i:
                                self.edges[i].unDraw(fresh=True)
                            else:
                                self.edges[i].unDraw()
                            listbox.itemconfig(i+2, {'bg': 'white', 'fg': 'black'})
                            i = i - 1
                            listbox.itemconfig(i+2, {'bg': '#ebebeb', 'fg': 'black'})
                            paused = True
                    if action == "pause":
                        paused = True
                    if action == "play":
                        paused = False
            
            if noAction:
                i = i + 1
                state = self.steps[i]['stateBefore']
                if len(state['result']) == self.V - 1:
                    if self.hasCompletedOnce == False:
                        messagebox.showinfo('Kruskal animation', 'The algorithm is complete, but you can still go back through the steps.')
                        self.hasCompletedOnce = True
                    paused = True
            
            while paused == True:
                sleep(0.1)
                if q.empty() == False:
                    action = q.get()
                    if action == "speedUp":
                        slowDownButton["state"] = NORMAL
                        if self.sleepTime == 4:
                            speedUpButton["state"] = DISABLED
                        if self.sleepTime >= 4:
                            self.sleepTime = self.sleepTime - 2
                    if action == "slowDown":
                        speedUpButton["state"] = NORMAL
                        if self.sleepTime == 14:
                            slowDownButton["state"] = DISABLED
                        if self.sleepTime <= 14:
                            self.sleepTime = self.sleepTime + 2
                    if action == "stepBack":
                        if i > 0:
                            self.edges[i].unDraw()
                            listbox.itemconfig(i+2, {'bg': 'white', 'fg': 'black'})
                            i = i - 1
                            listbox.itemconfig(i+2, {'bg': '#ebebeb', 'fg': 'black'})
                            paused = True
                    if action == "pause":
                        paused = True
                    if action == "play":
                        if self.hasCompletedOnce == False or i < len(self.steps) - 1:
                            paused = False

            state = self.steps[i]['stateBefore']
  

def thread_function(n):
    points = []

    for i in range(0, n):
        valid = False
        while valid == False:
            x = Point(randint(70, 750), randint(70, 750), i)
            valid = True
            for j in points:
                if x.dist(j) < 50:
                    valid = False
                
        points.append(x)

    size =  n
    g = Graph(size, points)
    for i in range(0, size):
        g.points[i].draw(20, nodeNotTaken)
        for j in range(0, size):
            if i < j:
                g.addEdge(i, j, points[i].dist(points[j]))

    listbox.insert(END, "Unsorted edges:")
    listbox.insert(END, "(node1, node2) = distance")
    for node in g.graph:
        u,v,w = node
        listbox.insert(END, "("+str(u)+","+str(v)+") = "+str(round(w, 2)))
  
    messagebox.showinfo("Kruskal animation", "Edges are unsorted, they will now be sorted.")
    sleep(1)

    g.graph =  sorted(g.graph,key=lambda item: item[2]) 

    listbox.delete(0, END)
    listbox.insert(END, "Sorted edges:")
    listbox.insert(END, "(node1, node2) = distance")
    for node in g.graph:
        u,v,w = node
        g.edges.append(Edge(g.points[u], g.points[v]))
        listbox.insert(END, "("+str(u)+","+str(v)+") = "+str(round(w, 2)))
     
    g.generateSteps()

    g.KruskalMST() 

    print("finished")

        
numberOfVertices = int(sys.argv[1])

x = threading.Thread(target=thread_function, args=(numberOfVertices,))
x.daemon = True
x.start()

def on_closing():
    root.destroy()
    sys.exit()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
