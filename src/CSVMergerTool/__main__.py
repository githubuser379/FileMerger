import datetime
import os
import endpointAttrFile
import settings

### This tool merges multiple CSV files that share values in a specified column. It searches
### for matching values between the two files in the chosen column.  If a match is found, the tools
### adds all remaining data in row to the CSV Output File.

print("Welcome to the CSV Merger Tool! This tool allows users to merge data from CSV files that contain "
      "columns with matching column fields [ie 'MAC Address' column] ")

# Import preconfigured settings
preconfiguredfilepathlist = settings.input_filepath_list

# Create master file object to store information from each file run through the script
masterObject = endpointAttrFile.endpointAttributeFile()

# Let the user change the default key attribute, if desired. Key attribute used to find common columns in each file
currentKeyAttribute = "macaddress"
keyAttribute = masterObject.changeKeyattributePrompt(currentKeyAttribute)

# Create and store file objects which contain filenames, filepaths, column names & dictionaries for each input file
while True:
    # Create endpointattributefile object
    fileobject =  endpointAttrFile.endpointAttributeFile()

    # Read preconfigured filepath list
    if len(preconfiguredfilepathlist) > 0:
        preconfiguredfileused = ""
        file = preconfiguredfilepathlist.pop(0)     
        preconfiguredfileused = input("The following file is preconfigured in the settings.py file: "+file+". Use this file?[y/n]: ")
        while preconfiguredfileused != 'y' and preconfiguredfileused != 'n':
            preconfiguredfileused = input("Input not valid. Please enter [y/n]: ")
        if preconfiguredfileused == "y":
            fileobject.filepath = file
            fileobject.filename = os.path.basename(fileobject.filepath)[:-4]
            print('File alias will be: '+fileobject.filename)
            fileobject.collectColumnlist()
            fileobject.keyattribute = keyAttribute
            fileobject.validateKeyAttribute()
            fileobject.createdict()
            masterObject.appendMasterKeyList(fileobject.filedict)
            masterObject.fileobjectlist.append(fileobject)
        elif preconfiguredfileused == 'n':
            pass

    # If no preconfigured files remaining, directly prompt the user for object filepath and filename alias
    if len(preconfiguredfilepathlist) == 0:
        # Prompt user for additional input files
        addFile = fileobject.filePrompt()
        if addFile == 'n':
            break
        else:
            fileobject.getFilepath()
            fileobject.getName()
            fileobject.collectColumnlist()
            fileobject.keyattribute = keyAttribute
            fileobject.validateKeyAttribute()
            fileobject.createdict()
            masterObject.appendMasterKeyList(fileobject.filedict)
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

# Set the filepath for the output file in the directory from which the script is run
scriptdirectory = os.path.abspath(os.path.dirname(__file__))
masterObject.filepath = scriptdirectory+"/OutputFiles/"+masterObject.filename

# Merge columns from each individual object in file object list into a single master column list
masterObject.createMasterColumnList()

# Add keys and associated attributes (csv row data) for each file object into master object dict
masterObject.createMasterDict()

# Write master object data to output CSV File
masterObject.createOutputCSVFile()


















