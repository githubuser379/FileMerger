from MACAddressInventoryTool.src.isetools.SharedServices.CSVoperations import *
from MACAddressInventoryTool.src.isetools.MACAddressInventoryTool.endpointAttrFile import *
import time
import datetime

### This tool merges multiple CSV files that share values in a specified column. It searches
### for matching values between the two files in the chosen column.  If a match is found, the tools
### adds all remaining data in row to the CSV Output File.

print("Welcome to the Endpoint Inventory Tool! This tool allows users to merge data from CSV files that contain "
      "columns with matching fields - 'key attributes'. ")

# Create master object to store information for each file run through the script
masterObject = endpointAttributeFile()

# Let the user change the default key attribute, if desired, used to match row values in each file
currentKeyAttribute = "macaddress"
keyAttribute = masterObject.changeKeyattributePrompt(currentKeyAttribute)

# Create and store file objects which contain filenames, filepaths, column names & dictionaries for each input file
while True:
    # Create endpointattributefile object
    fileobject = csvfile()

    # Prompt the user for object filepath and filename alias
    fileobject.getFilepath()
    fileobject.getName()

    # Parse provided filepath file for column names
    fileobject.collectColumnlist()

    # Ensure that file object is assigned the previously selected key attribute value
    fileobject.keyattribute = keyAttribute
    fileobject.validateKeyAttribute()

    # Create dictionary from file located at provided filepath. Add dictonary keys to master key list
    fileobject.createdict()

    # Add keys to master key list for later reference
    for key in fileobject.filedict:
        masterObject.appendMasterKeyList(fileobject.filedict)

    # Append csvfile object to master object list
    masterObject.fileobjectlist.append(fileobject)

    # Prompt user for additional input files
    addFile = fileobject.filePrompt()
    if addFile == 'n':
        break
    else:
        pass

# Set the key attribute value for the master object to the value provided by the user
masterObject.keyattribute = keyAttribute

#  Set the filename for the output file
dateTimeFormat = '%Y-%m-%d_%I%M%p'
currentTime = datetime.datetime.now()
masterObject.filename = currentTime.strftime(dateTimeFormat)+"_MergedCSVfile.csv"

# Set the filepath for the output file
currentdirectory = os.getcwd()
masterObject.filepath = currentdirectory+"/OutputFiles/"+masterObject.filename

# Merge each individual object in file object list into a single master object
masterObject.createrMasterColumnList()

# Add keys and associated attributes for each file object into master object dict
masterObject.createMasterDict()

# Write master object data to output CSV File
masterObject.createOutputCSVFile()


















