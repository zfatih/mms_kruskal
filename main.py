import tkinter as tk
import subprocess

font = "Arial 13"

class MainView(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        label = tk.Label(self, text="Number of nodes (5-60):", font=font)
        label.place(x=10, y=20)

        vcmd = (self.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry = tk.Entry(self, validate="key", validatecommand=vcmd, font=font)
        self.entry.place(x=195, y=21, width=100)

        self.b1 = tk.Button(self, text="START", command=self.runAnimation, font=font, height=4, width=15)
        self.b1.place(x=110, y=90)

        self.errorMessage = tk.StringVar()

        self.text = tk.Label(self, textvariable=self.errorMessage, foreground='red', font=font)
        self.text.place(x=160, y=50)

        self.numberOfNodes = 0

    def onValidate(self, d, i, P, s, S, v, V, W):
        if P == "":
            return True
        try:
            number = int(P)
            if number < 5 or number > 60:
                self.errorMessage.set("Invalid number of nodes!")
            else:
                self.errorMessage.set("")
            self.numberOfNodes = number
        except:
            self.bell()
            return False
            
        return True

    def runAnimation(self):
        if self.numberOfNodes < 5 or self.numberOfNodes > 60:
            self.errorMessage.set("Invalid number of nodes!")
        else:
            subprocess.run(["python", "kruskal.py", str(self.numberOfNodes)])

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Kruskal animation")
    root.resizable(False, False)
    root.wm_geometry("360x200")
    root.mainloop()
