import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageEditor:
    HANDLE_SIZE = 8  # size of corner handles

    def __init__(self, text_area):
        self.text_area = text_area
        self.images = []  # store all image frames

    def insert_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not file_path:
            return

        original_image = Image.open(file_path)
        original_image.thumbnail((200, 200))
        tk_image = ImageTk.PhotoImage(original_image)

        # Frame to hold image, handles, and delete button
        frame = tk.Frame(self.text_area, bd=0)
        frame.place(x=50, y=50)

        # Image label
        img_label = tk.Label(frame, image=tk_image)
        img_label.image = tk_image
        img_label.pack(fill="both", expand=True)

        # Store info
        img_data = {
            "frame": frame,
            "label": img_label,
            "image": original_image,
            "tk_image": tk_image,
            "handles": {},
            "delete_btn": None
        }
        self.images.append(img_data)

        # --- Resize handles ---
        for pos in ["nw", "ne", "sw", "se"]:
            handle = tk.Label(frame, bg="blue", width=1, height=1, cursor="size_nw_se")
            handle.place_forget()  # hide initially
            handle.bind("<Button-1>", lambda e, d=img_data, p=pos: self.start_resize(e, d, p))
            handle.bind("<B1-Motion>", lambda e, d=img_data, p=pos: self.resize_image(e, d, p))
            img_data["handles"][pos] = handle

        # --- Delete button "X" ---
        delete_btn = tk.Button(frame, text="X", bg="red", fg="white", bd=0,
                               command=lambda f=frame: self.delete_image(f))
        delete_btn.place_forget()  # hide initially
        delete_btn.lift()
        img_data["delete_btn"] = delete_btn

        # --- Drag ---
        img_label.bind("<Button-1>", lambda e, d=img_data: self.start_drag(e, d))
        img_label.bind("<B1-Motion>", lambda e, d=img_data: self.drag_image(e, d))

        # --- Hover events to show/hide handles and delete button ---
        def on_enter(event, d=img_data):
            # Show handles
            for pos, handle in d["handles"].items():
                x = 0 if "w" in pos else 1
                y = 0 if "n" in pos else 1
                handle.place(relx=x, rely=y, anchor=pos)
            # Show delete button
            d["delete_btn"].place(relx=1, rely=0, anchor="ne")
            d["delete_btn"].lift()

        def on_leave(event, d=img_data):
            # Hide handles and delete button
            for handle in d["handles"].values():
                handle.place_forget()
            d["delete_btn"].place_forget()

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

    # ---------------- Drag Functions ----------------
    def start_drag(self, event, img_data):
        img_data["drag_start_x"] = event.x
        img_data["drag_start_y"] = event.y

    def drag_image(self, event, img_data):
        dx = event.x - img_data["drag_start_x"]
        dy = event.y - img_data["drag_start_y"]
        frame = img_data["frame"]
        x = frame.winfo_x() + dx
        y = frame.winfo_y() + dy
        frame.place(x=x, y=y)

    # ---------------- Resize Functions ----------------
    def start_resize(self, event, img_data, corner):
        img_data["resize_start_x"] = event.x
        img_data["resize_start_y"] = event.y
        img_data["start_w"] = img_data["label"].winfo_width()
        img_data["start_h"] = img_data["label"].winfo_height()

    def resize_image(self, event, img_data, corner):
        dx = event.x - img_data["resize_start_x"]
        dy = event.y - img_data["resize_start_y"]

        # Determine resize based on corner
        if corner == "nw":
            new_w = max(20, img_data["start_w"] - dx)
            new_h = max(20, img_data["start_h"] - dy)
        elif corner == "ne":
            new_w = max(20, img_data["start_w"] + dx)
            new_h = max(20, img_data["start_h"] - dy)
        elif corner == "sw":
            new_w = max(20, img_data["start_w"] - dx)
            new_h = max(20, img_data["start_h"] + dy)
        elif corner == "se":
            new_w = max(20, img_data["start_w"] + dx)
            new_h = max(20, img_data["start_h"] + dy)

        # Resize PIL image and update label
        resized = img_data["image"].resize((new_w, new_h), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized)
        img_data["tk_image"] = tk_img
        img_data["label"].configure(image=tk_img)
        img_data["label"].image = tk_img

        # Update frame size to match image
        img_data["frame"].configure(width=new_w, height=new_h)

    # ---------------- Delete Function ----------------
    def delete_image(self, frame):
        for img_data in self.images:
            if img_data["frame"] == frame:
                img_data["frame"].destroy()
                self.images.remove(img_data)
                break
