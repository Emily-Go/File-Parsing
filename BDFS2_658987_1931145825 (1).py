##############################################################################
#In Part A, this program will parse files from a folder called "results"
#It will then use data (reformatted and summarized) from these files to create an output summary csv file
#In Part B, it will analyze file names in "results" and "results2", a different folder
#Part B will result in a summary text file
#This program uses relative paths
#"results" and "results2" must be placed in the same directory as this python file before running
##############################################################################

#######################################PART A#################################
##############################################################################

from os import listdir
results=listdir("results")  # Lists the files in the directory from "results"

output=open("OutputsFinal.csv","w") #Creates a csv file to write in later

# Below are columns to be written into the csv file
# Note: columns are written over multiple lines for readibility and then joined with commas
columnHeaders1=["Condition","Name", "Age", "Gender","Proportion of Hits, Proportion of Near Misses, Proportion Full Misses"]
columnHeaders2=["Mean Happiness Hits", "Mean Happiness Near Misses", "Mean Happiness Full Misses"]
columnHeaders3=["Mean Willingness Hits", "Mean Willingness Near Misses", "Mean Willingness Full Misses",]
columnHeaders4=["Minimum Happiness", "Minimum Happiness Index", "Maximum Happiness", "Maximum Happiness Index"]
columnsAll=columnHeaders1+columnHeaders2+columnHeaders3+columnHeaders4
columns=",".join(columnsAll)
output.write(columns+"\n")

# This loops goes through the files in the directory to remove duplicates by identifying files with the same IP Address
iPAddress=[]
unduplicatedFileNames=[]     # This is a new list of unique files
duplicates=[]                # This is a list of duplicates
for fileCSV in results:
    fileName="results/"+fileCSV
    file = open(fileName,'r')
    allLines = file.readlines()
    iP=allLines[2]           #This is where the IP falls in this file structure
    if iP not in iPAddress:
        iPAddress.append(iP)
        unduplicatedFileNames.append(fileName)
    else:
        duplicates.append(fileName)

# Now "unduplicatedFileNames" is the list operated on
# The counters below are to hold all fields that require counting
# This loop goes through each file line by line
# It takes out "\n" and the extra spaces and creates lists where there are commas
# Since commas separate fields, this allows us to access different fields per trial
# Each trial becomes a list made up of its different fields

for file in unduplicatedFileNames:
    file = open(file,'r')
    allLines = file.readlines()
    numberofTrials = 0
    hitsNumber = 0
    nearMissNumber = 0
    fullMissNumber = 0
    happinessHitsSum = 0
    happinessNearMissSum = 0
    happinessFullMissSum = 0
    willingnessHitsSum = 0
    willingnessNearMissSum = 0
    willingnessFullMissSum = 0
    happinessList = []
    for line in allLines:
        line = line.strip("\n").strip(" ").split(",") # This line strips "\n" and spaces while splitting fields by "," (it is done in one line for expedience)
        if len(line) == 3 and line[0].isalpha() == True: # This filters out the line with name, age, and gender by setting a conditional for a line with a length of 3 and alphabetic contents
            name = line[0]
            age = line[1]
            genderUncoded = line[2].lower()     # Makes gender lower case in case capitalization throws off the program
            if genderUncoded == "male":         # Recodes genders male and female as "1" and "2", respectively
                gender = "1"
            elif genderUncoded == "female":
                gender = "2"
# Line below sets a condition that filters out everything except the condition line by inluding only lines with a length of 1 and alphabetic contents
        elif line[0].isalpha()==True and len(line)==1:
            condition=line[0]
