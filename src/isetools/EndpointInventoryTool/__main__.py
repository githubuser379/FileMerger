import time
import datetime
import sys
import os
import endpointAttrFile

### This tool merges multiple CSV files that share values in a specified column. It searches
### for matching values between the two files in the chosen column.  If a match is found, the tools
### adds all remaining data in row to the CSV Output File.

print("Welcome to the Endpoint Inventory Tool! This tool allows users to merge data from CSV files that contain "
      "columns with matching column fields [ie 'MAC Address' column] ")

# Create master file object to store information from each file run through the script
masterObject = endpointAttrFile.endpointAttributeFile()

# Let the user change the default key attribute, if desired. Key attribute used to find common columns in each file
currentKeyAttribute = "macaddress"
keyAttribute = masterObject.changeKeyattributePrompt(currentKeyAttribute)

# Create and store file objects which contain filenames, filepaths, column names & dictionaries for each input file
while True:
    # Create endpointattributefile object
    fileobject =  endpointAttrFile.endpointAttributeFile()

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
scriptdirectory = os.path.abspath(os.path.dirname(__file__))
masterObject.filepath = scriptdirectory+"/OutputFiles/"+masterObject.filename

# Merge columns from each individual object in file object list into a single master column list
masterObject.createMasterColumnList()

# Add keys and associated attributes (csv row data) for each file object into master object dict
masterObject.createMasterDict()

# Write master object data to output CSV File
masterObject.createOutputCSVFile()


















