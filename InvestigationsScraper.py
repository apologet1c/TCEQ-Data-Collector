import mechanize
import pandas as pd
import time

br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots.txt
br.set_handle_refresh(False)  # can sometimes hang without this per what someone on the internet says

AllData = pd.read_csv("active.csv") #read our csv file and import the data into pandas
RNList = AllData['RN']
pending = []

starttime = time.perf_counter()
count = 0
for x in RNList:
    response = br.open('https://www2.tceq.texas.gov/oce/penenfac/')
    
    #selects the first form on the page
    br.select_form(nr=0)
    
    #inputs the RN number into the form
    br["rn_txt"] = x 
    
    #submits the form
    pagehtml = br.submit().read() 
    try:
        #use pandas to extract the html datatables and turn them into dataframes
        result = pd.read_html(pagehtml) 
        pending.append(1)
    except:
        pending.append(0)
        pass
    count = count +1
    print(count)

print("Done") 

#adds to dataframe
AllData["PendingInvestigation"] = pending

#savefile
AllData.to_csv('output.csv', index=False)

#end perf tracker
endtime = time.perf_counter()
print(endtime-starttime)
