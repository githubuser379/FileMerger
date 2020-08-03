import csv

class csvfile:
    def __init__(self):
        self.filepath = str()
        self.filename = str()
        self.file = []
        self.filedict = {}
        self.columnlist = []
        self.ValidCSVFile = None
        self.keyattribute = []
        self.keyattributefound = False

    def getFilepath(self):
        filepath = input("Please provide a filepath: ")
        try:
            str(filepath)
            self.filepath = filepath
        except:
            print("The filepath needs to be a string of characters. Please give a valid filepath")
            self.getFilepath()

    def store(self):
        if self.filepath[-4:] == ".csv":
            try:
                with open(self.filepath,newline='',encoding='utf-8') as file:
                    file_reader = csv.reader(file)
                    r = 0
                    for row in file_reader:
                        self.file.append(row)
                self.ValidCSVFile = True
            except:
                print("Cannot read file. Please ensure that you have provided a valid filepath.")
                self.store()
        else:
            self.ValidCSVFile = False
            print("File is not a 'csv' file. Please upload a valid 'csv' file")

    def getName(self):
        fileName = input("Please give the file a name: ")
        try:
            str(fileName)
            self.filename = fileName
        except:
            print("The name must be a string of characters. Please give a valid file name: ")
            self.getName()

    def collectColumnlist(self):
        with open(self.filepath,newline='',encoding='utf-8',errors='ignore') as file:
            CSVFile = csv.reader(file)
            for row in CSVFile:
                for column in row:
                    self.columnlist.append(column)
                #Stop after first row is collected. First row contains the column names
                break

    def filePrompt(self):
        promptUser = True
        while promptUser == True:
            filePrompt = input("Would you like to add another file? ['y' or 'n']: ")
            if filePrompt == "y" or filePrompt == "n":
                promptUser == False
                return filePrompt
            else:
                print("You did not choose 'y' or 'n'.  Please enter 'y' or 'n'")
                promptUser = True

    def validateKeyAttribute(self):
        while self.keyattributefound == False:
            self.searchColumnlistForKeyAttr()

    def createdict(self):
        with open(self.filepath,newline='',encoding='utf-8',errors='ignore') as file:
            CSVFile = csv.reader(file)
            rownumber = 0
            print("Parsing Rows from ",self.filename)
            for row in CSVFile:
                # Ignore column row
                if rownumber == 0:
                    rownumber += 1
                # For all data rows
                else:
                    # For logging purposes, print a line after every 20,000 entries that are processed
                    if rownumber % 20000 == 0:
                        print("Parsing Row", rownumber)
                    # Define key for row and associated rest of values in the row with this key
                    key = row[self.columnlist.index(self.keyattribute)].lower()
                    self.addKeyAttrsToFiledict(key, row)
                    rownumber += 1

    def searchColumnlistForKeyAttr(self):
        try:
            self.columnlist.index(self.keyattribute)
            self.keyattributefound = True
            print("Key attribute found in column list")
        except:
            print("Key attribute not found")
            newkeyattribute = self.chooseNewkeyattribute()
            self.keyattribute = newkeyattribute

    def addKeyAttrsToFiledict(self, key, row):
        if key in self.filedict:
            pass
        else:
            # Add key to filedict
            self.filedict[key] = []

            # Add source filename to filedict entry for current row
            #self.filedict[key].append([])
            self.filedict[key].append(self.filename)

            # For each column in a row, except for the row containing the key attribute, add attribute
            # values to Filedict
            numberofcolumns = len(self.columnlist)
            colnumber = 0
            for column in self.columnlist:
                if column.lower() == self.keyattribute.lower():
                    pass
                else:
                    if colnumber < numberofcolumns:
                        self.addAttribute(key, row, column)
                        colnumber += 1

    def addAttribute(self, key, row, column):
        if row[self.columnlist.index(column)].lower() == key.lower():
            pass
        else:
            self.filedict[key].append(row[self.columnlist.index(column)])

    def changeKeyattributePrompt(self, keyattributetype):
        changepreference = input("The default key attribute is '" + keyattributetype + "'. "
                                "Would you like to change the key attribute? [y/n]: ")
        if changepreference != "y" and changepreference != "n":
            print("Please choose 'y' or 'n'")
            self.changeKeyattributePrompt(keyattributetype)
        else:
            if changepreference == 'n':
                return keyattributetype.lower()
            if changepreference == 'y':
                newKeyAttribute = self.chooseNewkeyattribute()
                return newKeyAttribute.lower()

    def chooseNewkeyattribute(self):
        newkeyattribute = input("Please specify the attribute name (Must match a column name in CSV): ")
        return newkeyattribute





