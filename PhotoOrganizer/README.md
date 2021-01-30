PhotoOrganizer
===

This is a collection of scripts to manage my photos. 
The collection contains the following scripts:
- <span class="command">adjustdates</span>
- <span class="command">moveraw</span>
- <span class="command">qvgen</span>

### General Concepts

- All scripts are called from the `DailyHelpers/PhotoOrganizer` folder. They expect their working directory as command line argument.

### File Organization
My files are organized as follows:
|Level 1|Level 2|Level 3|Level 4|Name|Description|
|--|--|--|--|--|--|
|`2021`||||Year Folder|All photos taken in the given year.|
||`2021-01-01 event`|||Event Folder|All photos taken at the given date and event (location, occasion).|
|||`Raw`||Raw Folder|Contains all raw files of the event that either have a full-size JPG export or a quick-view JPG export.|
||||`file1.dng`<br>`file2.dng`|
|||`FsExport`||Full-size Export Folder|Contains all full-size JPG export files of the raw files in the event.<br>*Note: this could also be the JPG files from the camera if both formats are saved simultaneously.*|
||||`file3.jpg`|
|||`file1_qv.jpg`<br>`file2_qv.jpg`<br>`file3_qv.jpg`||Quick-view files|Low-quality exported files of either the raw file in the `Raw` or the `FsExport` directory.|

## adjustdates

### Description
> This script is not yet implemented.

Read the files' EXIF information and set the file date to the value of the "date taken" property.

### Typical Call
```
```

## moveraw

### Description
Move raw files to a separate "Raw" directory. The script scans the first level of sub-directories in the given root directory, so it should be executed on the Year Folder.

Raw files are only copied if there's a matching JPG file. Darktable's sidecar are also moved if their matching raw file is moved.

### Call Syntax
```
python3 moveraw.py [-p] <working directory>
```
Options:
- `-p`: preview. Print what the script would do but don't modify the file system.

### Call Examples
```
python3 moveraw.py ~/Data/Pictures/Photography/2021
```

## qvgen

### Description

Generate quick-view images from raw files. The script uses `rawtherapee` to generate low-quality JPG images that can be quickly viewed.

> Current limitation: the script does not export files in `Raw` folders yet!

### Call Syntax
```
python3 qvgen.py <working directory>
```

### Call Examples
```
python3 qvgen.py ~/Data/Pictures/Photography/2021
```

<style>
h2, .command { color: #01bc75; }
</style>