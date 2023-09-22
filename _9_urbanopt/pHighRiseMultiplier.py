import os
srcFldr = "wy-simplified-23-1-0"
targetFldr = "wy-simplified-23-1-0-HighRise"

# Create target directory & all intermediate directories if don't exists
if not os.path.exists(targetFldr):
    os.makedirs(targetFldr)

def modifyFile(srcFile):
    srcStr = "1,                       !- Multiplier"
    targetStr = "    28,                       !- Multiplier"
    newFile = ""
    lines = []  # Store previous lines for reference

    with open(srcFile, 'r') as file:
        for line in file:
            lines.append(line)  # Add the current line to the lines list
            if len(lines) >= 8:  # Ensure we have at least 7 lines to check
                if srcStr in line:
                    if 'Zone,' in lines[-8] and 'Building Story 2 ThermalZone' in lines[-7]:
                        newFile += targetStr + '\n'
                    else:
                        newFile += line
                else:
                    newFile += line
            else:
                newFile += line
    return newFile



# Copy files
for file in os.listdir(srcFldr):
    if file.endswith(".idf"):
        srcFile = os.path.join(srcFldr, file)
        targetFile = os.path.join(targetFldr, file)
        with open(targetFile, 'w') as file:
            file.write(modifyFile(srcFile))
        print("File copied: " + targetFile)
