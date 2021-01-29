import sys
import os
import shutil
from colorama import Fore, Back, Style

# Prerequesites:
# pip install colorama


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


def hasMatchingFile(fileName: str, imageFiles) -> os.DirEntry:
    for imageFile in imageFiles:
        if imageFile.name.split(".")[0].lower() == fileName.lower():
            return True
    return False


def hasMatchingSidecarFile(fileName: str, rawFiles) -> os.DirEntry:
    for rawFile in rawFiles:
        if rawFile.name.lower() == fileName.lower():
            return True
    return False


if len(sys.argv) != 2:
    printError("Please provide the root path to operate on.")
    quit(-1)

rootPath = sys.argv[1]
printOneStringArg("RAW file organizer starting in", rootPath, "...")

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
            printWarning("Skipping directory. There's nothing to do.", 1)
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
        for rawFile in rawFiles:
            fileName = rawFile.name.split(".")[0]
            if hasMatchingFile(fileName, imageFiles):
                rawFilesToMove.append(rawFile)

        # Determine sidecar files to be moved. A sidecar file is considered if there's a matching image file.
        # Remember that the sidecar files have the extension of the file they are sidecar to, i.e.
        # image.nef has image.nef.xmp and image.jpg has image.jpg.xmp.
        sidecarFilesToMove = []
        for sidecarFile in sidecarFiles:
            fileName = sidecarFile.name.split(".")[0] + "." + sidecarFile.name.split(".")[1]
            if hasMatchingSidecarFile(fileName, rawFiles):
                sidecarFilesToMove.append(sidecarFile)
        printTwoIntArg("There are", len(rawFilesToMove), "raw files and", len(sidecarFilesToMove), "sidecar files to move", 1)

        # Finally move the stuff around
        if len(rawFiles) - len(rawFilesToMove) != 0:
            printWarning(str(len(rawFiles) - len(rawFilesToMove)) + " raw files remain because there are no matching jpegs.", 1)
        if len(rawFilesToMove) == 0:
            printWarning("Skipping directory. No files to move left.", 1)
            continue

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
