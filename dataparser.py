import pandas as pd

AllData = pd.read_csv("RNs_final.csv") #read our csv file and import the data into pandas
REIDList = AllData['REG_ENT_ID'] #pull out RNs from the dataframe and drop it into a list

#initialize lists to hold what we're looking for
count = 0
activeflags = [] 
industrycodenumbers = []
industrycodelabels = []
activepermitnamelist = []
inactivepermitnamelist = []

for x in REIDList:
    
    filename = "C:/Users/Sharkfin/TCEQ Scraper/" + str(x) + ".html"

    with open(filename, "r") as text_file:
        rawhtml = text_file.read()

        #lets check to see if anything exists
        try:
            tables = pd.read_html(rawhtml)

        #If not? We'll just set everything to "N/A"    
        except: 
            activeflags.append(-1)
            industrycodenumbers.append(['N/A'])
            industrycodelabels.append(['N/A'])
            activepermitnamelist.append(['N/A'])
            inactivepermitnamelist.append(['N/A'])
            count = count +1
            continue
 
        #check if industry codes exist
        try:
            indcodes = pd.DataFrame(tables[1])
            codes = indcodes.loc[:, "Code"].values.tolist()
            codelabels = indcodes.loc[:, "Name"].values.tolist()
            
        #no? we'll just set industry codes data to N/A    
        except:
            codes = ['N/A']
            codelabels = ['N/A']
            pass
    
        #check if permits table exists
        try:
            permitlist = tables[2]

            #make lists of true/false values 
            activedf = permitlist.loc[:, 'ID\xa0Status'] == 'ACTIVE'
            permitdf = permitlist.loc[:, 'ID\xa0Type'] == 'PERMIT'
   
            #create lists of values because I don't know how to manipulate dataframes
            permitnames = permitlist.loc[:, 'Program'].values.tolist()
            activedf = activedf.values.tolist()
            permitdf = permitdf.values.tolist()
            activelist = []
            inactivelist = []
            
	    #Let's see if anything's active at all and set the flag accordingly
            if any(activedf):
                activeflags.append(1)
            else:
                activeflags.append(0)
            
	    #now lets sort and dump the data on permits into lists
            for i, val in enumerate(activedf):
                if activedf[i] is True and permitdf[i] is True:
                    activelist.append(permitnames[i])

                if activedf[i] is False and permitdf[i] is True:
                    inactivelist.append(permitnames[i])

	#if permits table doesn't exist at all or something goes wrong, set everything to N/A.
        except:
            activelist = ['N/A']
            inactivelist = ['N/A']
            activeflags.append(-1)
            pass

    #append results to the list for later!
    activepermitnamelist.append(activelist)
    inactivepermitnamelist.append(inactivelist)    
    industrycodenumbers.append(codes)
    industrycodelabels.append(codelabels)
    
    #counter that counts every 100 so I can see where we're at
    count = count +1
    if count % 100 == 0:
        print(count)
    else:
        continue

#add everything to the dataframe AllData and send to csv
AllData["Active?"] = activeflags
AllData["ActivePermits"] = activepermitnamelist
AllData["HistoricalPermits"] = inactivepermitnamelist
AllData["IndustryCodeNumber"] = industrycodenumbers
AllData["IndustryCodeLabel"] = industrycodelabels
AllData.to_csv('output.csv', index=False)
