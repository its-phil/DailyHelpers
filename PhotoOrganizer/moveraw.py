import sys
import os
import shutil
from colorama import Fore, Back, Style

# Prerequesites:
# - pip install colorama


def printOneIntArg(prefix: str, arg: int, postfix: str, indent: int = 0):
    print("   " * indent + prefix + " " + Fore.CYAN + str(arg) + Fore.RESET + " " + postfix)


def printTwoIntArg(prefix: str, arg1: int, between: str, arg2: int, postfix: str, indent: int = 0):
    print("   " * indent + prefix + " " + Fore.CYAN + str(arg1) + Fore.RESET + " " + between + " " + Fore.CYAN + str(arg2) + Fore.RESET + " " + postfix)


def printThreeIntArg(prefix: str, arg1: int, between1: str, arg2: int, between2: str, arg3: int, postfix: str, indent: int = 0):
    print("   " * indent + prefix + " " + Fore.CYAN + str(arg1) + Fore.RESET + " " + between1 + " " + Fore.CYAN + str(arg2) + Fore.RESET + " " + between2 + " " + Fore.CYAN + str(arg3) + Fore.RESET + " " + postfix)


def printOneStringArg(prefix: str, arg: str, postfix: str, indent: int = 0):
    print("   " * indent + prefix + " '" + Fore.CYAN + arg + Fore.RESET + "' " + postfix)


def printNoArg(arg: str, indent: int = 0):
    print("   " * indent + arg)


def printOk(arg: str, indent: int = 0):
    print("   " * indent + Fore.GREEN + arg + Fore.RESET)


def printWarning(arg: str, indent: int = 0):
    print("   " * indent + Fore.YELLOW + arg + Fore.RESET)


def printError(arg: str, indent: int = 0):
    print("   " * indent + Fore.RED + arg + Fore.RESET)


def isRawFile(entry: os.DirEntry) -> bool:
    name = entry.name.lower()
    return name.endswith(".nef") or name.endswith(".dng") or name.endswith(".arw")


def isImageFile(entry: os.DirEntry) -> bool:
    name = entry.name.lower()
    return name.endswith(".jpg") or name.endswith(".jpeg")


def isSidecarFile(entry: os.DirEntry) -> bool:
    name = entry.name.lower()
    return name.endswith(".xmp")


# We define that a raw file has a matching image file if
# - there is an image file with the same file name (e.g. file1.dng and file1.jpg are a match)
# - there is a quick-view image file with the same file name (e.g. file1.dng and file1_qv.jpg are a match)
def hasMatchingImageFile(rawFileName: str, imageFiles) -> os.DirEntry:
    rawFileName = rawFileName.lower()
    rawQvFileName = rawFileName + "_qv"
    for imageFile in imageFiles:
        imageFileName = os.path.splitext(imageFile.name)[0].lower()
        if imageFileName == rawFileName or imageFileName == rawQvFileName:
            return True
    return False


def hasMatchingSidecarFile(fileName: str, rawFiles) -> os.DirEntry:
    for rawFile in rawFiles:
        if rawFile.name.lower() == fileName.lower():
            return True
    return False


# Process arguments
rootPath = ""
previewFsOperations = False
if len(sys.argv) == 2:
    rootPath = sys.argv[1]
elif len(sys.argv) == 3:
    if sys.argv[1] == "-p":
        previewFsOperations = True
    else:
        printError("Unknown option '" + sys.argv[1] + "'. Quitting.")
        quit(-1)
    rootPath = sys.argv[2]
else:
    printError("Please provide the root path to operate on.")
    quit(-1)

# Print a summary of the configuration options I understood
printOneStringArg("RAW file organizer starting in", rootPath, "...")
if previewFsOperations:
    printOk("Preview mode active. File system will not be modified.")
else:
    printWarning("Preview mode inactive. File system may be modified.")

summaryFilesMoved = 0

# Start the processing loop
for root, dirs, files in os.walk(rootPath):
    for dir in dirs:
        testPath = os.path.join(rootPath, dir)
        printOneStringArg("Processing path", testPath, "...")

        # Collect raw files and image files in the directory
        rawFiles = []
        imageFiles = []
        sidecarFiles = []
        for entry in os.scandir(testPath):
            if isRawFile(entry):
                rawFiles.append(entry)
            elif isImageFile(entry):
                imageFiles.append(entry)
            elif isSidecarFile(entry):
                sidecarFiles.append(entry)

        if len(rawFiles) == 0:
            printNoArg("Skipping directory. There's nothing to do.", 1)
            continue

        printThreeIntArg(
            "Found",
            len(rawFiles),
            "raw files,",
            len(imageFiles),
            "image files and",
            len(sidecarFiles),
            "sidecar files.",
            1,
        )

        # Determine raw files to be moved. A raw file is considered if there's a matching image file.
        rawFilesToMove = []
        sidecarFilesToMove = []
        for rawFile in rawFiles:
            fileName = os.path.splitext(rawFile.name)[0]
            if hasMatchingImageFile(fileName, imageFiles):
                rawFilesToMove.append(rawFile)

                # Determine sidecar files to be moved. A sidecar file is considered if there's a matching image file.
                # Remember that the sidecar files have the extension of the file they are sidecar to, i.e.
                # image.nef has image.nef.xmp and image.jpg has image.jpg.xmp.
                for sidecarFile in sidecarFiles:
                    fileName = os.path.splitext(sidecarFile.name)[0]
                    if hasMatchingSidecarFile(fileName, rawFiles):
                        sidecarFilesToMove.append(sidecarFile)
        printTwoIntArg("There are", len(rawFilesToMove), "raw files and", len(sidecarFilesToMove), "sidecar files to move", 1)

        # Finally move the stuff around
        if len(rawFiles) - len(rawFilesToMove) != 0:
            printWarning(str(len(rawFiles) - len(rawFilesToMove)) + " raw files will stay in their original location because there are no matching jpegs.", 1)
        if len(rawFilesToMove) == 0:
            printWarning("Skipping directory. No files to move left.", 1)
            continue

        summaryFilesMoved += len(rawFilesToMove)
        
        if not previewFsOperations:
            rawDir = os.path.join(testPath, "Raw")
            if os.path.isdir(rawDir):
                printWarning("Raw directory exists. We might overwrite existing data.", 1)
            else:
                os.mkdir(rawDir)

            for rawFile in rawFilesToMove:
                shutil.move(rawFile.path, rawDir)
            for sidecarFile in sidecarFilesToMove:
                shutil.move(sidecarFile.path, rawDir)
        printOk("Raw + sidecar files moved successfully.", 1)

    break

printOneIntArg("All done. I moved", summaryFilesMoved, "files.")