# This script follows the idea from https://ayende.com/blog/4749/executing-tortoisegit-from-the-command-line
param($cmd)
& "C:\Program Files\TortoiseGit\bin\TortoiseGitProc.exe" /command:$cmd /path:.