# Now operate on all trial lines by filtering for lines longer than 8 where index 1 is not alphabet
# Depending on the outcome of the trial, add results to the counters above
        elif len(line)>8 and line[1].isalpha()==False: # The not alphabet condition filters out the header line with "ships, aimed for, etc"
            numberofTrials = numberofTrials + 1
            happinessList.append(int(line[7]))      # Changed the happiness to integers so that they read properly when appending to "happinessList"
            if line[4] == "hit":
                hitsNumber = hitsNumber + 1
                happinessHitsSum = happinessHitsSum + float(line[7]) # float is used throughout to avoid inaccuracy caused by rounding to integers
                willingnessHitsSum = willingnessHitsSum + float(line[8])
            elif line[4] == "nearMiss":
                nearMissNumber = nearMissNumber + 1
                happinessNearMissSum = happinessNearMissSum + float(line[7])
                willingnessNearMissSum = willingnessNearMissSum + float(line[8])
            elif line[4] == "fullMiss":
                fullMissNumber = fullMissNumber + 1
                happinessFullMissSum = happinessFullMissSum + float(line[7])
                willingnessFullMissSum = willingnessFullMissSum + float(line[8])
# Use the counters above to calculate proportions, means, etc for each file
# Use the format method to limit the number of decimals points by overwriting some of the variable
    formProportion = "{0:.2f}" #This is the format that all outputs should take (2 decimal points)
    proportionHits = formProportion.format(hitsNumber / numberofTrials)
    proportionNearMiss = formProportion.format(nearMissNumber / numberofTrials)
    proportionFullMiss = formProportion.format(fullMissNumber / numberofTrials)
    meanHappinessHits = formProportion.format(happinessHitsSum / hitsNumber)
    meanHappinessNearMiss = formProportion.format(happinessNearMissSum / nearMissNumber)
    meanHappinessFullMiss = formProportion.format(happinessFullMissSum / fullMissNumber)
    meanWillingnessHits = formProportion.format(willingnessHitsSum / hitsNumber)
    meanWillingnessNearMiss = formProportion.format(willingnessNearMissSum / nearMissNumber)
    meanWillingnessFullMiss = formProportion.format(willingnessFullMissSum / fullMissNumber)
    maximumHappiness = max(happinessList)

# Note: Add 1 to the happiness indices because otherwise the program counts the first trial as trial 0
    maximumHappinessIndex = happinessList.index(maximumHappiness) + 1
    minimumHappiness = min(happinessList)
    minimumHappinessIndex = happinessList.index(minimumHappiness) + 1
# Separate the output variables into three output lists for readability purposes, separate all fields with commas
# Make sure all output contents are type string to allow for concatenation when writing
    outputVariables1 = [condition, str(name), str(age),gender, str(proportionHits), str(proportionNearMiss),
                        str(proportionFullMiss)]
    outputVariables2 = [str(meanHappinessHits), str(meanHappinessNearMiss), str(meanHappinessFullMiss),
                        str(meanWillingnessHits)]
    outputVariables3 = [str(meanWillingnessNearMiss), str(meanWillingnessFullMiss), str(minimumHappiness),
                        str(minimumHappinessIndex), str(maximumHappiness), str(maximumHappinessIndex)]
# Concatenate all the output variables and join with "," for easy writing
    outputVariablesAll = outputVariables1 + outputVariables2 + outputVariables3
    outputs = ",".join(outputVariablesAll)
# Write the csv file, putting "\n" after each participant file to create a new line in the csv file
    output.write(outputs+"\n")

output.close()



#######################################PART B#################################
##############################################################################

