
# This python file was used to remove unnecessary data from the csvs, run from the command line.
# /Users/247124/Desktop/lc/rawRegionalData.csv

import pandas as pd
import sys
import os

def clean(csvPath = 'rawGlobalData.csv'):
    
    # Verify that the csv does exist at this path
    if os.path.isfile(csvPath):
        print("File exists!")
            
        # Load CSV file from a URL
        df = pd.read_csv(csvPath)
            

        # ---------------------------------------------  Cleaning the Dataset  --------------------------------------------- 

        print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~\nWe are now cleaning the csv dataset located at: << {csvPath} >>!\n~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # Fortunately this IEA dataset is incredibly clean, and so all I need to do is some surface level cleaning. 

        
        # The raw csv features the followig columns: PUBLICATION,SCENARIO,CATEGORY,PRODUCT,FLOW,UNIT,REGION,YEAR,VALUE
        # Drop unnecessary columns

        # We can drop 'Publicaton' because it is the same in every row: World Energy Outlook 2024
        # Additionally, we can drop the 'Region' column as this csv only features the global data

        # Drop the unnecessary columns
        df = df.drop(['PUBLICATION', 'REGION'], axis=1)

        # Replace potential Nan's with 0
        df = df.fillna(0)

        
        # Save cleaned df to csv
        exportedCsv = 'cleanedGlobal.csv'
        df.to_csv(exportedCsv, index_label='rowID')

        cwd = os.getcwd()
        completePath = os.path.join(cwd, exportedCsv)
        
        print(f'\nDataset cleaneed!\n It has been saved at {completePath}')
    else:
        raise Exception("File doesn't exist at this path!")



# Main execution of the cleanData.py
if __name__ == '__main__':

        # Ensure that an argument is passed when the python file is run through the terminal
    if len(sys.argv) > 1:
        csvPath = sys.argv[1]

        clean(csvPath)
        
    else:
        print("\nAs you have not provided me with the csv filepath, I will default to the hardcoded location!\n")
        clean()

    

        
