PowerShell Scripts for Handling Git Repos on Windows
===

The scripts can be called without parameter. Then they will use their current location as base path to check for git repos.
If called with parameter, the scripts wiill use this parameter as base path.

# Creating Shortcuts

When creating shortcuts in Windows explorer add powershell.exe and the base path as target. Example:
```
powershell.exe C:\git\DailyHelpers\PowerShell\PullAll.ps D:\
```
can be placed in `D:` and pull all repos found in `D:`.