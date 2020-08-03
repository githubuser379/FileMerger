from MACAddressInventoryTool.src.isetools.SharedServices.CSVoperations import *
import os

# Includes network endpoint inventory specific values and functions
class endpointAttributeFile(csvfile):
    def __init__(self):
        super().__init__()
        # Define default base attribute
        self.keyattribute = "macaddress"
        self.fileobjectlist = []
        self.masterkeylist = []
        self.sourcefilelist = []

    def appendMasterKeyList(self,dictionary):
        for key in dictionary:
            if key in self.masterkeylist:
                pass
            else:
                self.masterkeylist.append(key)

    def createrMasterColumnList(self):
        for object in self.fileobjectlist:
            for column in object.columnlist:
                if column.lower() == self.keyattribute:
                    pass
                else:
                    self.columnlist.append(object.filename + ":" + column)

    def createMasterDict(self):
        # For each key in the master key list
        for key in self.masterkeylist:
            # Check to see if key exists in each object dictionary
            for object in self.fileobjectlist:
                if key in object.filedict:
                    # If so, check if key is already in the master object dictionary
                    if key in self.filedict:
                        # If a key has already been created in the master object dictionary,
                        # just add the attributes from the current file to the existing key
                        i = 0
                        for attribute in object.filedict[key]:
                            ## First attribute is the source file; add to sourcefile list
                            if i == 0:
                                self.sourcefilelist.append(attribute)
                                i += 1
                            ## Add the rest of the attributes in the row into the master filedict
                            else:
                                self.filedict[key].append(attribute)
                                i += 1
                    else:
                        # If a key does not exist in the master object dictionary, add the key
                        # and the associated attributes
                        self.filedict[key] = []
                        i = 0
                        for attribute in object.filedict[key]:
                            ## First attribute is the source file; add to sourcefile list
                            if i == 0:
                                self.sourcefilelist.append(attribute)
                                i += 1
                            ## Add the rest of the attributes in the row into the master filedict
                            else:
                                self.filedict[key].append(attribute)
                                i += 1
                else:
                    # If current dictionary doesn't contain the key, fill in master object dictionary entries with "N/A"
                    # for the number of columns contained in that file
                    for i in range(len(object.columnlist)):
                        self.filedict[key].append("N/A")

    def createOutputCSVFile(self):
        with open(self.filepath, 'w', newline='', encoding='utf-8') as outputFile:
            # Add the column names to the first row of the output CSV File
            outputFileWriter = csv.writer(outputFile)
            firstRow = [self.keyattribute, "Source File"]
            for column in self.columnlist:
                firstRow.append(column)
            outputFileWriter.writerow(firstRow)
            # Add the rest of the rows to the output CSV File
            r = 0
            for key in self.filedict:
                if r % 20000 == 0:
                    print("Creating row", r)
                row = [key,[x for x in self.sourcefilelist]]
                i = 0
                for attribute in self.filedict[key]:
                    if isinstance(attribute, list):
                        string = ";".join(attribute)
                        row.append(string)
                        i += 1
                    else:
                        row.append(attribute)
                outputFileWriter.writerow(row)