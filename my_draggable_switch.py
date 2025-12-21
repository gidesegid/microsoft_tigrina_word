import tkinter as tk
class DraggableSwitch(tk.Frame):
    def __init__(self, parent, title="Switch:", command=None, width=40, height=20, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.command = command
        self.width = width
        self.height = height
        self.radius = height // 2
        self.switch_on = False

        # Label (Title) aligned to the left
        self.label = tk.Label(self, text=title, font=("Arial", 10))
        self.label.pack(side="left", padx=5)

        # Canvas for switch
        self.canvas = tk.Canvas(self, width=width, height=height, bg="lightgray", highlightthickness=0)
        self.canvas.pack(side="right", padx=5)

        # Background (track)
        self.track = self.canvas.create_oval(0, 0, height, height, fill="gray", outline="gray")
        self.canvas.create_oval(width - height, 0, width, height, fill="gray", outline="gray")

        # Draggable knob
        self.knob = self.canvas.create_oval(1, 1, height - 1, height - 1, fill="white", outline="gray")

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.release_drag)

        self.update_switch()

    def start_drag(self, event):
        self.drag_start_x = event.x

    def on_drag(self, event):
        knob_x1, _, knob_x2, _ = self.canvas.coords(self.knob)
        dx = event.x - self.drag_start_x
        new_x1 = min(max(knob_x1 + dx, 1), self.width - self.height)
        self.canvas.move(self.knob, new_x1 - knob_x1, 0)

    def release_drag(self, event):
        knob_x1, _, knob_x2, _ = self.canvas.coords(self.knob)
        if (knob_x1 + knob_x2) / 2 > self.width / 2:
            self.switch_on = True
        else:
            self.switch_on = False
        self.update_switch()

        

    def update_switch(self):
        if self.switch_on:
            self.canvas.coords(self.knob, self.width - self.height, 1, self.width - 1, self.height - 1)
            self.canvas.itemconfig(self.track, fill="green", outline="green")
        else:
            self.canvas.coords(self.knob, 1, 1, self.height - 1, self.height - 1)
            self.canvas.itemconfig(self.track, fill="gray", outline="gray")

        if self.command:
            self.command(self.switch_on)
