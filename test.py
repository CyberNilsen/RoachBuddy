import tkinter as tk
from PIL import Image, ImageTk

def rotate_image(image, degrees):
    rotated_image = image.rotate(degrees)
    return rotated_image

window = tk.Tk()
label = tk.Label(window)
label.pack()

image_path = "RoachMove/finn.jpg"
pil_image = Image.open(image_path)

degrees_to_rotate = 143
rotated_pil_image = rotate_image(pil_image, degrees_to_rotate)
tk_image = ImageTk.PhotoImage(rotated_pil_image)
label.config(image=tk_image)
label.image = tk_image

window.mainloop()