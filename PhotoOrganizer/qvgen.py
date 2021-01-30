import sys
import os
import shutil
from colorama import Fore, Back, Style

# Prerequesites:
# - pip install colorama
# - install rawtherapee (e.g. apt install rawtherapee)
# - set rawtherapee default profile to "Standard Film Curve - ISO Medium" (Preferences > Image Processing > Default Processing Profile)


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


def hasMatchingQvFile(fileName: str, imageFiles) -> os.DirEntry:
    qvName = fileName.lower() + "_qv"
    for imageFile in imageFiles:
        if os.path.splitext(imageFile.name)[0].lower() == qvName:
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

# Start the processing loop
for root, dirs, files in os.walk(rootPath):
    for dir in dirs:
        testPath = os.path.join(rootPath, dir)
        printOneStringArg("Processing path", testPath, "...")

        # Collect raw files and image files in the directory
        rawFiles = []
        imageFiles = []
        for entry in os.scandir(testPath):
            if isRawFile(entry):
                rawFiles.append(entry)
            elif isImageFile(entry):
                imageFiles.append(entry)

        if len(rawFiles) == 0:
            printNoArg("Skipping directory. There's nothing to do.", 1)
            continue

        printTwoIntArg(
            "Found",
            len(rawFiles),
            "raw files,",
            len(imageFiles),
            "image files.",
            1,
        )

        # Determine raw files to be exported. A raw file is considered if there's a matching image file.
        rawFilesToProcess = []
        for rawFile in rawFiles:
            fileName = os.path.splitext(rawFile.name)[0]
            if not hasMatchingQvFile(fileName, imageFiles):
                rawFilesToProcess.append(rawFile)

        printOneIntArg("There are", len(rawFilesToProcess), "raw files to process.", 1)

        # Now the exporting stuff
        if len(rawFilesToProcess) == 0:
            printWarning("Skipping directory. No files to export left.", 1)
            continue

        for rawFile in rawFilesToProcess:
            inFile = rawFile.path
            outFile = os.path.splitext(rawFile.path)[0] + "_qv.jpg"
            cmd = 'rawtherapee-cli -q -Y -d -j75 -o "' + outFile + '" -c "' + inFile + '"'
            printOneStringArg("Executing", cmd, "", 1)
            if not previewFsOperations:
                result = os.system(cmd)
                if result == 0:
                    printOk(" Export successful.", 1)
                else:
                    printError("Export failed: " + str(result), 1)
            else:
                printOk("PREVIEW MODE. COMMAND NOT EXECUTED.", 1)

    break