# Parts 1 and 2
# This loop goes through each file name in the results file, and adds that name to a count of Experiment A or B
# It then extracts the using the "." in the file names as a point of reference (date ends 6 characters before the "." and has 8 characters)
# Date is obtained as three parts for easy concatenation with a slash
# It then joins these parts of the dates together to form a single date where parts are divided by slashes
# It adds these full dates (dateFormatted) as a key in a dictionary of the dates if it's not already in it with a value of 1
# If the date is already in the dictionary, it adds 1 to its current value
experimentA=0
experimentB=0
numberTrialsinResults1=len(results)
date=[] #This variable is mostly to to check the dates are formatted properly before continuing with dictionaries of dates. Can print the variable to check
dictionaryOfDates={}
formattedDictionary=""
for name in results:
    if name[0:4]=="expA":
        experimentA+=1
    elif name[0:4]=="expB":
        experimentB+=1
    end=name.find(".")-6
    start=end-8
    dateOnly=name[start:end]
    datePartOne=dateOnly[0:2] # datePartOneis day
    datePartTwo=dateOnly[2:4] # datePartTwo is month
    datePartThree=dateOnly[4:] # datePartThree is year
    dateAllParts=[datePartOne,datePartTwo,datePartThree] # This is the full date without slashes
    dateFormatted="/".join(dateAllParts) #This is the full date with slashes
    date.append(dateFormatted)
    if dateFormatted not in dictionaryOfDates:
        dictionaryOfDates[dateFormatted] = 1
    else:
        dictionaryOfDates[dateFormatted] = dictionaryOfDates[dateFormatted] + 1
# This loop is to make the formatting nicer in the text file and to convert to string
for item in dictionaryOfDates:
    new = str(item) + ":" + str(dictionaryOfDates[item]) + '\n'
    formattedDictionary = formattedDictionary + new

# These variables calculate proportions in each experiment and use the format method to limit their decimal places in a message
proportionExpA=(experimentA/numberTrialsinResults1)
proportionExpB=(experimentB/numberTrialsinResults1)
form="{0:.2%} of the participants were in Experiment A and {1:.2%} were in Experiment B"
messageAboutProportions=form.format(proportionExpA,proportionExpB)+"\n"

# These commands create a message about dates using the format method
formDates="The number of participants per date is as follows:{0}"
messageAboutDates=formDates.format("\n"+formattedDictionary+"\n")


#Part 3
# First creates a variable to hold the list of file names in the directory from the results2 folder and creates empty lists
# Goes through the file names in results2 and sort them into "duplicates", "differentNames", or "same"
# Does this by setting the "end" of the file name to the period before the file type
# If the character before this period is a letter, then the file is a duplicate ("duplicate")
# If file name is also found in the results directory, it is the same file ("same")
# If the file is neither of the above, it is unique to results2 ("differentNames")
# Also creates lists of these variables to facilitate comparison between list lengths later on
from os import listdir
result_FileTwo_Names=listdir("results2")
duplicate=""
duplicatesList=[]
differentNames=""
differentList=[]
same=[]

#This loop identifies duplicate files by asking if the character before the "." in each file is a letter
#It then adds the file name to the appropriate list above
for file in result_FileTwo_Names:
    end=file.find(".")
    if file[end-1].isalpha()==True:
        duplicate+="\n"+file
        duplicatesList.append(file)
    elif file in results:
        same.append(file)
    else:
        differentNames+=file+"\n"
        differentList.append(file)

# Format the messages comparing results and results2 folders for easier incorporation into the text file
# The "\n"s added to the messages formats the output better in the csv
formMessage="The names of files that are in second list (results2.zip) but not in the original list (results.zip) and are not duplicates are:"+"\n"+"{}"+"\n"
messageAboutNewItems=formMessage.format(differentNames)
formSecondMessage="The names of the files that are in the second list with extra characters that are duplicates and thus should be deleted at a later stage are: {}"+"\n"
messageAboutDuplicates=formSecondMessage.format (duplicate)

#Compare the length of the "results" directory to length of the "results2" directory once duplicates and new files are subtracted
lengthOfOriginalList=len(results)
lengthOfOtherListRedacted=len(result_FileTwo_Names)-len(duplicatesList)-len(differentList)
if lengthOfOriginalList==lengthOfOtherListRedacted:
    resultOfCheck="The difference is the lists is accounted for by the duplicates and different names."
else:
    resultOfCheck="These lists are still different. Look at them again."


# Write the text file containing all the previous messages generated. The "\n" are added for better spacing
summary=open ("SummaryMessage.txt","w")
summary.write(messageAboutProportions+"\n"+messageAboutDates+"\n"+messageAboutNewItems+"\n"+messageAboutDuplicates+"\n"+resultOfCheck)


summary.close()