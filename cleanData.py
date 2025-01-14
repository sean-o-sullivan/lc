
# This csv was used to remove unnecessary data from the csvs, run from the command line

# /Users/sean/Desktop/lc/rawRegionalData.csv

import sys
import os

def clean(csvPath):
    print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~\nWe are now cleaning the csv at {csvPath}!\n~~~~~~~~~~~~~~~~~~~~~~~~~~")

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        csvPath = sys.argv[1]
        if os.path.isfile(csvPath):
            print("File exists!")
        else:
            raise Exception("File doesn't exist at this path!")
        clean(csvPath)
    else:
        raise Exception("You need to give me the filepath of the csv to clean as an argument!")
        