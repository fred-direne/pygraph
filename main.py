import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import Graph as graph

# middle-click: create node
# double left-click: delete node
# right click on node: create edge
# left-click hold: drag node

# mostrar o output tmb nas janelas, tipo o caminho no dfs etc
# dfs(0) na draw_dfs, deixa o user escolher ou deixa assim?
# save and open functions

# save functions: define how i'm going to save the graph : FRED

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("PyGraph")
        #configuring and adding the menu bar
        menu=tk.Menu(self)
        file_menu=tk.Menu(menu,tearoff=0)
        file_menu.add_command(label="New file",command=self.clear_canvas)
        file_menu.add_command(label="Open",command=self.choose_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save",command=self.save_file)
        menu.add_cascade(label="File",menu=file_menu)
        algorithm_menu=tk.Menu(menu,tearoff=0)
        algorithm_menu.add_command(label="Is Eulerian", command=self.draw_eulerian)
        algorithm_menu.add_command(label="Depth-first Search (DFS)", command=self.draw_dfs)
        algorithm_menu.add_command(label="Hamiltonian Circuit", command=self.draw_ham)
        algorithm_menu.add_command(label="Prim's Algorithm", command=self.draw_prim)

        #algorithm_menu.add_command(label="[TEST] export AdjMatrix", command=self.export_adjmatrix)
        #algorithm_menu.add_command(label="[TEST] export Canvas Graph", command=self.export_graph)
        #algorithm_menu.add_command(label="[TEST] load Canvas Graph", command=self.load_graph)
        #algorithm_menu.add_command(label="[TEST] Clear Canvas (new file)", command=self.clear_canvas)

        menu.add_cascade(label="Algorithm",menu=algorithm_menu)
        menu.add_command(label="About",command=self.about)
        menu.add_command(label="Quit",command=self.quit)
        self.config(menu=menu)

        self.canvas = tk.Canvas(self, height=600, width=800, bg="white")
        frame = tk.Frame(self)

        # used for dragging vertices
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # variables
        self._edges = [] # contains reference for every edge created
        self._edgeText = dict()
        self._nodes = [] # contains reference for every node created
        self._nodeText = dict()
        self._leftEdges = dict() # used to update edge position on moving a vertex :: index = edge ref, value = node ref of the leftmost end of the edge
        self._rightEdges = dict() # used to update edge position on moving a vertex :: index = edge ref, value = node ref of the rightmost end of the edge
        self._node_count = -1
        self.line_start=None
        self._selectedEdge = None # reference for when you click an edge to edit its weight

        # binds

        # if double button to delete node glitches switch to keyboard
        #self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        #self.canvas.bind("<Key>", self.delete_node)

        self.canvas.bind("<Button-2>", self.draw_node)
        self.canvas.tag_bind("edge", "<ButtonPress-1>", self.open_edge_window)
        self.canvas.tag_bind("node", "<Double-Button-1>", self.delete_node)
        self.canvas.tag_bind("node", "<Button-3>", self.connect_node)
        self.canvas.tag_bind("node", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("node", "<B1-Motion>", self.on_token_motion)

        self.canvas.pack(fill="both", expand=True)
        frame.pack(fill="both", expand=True)

    def generate_graph(self):
        g = graph.Graph(0)
        for v in self._nodes:
            g.addVertex()
        for e in self._edges:
            left = self._nodes.index(self._leftEdges[e]) # left node index
            right = self._nodes.index(self._rightEdges[e]) # right node index
            weight = int(self.canvas.gettags(e)[1])
            g.addEdge(left, right, weight)
        return g
    
    def draw_eulerian(self):
        g = self.generate_graph()
        result = g.isEulerian()
        if result == 2:
            messagebox.showinfo("Is Eulerian Result", "This is an Eulerian Graph")
        elif result == 1:
            messagebox.showinfo("Is Eulerian Result", "This is a Semi-Eulerian Graph")
        else:
            messagebox.showinfo("Is Eulerian Result", "This is not an Eulerian Graph")  

    def draw_dfs(self):
        # creates second Canvas window
        self.dfswindow = tk.Toplevel(self)
        self.dfswindow.title("DFS Result")
        self.dfscanvas = tk.Canvas(self.dfswindow, height=600, width=800, bg="white")
        self.dfscanvas.pack(fill="both", expand=True)

        g = self.generate_graph()
        g.dfs(0)
        marked = list()

        for i in range(len(g.result)):
            for j in range(i, len(g.result)):
                if g.result[i][j] > 0:
                    #print("Edge found at: (%d, %d, w=%d)" % (i, j, g.result[i][j]))
                    for e in self._edges:
                        if (self._leftEdges[e] == self._nodes[i] and self._rightEdges[e] == self._nodes[j]) or self._leftEdges[e] == self._nodes[j] and self._rightEdges[e] == self._nodes[i]:
                            marked.append(e)

        # draws everything based on canvas.find_all
        for element_id in self.canvas.find_all():
            item_type = self.canvas.type(element_id)
            if item_type == "text":
                item_text = self.canvas.itemcget(element_id, "text")
                bbox = self.canvas.coords(element_id)
                self.dfscanvas.create_text(bbox[0], bbox[1], fill="black", font="Helvetica 10 bold", text=item_text)
            elif item_type == "oval":
                item_tags = self.canvas.gettags(element_id)
                bbox = self.canvas.bbox(element_id)
                if element_id in marked:
                    color = "red"
                else:
                    color = "#808080"
                if item_tags[0] == "node":
                    self.dfscanvas.create_oval(*bbox, fill="#77c777", tags=("node", int(item_tags[1])))
                else:
                    self.dfscanvas.create_oval(*bbox, fill='',outline=color, width=3, tags=("edge", int(item_tags[1]), "loop"))
            elif item_type == "line":
                item_tags = self.canvas.gettags(element_id)
                bbox = self.canvas.coords(element_id)
                if element_id in marked:
                    color = "red"
                else:
                    color = "#808080"
                self.dfscanvas.create_line(bbox[0], bbox[1], bbox[2], bbox[3], fill=color, width=3, tags=("edge", int(item_tags[1])))

    def draw_ham(self):
        g = self.generate_graph()
        isHamiltonian = g.hamCycle()

        if isHamiltonian:
            # creates second Canvas window
            self.hamwindow = tk.Toplevel(self)
            self.hamwindow.title("Hamiltonian Circuit Result")
            self.hamcanvas = tk.Canvas(self.hamwindow, height=600, width=800, bg="white")
            self.hamcanvas.pack(fill="both", expand=True)
            marked = list()

            for i in range(len(g.result)):
                for j in range(i, len(g.result)):
                    if g.result[i][j] > 0:
                        #print("Edge found at: (%d, %d, w=%d)" % (i, j, g.result[i][j]))
                        for e in self._edges:
                            if (self._leftEdges[e] == self._nodes[i] and self._rightEdges[e] == self._nodes[j]) or self._leftEdges[e] == self._nodes[j] and self._rightEdges[e] == self._nodes[i]:
                                marked.append(e)

            # draws everything based on canvas.find_all
            for element_id in self.canvas.find_all():
                item_type = self.canvas.type(element_id)
                if item_type == "text":
                    item_text = self.canvas.itemcget(element_id, "text")
                    bbox = self.canvas.coords(element_id)
                    self.hamcanvas.create_text(bbox[0], bbox[1], fill="black", font="Helvetica 10 bold", text=item_text)
                elif item_type == "oval":
                    item_tags = self.canvas.gettags(element_id)
                    bbox = self.canvas.bbox(element_id)
                    if element_id in marked:
                        color = "red"
                    else:
                        color = "#808080"
                    if item_tags[0] == "node":
                        self.hamcanvas.create_oval(*bbox, fill="#77c777", tags=("node", int(item_tags[1])))
                    else:
                        self.hamcanvas.create_oval(*bbox, fill='',outline=color, width=3, tags=("edge", int(item_tags[1]), "loop"))
                elif item_type == "line":
                    item_tags = self.canvas.gettags(element_id)
                    bbox = self.canvas.coords(element_id)
                    if element_id in marked:
                        color = "red"
                    else:
                        color = "#808080"
                    self.hamcanvas.create_line(bbox[0], bbox[1], bbox[2], bbox[3], fill=color, width=3, tags=("edge", int(item_tags[1])))
        else:
            messagebox.showinfo("Hamiltonian Circuit Result", "No Hamiltonian Circuit found")

    def draw_prim(self):
        # creates second Canvas window
        self.primwindow = tk.Toplevel(self)
        self.primwindow.title("Prim's Algorithm Result")
        self.primcanvas = tk.Canvas(self.primwindow, height=600, width=800, bg="white")
        self.primcanvas.pack(fill="both", expand=True)

        g = self.generate_graph()
        g.primMST()
        marked = list()

        for i in range(len(g.result)):
            for j in range(i, len(g.result)):
                if g.result[i][j] > 0:
                    #print("Edge found at: (%d, %d, w=%d)" % (i, j, g.result[i][j]))
                    for e in self._edges:
                        if (self._leftEdges[e] == self._nodes[i] and self._rightEdges[e] == self._nodes[j]) or self._leftEdges[e] == self._nodes[j] and self._rightEdges[e] == self._nodes[i]:
                            marked.append(e)

        # draws everything based on canvas.find_all
        for element_id in self.canvas.find_all():
            item_type = self.canvas.type(element_id)
            if item_type == "text":
                item_text = self.canvas.itemcget(element_id, "text")
                bbox = self.canvas.coords(element_id)
                self.primcanvas.create_text(bbox[0], bbox[1], fill="black", font="Helvetica 10 bold", text=item_text)
            elif item_type == "oval":
                item_tags = self.canvas.gettags(element_id)
                bbox = self.canvas.bbox(element_id)
                if element_id in marked:
                    color = "red"
                else:
                    color = "#808080"
                if item_tags[0] == "node":
                    self.primcanvas.create_oval(*bbox, fill="#77c777", tags=("node", int(item_tags[1])))
                else:
                    self.primcanvas.create_oval(*bbox, fill='',outline=color, width=3, tags=("edge", int(item_tags[1]), "loop"))
            elif item_type == "line":
                item_tags = self.canvas.gettags(element_id)
                bbox = self.canvas.coords(element_id)
                if element_id in marked:
                    color = "red"
                else:
                    color = "#808080"
                self.primcanvas.create_line(bbox[0], bbox[1], bbox[2], bbox[3], fill=color, width=3, tags=("edge", int(item_tags[1])))

    def export_graph(self):
        # exporta matriz de adjacencia
        # exporta posicao de cada vertice

        # para pegar a posicao do vertice
        for vertice in self._nodes:
            print(self.canvas.coords(vertice))

    
    def load_graph(self, adjmatrix, coordvertices):

        am = list()
        cv = list()

        strs = adjmatrix.replace('[','').split('],')
        lists = list(map(int, s.replace(']','').split(',')) for s in strs)
        for i in lists:
            am.append([ int(x) for x in i ])
                
        strs = coordvertices.replace('[','').split('],')
        lists = list(map(float, s.replace(']','').split(',')) for s in strs)
        for i in lists:
            cv.append([ float(x) for x in i ])

        for node in cv:
            bbox = (node[0], node[1], node[2], node[3])
            self._node_count += 1
            self._nodes.append(self.canvas.create_oval(*bbox, fill="#77c777", activefill="#90EE90", tags=("node", self._node_count)))
            self._nodeText[self._nodes[-1]] = self.canvas.create_text(node[0]+20, node[1]+20, fill="black", font="Helvetica 10 bold", text=self._node_count)

        for i in range(len(am)):
            for j in range(i, len(am)):
                if am[i][j] > 0:
                    #print("Edge found at: (%d, %d, w=%d)" % (i, j, am[i][j]))
                    
                    # FALTA MEXER NESTA PARTE AQUI PARA TERMINAR O LOAD

                    x, y = event.x, event.y
                            x_origin, y_origin = self.line_start
                            self.line_start = None
                            
                            # check if the edge created is a loop
                            if self.firstnode == self.canvas.find_closest(x, y)[0]:
                                # draws an oval instead of a line
                                x1,y1,x2,y2 = self.canvas.coords(self.firstnode)
                                edge = self.canvas.create_oval(x2-15, y2-15, x2-70, y2-70, fill='',outline="#808080", activeoutline="red", width=3, tags=("edge", 1, "loop"))
                                self.canvas.tag_lower(edge)

                                # saves the edge reference
                                self._edges.append(edge)
                                self._edgeText[self._edges[-1]] = self.canvas.create_text(x2-70, y2-75, fill="black", font="Helvetica 12 bold", text="1")
                            else:
                                # not a loop -> draw a line connecting both selected nodes
                                edge = self.canvas.create_line(x_origin, y_origin, x, y, fill="#808080", activefill="red", width=3, tags=("edge", 1))
                                self.canvas.tag_lower(edge)

                                # saves the edge reference
                                self._edges.append(edge)

                                # calculating position for the edge text
                                int_x = (x_origin + x) / 2
                                int_y = (y_origin + y) / 2
                                self._edgeText[self._edges[-1]] = self.canvas.create_text(int_x-15, int_y-15, fill="black", font="Helvetica 12 bold", text="1")

                            # used to update edge position when dragging a node
                            self._leftEdges[edge] = self.firstnode
                            self._rightEdges[edge] = self.canvas.find_closest(x, y)[0]        
                        

        
    def clear_canvas(self):
        self.canvas.delete("all")
        self._edges = []
        self._edgeText = dict()
        self._nodes = []
        self._nodeText = dict()
        self._leftEdges = dict()
        self._rightEdges = dict()
        self._node_count = -1
        self.line_start=None
        self._selectedEdge = None

    def export_adjmatrix(self):
        g = self.generate_graph()

        # change this print to a return and format it like
        # [0 0 0]
        # [0 0 0]
        # [0 0 0]
        print(g.adjMatrix)

    #functions of the menubar
    def choose_file(self):
        filetypes=(("Plain text files","*.txt"),
                    ("All files", "*"))
        filename=fd.askopenfilename(title="Open file",
                initialdir="/",
                filetypes=filetypes)
        if filename:
            print(filename)
            file = open(filename,"r+")
            for line in file:
                if line.startswith("Adj:"):
                    adjmatrix = line[5:len(line)]
                elif line.startswith("Coord:"):
                    coordvertices = line[7:len(line)]
            self.load_graph(adjmatrix, coordvertices)
            file.close()

    def save_file(self):
        g = self.generate_graph()
        contents="Adj: "
        contents+=str(g.adjMatrix)
        contents+="\n"
        contents+="Coord: "

        coordlist = list()
        for vertice in self._nodes:
            coordlist.append(self.canvas.coords(vertice))
        contents += str(coordlist)

        # contents+="["
        # for vertice in self._nodes:
        #     contents+=str(self.canvas.coords(vertice))
        #     contents+=","
        # contents+="]"    
        new_file=fd.asksaveasfile(title="Save file",
                    defaultextension=".txt",
                    filetypes=(("Text files","*.txt"),))
        if new_file:
            new_file.write(contents)
            new_file.close()

    def quit(self):
        if messagebox.askyesno('Quit','Do you really want to quit?'):
            self.destroy()

    def about(self):
        messagebox.showinfo("PyGraph","\n PyGraph \n\n\n Version: 1.0 \n Github: https://github.com/ftdneves/graph_program.git")        

    def on_token_press(self, event):
        '''Beginning drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        # moving the text along with the node
        self.canvas.move(self._nodeText[self._drag_data["item"]], delta_x, delta_y)

        # moving the edges along with the node
        # if the edge end is the current node being dragged: update its position
        for e in self._leftEdges:
            if(self._leftEdges[e] == self._drag_data["item"]):
                if "loop" in self.canvas.gettags(e):
                    # if the edge is a loop use different method to move it and its text
                    self.canvas.move(e, delta_x, delta_y)
                    self.canvas.move(self._edgeText[e], delta_x, delta_y)
                else:
                    # if it is a normal edge get original coordinates and update half of it
                    original = self.canvas.coords(e)
                    self.canvas.coords(e, event.x, event.y, original[2], original[3])
                    # some really bad but functioning code to move edge weight text
                    int_x = (event.x + original[2]) / 2
                    int_y = (event.y + original[3]) / 2
                    self.canvas.coords(self._edgeText[e], int_x-15, int_y-15)
                
        for e in self._rightEdges:
            if(self._rightEdges[e] == self._drag_data["item"]):
                if "loop" in self.canvas.gettags(e):
                    # everything was already moved in the first for
                    pass
                else:
                    # if it is a normal edge get original coordinates and update half of it
                    original = self.canvas.coords(e)
                    self.canvas.coords(e, original[0], original[1], event.x, event.y)
                    # some really bad but functioning code to move edge weight text
                    int_x = (event.x + original[0]) / 2
                    int_y = (event.y + original[1]) / 2
                    self.canvas.coords(self._edgeText[e], int_x-15, int_y-15)

    def draw_node(self, event):
        # calculate node position placement
        x, y = event.x, event.y
        bbox = (x + 20, y + 20, x - 20, y - 20)
        # increments node count
        self._node_count += 1

        #draws node on canvas
        self._nodes.append(self.canvas.create_oval(*bbox, fill="#77c777", activefill="#90EE90", tags=("node", self._node_count)))

        #draws node text on canvas
        # nodeText = dictionary where index = last node created and value = text
        self._nodeText[self._nodes[-1]] = self.canvas.create_text(x, y, fill="black", font="Helvetica 10 bold", text=self._node_count)

    def connect_node(self, event):
        # get mouse position
        x, y = event.x, event.y

        if "edge" in self.canvas.gettags(self.canvas.find_closest(x, y)[0]):
            pass
        else:
            if not self.line_start:
                # this is the first click -> leftmost edge end
                # get mouse position and reference of the node selected
                self.line_start = (x,y)
                self.firstnode = self.canvas.find_closest(x, y)[0]
                # highlights the selected node
                self.canvas.itemconfig(self.firstnode, fill='#ff726f', activefill='#ff726f')
            else:
                # this is the second click -> rightmost edge end
                x_origin, y_origin = self.line_start
                self.line_start = None
                
                # check if the edge created is a loop
                if self.firstnode == self.canvas.find_closest(x, y)[0]:
                    # draws an oval instead of a line
                    x1,y1,x2,y2 = self.canvas.coords(self.firstnode)
                    edge = self.canvas.create_oval(x2-15, y2-15, x2-70, y2-70, fill='',outline="#808080", activeoutline="red", width=3, tags=("edge", 1, "loop"))
                    self.canvas.tag_lower(edge)

                    # saves the edge reference
                    self._edges.append(edge)
                    self._edgeText[self._edges[-1]] = self.canvas.create_text(x2-70, y2-75, fill="black", font="Helvetica 12 bold", text="1")
                else:
                    # not a loop -> draw a line connecting both selected nodes
                    edge = self.canvas.create_line(x_origin, y_origin, x, y, fill="#808080", activefill="red", width=3, tags=("edge", 1))
                    self.canvas.tag_lower(edge)

                    # saves the edge reference
                    self._edges.append(edge)

                    # calculating position for the edge text
                    int_x = (x_origin + x) / 2
                    int_y = (y_origin + y) / 2
                    self._edgeText[self._edges[-1]] = self.canvas.create_text(int_x-15, int_y-15, fill="black", font="Helvetica 12 bold", text="1")

                # used to update edge position when dragging a node
                self._leftEdges[edge] = self.firstnode
                self._rightEdges[edge] = self.canvas.find_closest(x, y)[0]

                # remove highlight from firstnode
                self.canvas.itemconfig(self.firstnode, fill="#77c777", activefill="#90EE90")

    def delete_node(self, event):
        x, y = event.x, event.y
        # finding the selected node and its text
        node = self.canvas.find_closest(x, y)[0]
        nodetext = self._nodeText[node]
        # deleting node from canvas and variables
        self.canvas.delete(node)
        self.canvas.delete(nodetext)
        self._nodes.remove(node)
        self._nodeText.pop(node)

        # searching and removing any edge bound to the selected node
        edgestoremove = list()

        for e in self._leftEdges:
            if(self._leftEdges[e] == node):
                if e not in edgestoremove:
                    edgestoremove.append(e)
        for e in self._rightEdges:
            if(self._rightEdges[e] == node):
                if e not in edgestoremove:
                    edgestoremove.append(e)
        
        for e in edgestoremove:
            self.canvas.delete(e)
            self.canvas.delete(self._edgeText[e])
            self._edges.remove(e)
            self._leftEdges.pop(e)
            self._rightEdges.pop(e)
            self._edgeText.pop(e)

    def open_edge_window(self, event):
        # get mouse position
        x, y = event.x, event.y
        # save edge reference
        self._selectedEdge = self.canvas.find_closest(x, y)[0]
        # draw window and form
        self.edgewindow = tk.Toplevel(self)
        self.edgewindow.geometry("400x200") 
        self.edgewindow.title("Edit Edge Weight")
        self.weight = tk.StringVar()
        self.weight.set(int(self.canvas.gettags(self._selectedEdge)[1]))
        tk.Label(self.edgewindow, text="Edge Weight").pack(padx=5,pady=2)
        tk.Entry(self.edgewindow, textvariable=self.weight).pack(padx=5,pady=2)
        tk.Button(self.edgewindow, text="Submit", command=self.submit).pack(padx=5,pady=2)
        tk.Button(self.edgewindow, text="Delete Edge", command=self.delete_edge).pack(padx=5,pady=2)
    
    def submit(self):
        if "loop" in self.canvas.gettags(self._selectedEdge):
            self.canvas.itemconfig(self._selectedEdge, tags=("edge", self.weight.get(), "loop"))
        else:
            self.canvas.itemconfig(self._selectedEdge, tags=("edge", self.weight.get()))
        self.canvas.itemconfigure(self._edgeText[self._selectedEdge], text=str(self.weight.get()))
        self.edgewindow.destroy()
    
    def delete_edge(self):
        self.canvas.delete(self._selectedEdge)
        self.canvas.delete(self._edgeText[self._selectedEdge])
        self._edges.remove(self._selectedEdge)
        self._leftEdges.pop(self._selectedEdge)
        self._rightEdges.pop(self._selectedEdge)
        self._edgeText.pop(self._selectedEdge)
        self.edgewindow.destroy()

app = App()
app.iconbitmap('resources/img/graph.ico')
app.mainloop()