import unittest
from ISETools.src.isetools.SharedServices.CSVoperations import *

class CSVTestCase(unittest.TestCase):

    def test_ValidFilePath(self):
        """Is the provided filepath valid?"""
        FileObject = csvfile()
        FileObject.filepath = "C:\\Users\JAOPC\PycharmProjects\ISETools\ISETools\src\isetools\SharedServices\Tests\TestCSVFile.csv"
        FileObject.store()
        self.assertTrue(FileObject.ValidCSVFile)

    def test_CreateMasterDict(self):
        """Can you create a successful dict from a given file"""
        FileObject = endpointAttributeFile()
        FileObject.filepath = "C:\\Users\JAOPC\PycharmProjects\ISETools\ISETools\src\isetools\SharedServices\Tests\TestCSVFile.csv"
        FileObject.collectColumnlist()
        FileObject.createdict()

        self.assertEqual(len(FileObject.file),len(FileObject.filedict)+1)

if __name__ == '__main__':
    unittest.main()





