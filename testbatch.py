import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=300, bg="deep sky blue")
canvas.pack()

label = tk.Label(root, text="Hello World", font=("Arial", 20))
canvas.create_window(150, 150, window=label)

root.mainloop()