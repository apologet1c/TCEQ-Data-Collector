import pandas as pd
import time
import requests

AllData = pd.read_csv("rnstesting.csv") #read our csv file and import the data into pandas
REIDList = AllData['REG_ENT_ID'].values.tolist() #pull out RNs from the dataframe and drop it into a list

for x in REIDList:
    starttime = time.perf_counter()
    url = 'https://www15.tceq.texas.gov/crpub/index.cfm?fuseaction=regent.showSingleRN&re_id=' + str(x)
    response = requests.get(url)
    rawhtml = response.text
    filename = str(x) + ".html"
    print(filename)
    with open(filename, "w") as text_file:
        print(rawhtml, file=text_file)
    endtime = time.perf_counter()    
    totaltime = endtime - starttime
    print("Finished getting " + str(x) + " in " + str(totaltime) + " seconds." )

else:
    print("Done!") 
