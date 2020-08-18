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
        self.fgError = "red"
        self.fgLogHeading = "blue"
        self.fontRepo = "Consolas 12"
        self.fontLogHeading = "Consolas 11 bold"
        self.fontLogMessage = "Consolas 10"


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

        self.contentFrame = tk.Frame(self.root)
        self.contentFrame.pack(fill="both", expand=True)

        self.repoList = tk.LabelFrame(self.contentFrame, text="Repositories")
        self.repoList.place(relwidth=.5, relheight=1)

        self.logView = tk.LabelFrame(self.contentFrame, text="Log")
        self.logView.place(relx=.5, relwidth=.5, relheight=1)

    def listRepoDirs(self):
        return [
            d for d in (os.path.join(self.basePath, d1) for d1 in os.listdir(self.basePath))
            if os.path.isdir(d)
        ]

    def discoverRepos(self):
        print("Discovering repositories...")

        # Collect data on the repositories in the given base directory
        self.gitRepos = []
        for dir in self.listRepoDirs():
            sys.stdout.write(f"   Analyzing '{dir}'")
            candidate = os.path.join(self.basePath, dir)
            try:
                if ".git" in os.listdir(candidate):
                    print(" is a git repo.")
                    self.gitRepos.append(
                        {"name": dir, "path": candidate, "branch": "---"})
                else:
                    print(" is not a git repo.")
            except Exception as e:
                print(f" error occurred: '{str(e)}'")

    def updateCurrentBranches(self):
        for repo in self.gitRepos:
            try:
                r = Repository(repo["path"])
                repo["branch"] = r.head.shorthand
            except Exception as e:
                repo["branch"] = f"ERROR: {str(e)}"

    def updateRepoList(self):
        # Display the repositories in the repo list
        self.clearFrame(self.repoList)
        row = 0
        for repo in self.gitRepos:
            nameLabel = tk.Label(
                self.repoList, text=repo["name"], font=self.theme.fontRepo, padx=10)
            nameLabel.grid(row=row, column=0, sticky="W")

            branchLabel = tk.Label(
                self.repoList, text=repo["branch"], fg=self.theme.fgOtherBranch, font=self.theme.fontRepo)
            if repo["branch"] == "master":
                branchLabel.configure(fg=self.theme.fgMasterBranch)
            if repo["branch"] == "develop":
                branchLabel.configure(fg=self.theme.fgDevelopBranch)
            if repo["branch"].startswith("ERROR: "):
                branchLabel.configure(fg=self.theme.fgError)
            branchLabel.grid(row=row, column=1, sticky="W")

            row += 1

    def showBranches(self):
        print("Showing branches")
        self.updateRepoList()

    def pullAll(self):
        print("Pulling all repos")

        self.clearFrame(self.logView)

        row = 0
        for repo in self.gitRepos:
            # Pull the repo and gather the result
            # result = subprocess.run(
            #    ['git', 'pull', repo['path']], stdout=subprocess.PIPE)

            result = subprocess.run(
                ['git', 'pull'], cwd=repo['path'], stdout=subprocess.PIPE)
            resultMsg = result.stdout.decode('utf-8')
            print(resultMsg)

            # Add a label for the repo name
            nameLabel = tk.Label(
                self.logView, text=repo["name"], font=self.theme.fontLogHeading, padx=10, fg=self.theme.fgLogHeading)
            nameLabel.grid(row=row, column=0, sticky="W")
            row += 1
            # Add a label for the message
            msgLabel = tk.Label(
                self.logView, text=resultMsg, font=self.theme.fontLogMessage, padx=10)
            msgLabel.grid(row=row, column=0, sticky="W")
            row += 1

            self.root.update()


if __name__ == "__main__":
    # Check the command line arguments
    if(len(sys.argv) < 2):
        raise Exception("Please provide the base path as the first argument")

    basePath = sys.argv[1]
    print(f"Opening application for basepath '{basePath}'...")

    root = tk.Tk()
    app = Application(basePath=basePath, root=root)
    app.mainloop()
