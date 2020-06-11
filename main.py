import tkinter as tk
import subprocess

font = "Arial 13"

class MainView(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        label = tk.Label(self, text="Broj čvorova(5-60):", font=font)
        label.place(x=10, y=20)

        vcmd = (self.register(self.onValidate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry = tk.Entry(self, validate="key", validatecommand=vcmd, font=font)
        self.entry.place(x=160, y=21)

        self.b1 = tk.Button(self, text="START", command=self.runAnimation, font=font, height=4, width=15)
        self.b1.place(x=110, y=90)

        self.errorPoruka = tk.StringVar()

        self.text = tk.Label(self, textvariable=self.errorPoruka, foreground='red', font=font)
        self.text.place(x=160, y=50)

        self.brojCvorova = 0

    def onValidate(self, d, i, P, s, S, v, V, W):
        if P == "":
            return True
        try:
            broj = int(P)
            if broj < 5 or broj > 60:
                self.errorPoruka.set("Pogrešan broj čvorova!")
            else:
                self.errorPoruka.set("")
            self.brojCvorova = broj
        except:
            self.bell()
            return False
            
        return True

    def runAnimation(self):
        if self.brojCvorova < 5 or self.brojCvorova > 60:
            self.errorPoruka.set("Pogrešan broj čvorova!")
        else:
            subprocess.run(["python3", "kruskal.py", str(self.brojCvorova)])

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Kruskal animacija")
    root.resizable(False, False)
    root.wm_geometry("360x200")
    root.mainloop()