import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.root.title("Cript CVA App")
        self.root.geometry("400x300")

        label = tk.Label(root, text="Hello, World!")
        label.pack(pady=20)