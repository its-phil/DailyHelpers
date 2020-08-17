import os
import sys
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, basePath: str, root: tk.Tk):
        super().__init__(root)
        self.basePath = basePath
        self.root = root
        self.setupWindow()
        self.pack()
        self.createElements()
        self.discoverRepos()

    def setupWindow(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(root.attributes, '-topmost', False)
        self.root.title("Git Helper")

    def createElements(self):
        self.toolBar = tk.Frame(self)
        self.toolBar.pack(side="top", fill="x", expand=True)

        self.showBranchesButton = tk.Button(
            self.toolBar, text="show branches", command=self.showBranches)
        self.showBranchesButton.pack(side="left")

        self.pullAllButton = tk.Button(
            self.toolBar, text="pull all", command=self.pullAll)
        self.pullAllButton.pack(side="left")

        self.repoList = tk.Frame(self.root, bg="yellow")
        self.repoList.pack(fill="both", expand=True)

    def discoverRepos(self):
        print("Discovering repositories...")

        self.gitRepos = []
        for dir in os.listdir(self.basePath):
            sys.stdout.write(f"   Analyzing '{dir}'")
            candidate = os.path.join(self.basePath, dir)
            if ".git" in os.listdir(candidate):
                print(" is a git repo.")
                self.gitRepos.append({"name": dir, "path": candidate})
            else:
                print(" is not a git repo.")

    def showBranches(self):
        print("Showing branches")

    def pullAll(self):
        print("Pulling all repos")


if __name__ == "__main__":
    # Check the command line arguments
    if(len(sys.argv) < 2):
        raise Exception("Please provide the base path as the first argument")

    basePath = sys.argv[1]
    print(f"Opening application for basepath '{basePath}'...")

    root = tk.Tk()
    app = Application(basePath=basePath, root=root)
    # app.mainloop()
