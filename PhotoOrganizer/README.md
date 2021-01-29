PhotoOrganizer
===

This is a collection of scripts to manage my photos. 
The collection contains the following scripts:
- adjustdates
- moveraw

### General Concepts

- All scripts are called from the `DailyHelpers/PhotoOrganizer` folder. They expect their working directory as command line argument.

## adjustdates

### Description
> This script is not yet implemented.

Read the files' EXIF information and set the file date to the value of the "date taken" property.

### Typical Call
```
```

## moveraw

### Description
Move raw files to a separate "Raw" directory. The script scans the first level of sub-directories in the given root directory, so it should be executed on the year folder.

Raw files are only copied if there's a matching JPG file. Darktable's sidecar are also moved if their matching raw file is moved.

### Call Syntax
```
python3 moveraw.py <working directory>
```

### Call Examples
```
python3 moveraw.py ~/Data/Pictures/Photography/2021
```