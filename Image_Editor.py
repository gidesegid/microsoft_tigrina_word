import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io
import base64
import os
class ImageEditor:
    HANDLE_SIZE = 8  # size of corner handles

    def __init__(self, text_area):
        self.text_area = text_area
        self.images = []  # store all image frames
        # self.file_path=""

    def insert_image(self):
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
            )
            if not file_path:
                return
            file_name = os.path.basename(file_path)
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
                "image_name":file_name,
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
                                command=lambda f=frame,d=img_data: self.delete_image(f,d))
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
        for item in self.images:
            if item["image_name"]==img_data["image_name"]:
                img_data["drag_start_x"] = event.x
                img_data["drag_start_y"] = event.y

        imageInf=self.get_images_info()
        print("imageInf:",imageInf)

    def drag_image(self, event, img_data):
        for item in self.images:
            if item["image_name"]==img_data["image_name"]:
                dx = event.x - img_data["drag_start_x"]
                dy = event.y - img_data["drag_start_y"]
                frame = img_data["frame"]
                x = frame.winfo_x() + dx
                y = frame.winfo_y() + dy
                frame.place(x=x, y=y)

        self.get_images_info()

    # ---------------- Resize Functions ----------------
    def start_resize(self, event, img_data, corner):
        for item in self.images:
            if item["image_name"]==img_data["image_name"]:
                img_data["resize_start_x"] = event.x
                img_data["resize_start_y"] = event.y
                img_data["start_w"] = img_data["label"].winfo_width()
                img_data["start_h"] = img_data["label"].winfo_height()

    def resize_image(self, event, img_data, corner):
        for item in self.images:
            if item["image_name"]==img_data["image_name"]:
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
        imageInf=self.get_images_info()
        print("imageInf:",imageInf)

    # ---------------- Delete Function ----------------
    def delete_image(self, frame,image_data):
        for img_data in self.images:
             for item in self.images:
                if item["image_name"]==image_data["image_name"]:
                    if img_data["frame"] == frame:
                        img_data["frame"].destroy()
                        self.images.remove(img_data)
                        break
    
    def get_images_info(self):
        images_info = []
        for img_data in self.images:
            frame = img_data["frame"]
            width = img_data["label"].winfo_width()
            height = img_data["label"].winfo_height()

            # Resize the PIL image to current displayed size
            resized_image = img_data["image"].resize((width, height), Image.LANCZOS)

            img_base64 = self.pil_image_to_base64(resized_image)

            info = {
                "name":img_data["image_name"],
                "type": "image",
                # "data": img_base64,
                "x": frame.winfo_x(),
                "y": frame.winfo_y(),
                "width": width,
                "height": height
            }
            images_info.append(info)
        return images_info
    
    def pil_image_to_base64(self,pil_image):
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")  # save as PNG in memory
        buffer.seek(0)
        img_bytes = buffer.read()
        return base64.b64encode(img_bytes).decode("utf-8")  # get string
    
    def insert_image_from_base64(self, img_base64, x, y, width, height):
        img_bytes = base64.b64decode(img_base64)
        pil_image = Image.open(io.BytesIO(img_bytes))
        pil_image = pil_image.resize((width, height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Frame
        frame = tk.Frame(self.text_area, bd=0)
        frame.place(x=x, y=y)

        # Image label
        img_label = tk.Label(frame, image=tk_image)
        img_label.image = tk_image
        img_label.pack(fill="both", expand=True)

        # Store img_data
        img_data = {
            "frame": frame,
            "label": img_label,
            "image": pil_image,
            "tk_image": tk_image,
            "handles": {},
            "delete_btn": None
        }
        self.images.append(img_data)

        # Add resize handles, delete button, drag bindings as in insert_image
        self._create_handles_and_delete(img_data)