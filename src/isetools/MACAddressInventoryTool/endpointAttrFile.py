from ISETools.src.isetools.SharedServices.CSVoperations import *
import os

# Includes network endpoint inventory specific values and functions
class endpointAttributeFile(csvfile):
    def __init__(self):
        super().__init__()
        # Define default base attribute
        self.keyattribute = "macaddress"
        self.fileobjectlist = []
        self.masterkeylist = []

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
        for key in self.masterkeylist:
            # Check to see if key exists in each object dictionary
            for object in self.fileobjectlist:
                if key in object.filedict:
                    # If so, check if key is already in the master object dictionary
                    if key in self.filedict:
                        # If a key has already been created in the master object dictionary,
                        # just add the attributes from the current file to the existing key
                        for attribute in object.filedict[key]:
                            self.filedict[key].append(attribute)
                    else:
                        # If a key does not exist in the master object dictionary, add the key
                        # and the associated attributes
                        self.filedict[key] = []
                        for attribute in object.filedict[key]:
                            self.filedict[key].append(attribute)
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
                row = [key]
                i = 0
                for attribute in self.filedict[key]:
                    if isinstance(attribute, list):
                        string = ";".join(attribute)
                        row.append(string)
                        i += 1
                    else:
                        row.append(attribute)
                outputFileWriter.writerow(row)