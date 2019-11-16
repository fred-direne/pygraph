import tkinter as tk

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()

        # canvas stuff
        self.canvas = tk.Canvas(self, height=800, width=800, bg="white")
        frame = tk.Frame(self)

        self._drag_data = {"x": 0, "y": 0, "item": None}
        self._edges = []
        self._node_count = 0

        self.canvas.bind("<Button-2>", self.draw_node)

        self.canvas.tag_bind("node", "<Button-3>", self.connect_node)
        self.canvas.tag_bind("node", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("node", "<B1-Motion>", self.on_token_motion)

        self.canvas.pack()

        self.line_start=None
    
        frame.pack(fill=tk.BOTH)

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location

        item = self.canvas.find_closest(event.x, event.y)[0]

        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        print(self.edges)

        '''
        for n in hue:
            tags = self.canvas.gettags(n)
            #print(tags)
            if str(item) in tags:
                print(self.canvas.coords(n))
                #self.asd.append({"x": 0, "y": 0, "item": n})
        '''

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

        # THIS IS WHERE I STOPPED
        # IT WORKS WITH ONE EDGE NOW DO WITH THE REST


        original = self.canvas.coords(self._edges[-1])
        self.canvas.coords(self._edges[-1], original[0],original[1], event.x, event.y)

        #print(self._drag_data["item"])


    def draw_node(self, event):
        x, y = event.x, event.y
        bbox = (x, y, x-50, y-50)
        self._node_count += 1
        self.canvas.create_oval(*bbox, fill="red", activefill="yellow", tags=("node", self._node_count))

    def connect_node(self, event):
        x,y=event.x,event.y
        #print(self.canvas.gettags(self.canvas.find_closest(x, y)[0])[1])

        if not self.line_start:
            self.line_start=(x,y)
            self.firstnode = self.canvas.gettags(self.canvas.find_closest(x, y)[0])[1]
        else:
            x_origin,y_origin=self.line_start
            self.line_start=None
            self.secondnode = self.canvas.gettags(self.canvas.find_closest(x, y)[0])[1]
            self._edges.append(self.canvas.create_line(x_origin, y_origin, x, y, tags=("edge", self.firstnode, self.secondnode)))

    def callback(self, event):
        self.draw(event.x, event.y)

    def draw(self, x, y):
        self.canvas.coords(self.circle, x-20, y-20, x+20, y+20)

app = App()
app.mainloop()
