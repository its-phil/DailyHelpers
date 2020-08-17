import os
import subprocess
import sys
import tkinter as tk
from pygit2 import Repository


class Theme:
    def __init__(self):
        self.fgMasterBranch = "blue"
        self.fgDevelopBranch = "green"
        self.fgOtherBranch = "orange"


class Application(tk.Frame):
    def __init__(self, basePath: str, root: tk.Tk):
        super().__init__(root)
        self.basePath = basePath
        self.root = root

        self.theme = Theme()

        self.setupWindow()
        self.pack()
        self.createElements()
        self.discoverRepos()
        self.updateCurrentBranches()
        self.updateRepoList()

    def setupWindow(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(root.attributes, '-topmost', False)
        self.root.title("Git Helper")

    def clearFrame(self, frame: tk.Frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def createElements(self):
        self.toolBar = tk.Frame(self)
        self.toolBar.pack(side="top", fill="x", expand=True)

        self.showBranchesButton = tk.Button(
            self.toolBar, text="show branches", command=self.showBranches)
        self.showBranchesButton.pack(side="left")

        self.pullAllButton = tk.Button(
            self.toolBar, text="pull all", command=self.pullAll)
        self.pullAllButton.pack(side="left")

        self.repoList = tk.Frame(self.root)
        self.repoList.pack(fill="both", expand=True)

    def discoverRepos(self):
        print("Discovering repositories...")

        # Collect data on the repositories in the given base directory
        self.gitRepos = []
        for dir in os.listdir(self.basePath):
            sys.stdout.write(f"   Analyzing '{dir}'")
            candidate = os.path.join(self.basePath, dir)
            if ".git" in os.listdir(candidate):
                print(" is a git repo.")
                self.gitRepos.append(
                    {"name": dir, "path": candidate, "branch": "---"})
            else:
                print(" is not a git repo.")

    def updateCurrentBranches(self):
        for repo in self.gitRepos:
            r = Repository(repo["path"])
            repo["branch"] = r.head.shorthand

    def updateRepoList(self):
        # Display the repositories in the repo list
        self.clearFrame(self.repoList)
        row = 0
        for repo in self.gitRepos:
            nameLabel = tk.Label(self.repoList, text=repo["name"])
            nameLabel.grid(row=row, column=0, sticky="W")

            branchLabel = tk.Label(
                self.repoList, text=repo["branch"], fg=self.theme.fgOtherBranch)
            if repo["branch"] == "master":
                branchLabel.configure(fg=self.theme.fgMasterBranch)
            if repo["branch"] == "develop":
                branchLabel.configure(fg=self.theme.fgDevelopBranch)
            branchLabel.grid(row=row, column=1, sticky="W")

            row += 1

    def showBranches(self):
        print("Showing branches")
        self.updateRepoList()

    def pullAll(self):
        print("Pulling all repos")

        repo = self.gitRepos[0]
        result = subprocess.run(
            ['git', 'pull', repo['path']], stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))


if __name__ == "__main__":
    # Check the command line arguments
    if(len(sys.argv) < 2):
        raise Exception("Please provide the base path as the first argument")

    basePath = sys.argv[1]
    print(f"Opening application for basepath '{basePath}'...")

    root = tk.Tk()
    app = Application(basePath=basePath, root=root)
    app.mainloop()
