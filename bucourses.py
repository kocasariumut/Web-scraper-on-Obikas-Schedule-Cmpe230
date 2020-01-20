import sys
import csv
import requests
import re
spamwriter = csv.writer(sys.stdout) # Creates the writing object
shortdept=["AD","ASIA","ASIA","ATA","AUTO","BIO","BIS","BM","CCS","CE","CEM","CET","CET","CHE","CHEM","CMPE","COGS","CSE","EC","ED","EE","EF","ENV","ENVT","EQE","ETM","FE","FLED","GED","GPH","GUID","HIST","HUM","IE","INCT","INT","INTT","INTT","LING","LL","LS","MATH","ME","MECA","MIR","MIR","MIS","PA","PE","PHIL","PHYS","POLS","PRED","PSY","SCED","SCED","SCO","SOC","SPL","SWE","SWE","TK","TKL","TR","TRM","TRM","WTR","XMBA","YADYOK"]
dept=["MANAGEMENT","ASIAN+STUDIES","ASIAN+STUDIES+WITH+THESIS","ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY","AUTOMOTIVE+ENGINEERING","MOLECULAR+BIOLOGY+%26+GENETICS","BUSINESS+INFORMATION+SYSTEMS","BIOMEDICAL+ENGINEERING","CRITICAL+AND+CULTURAL+STUDIES","CIVIL+ENGINEERING","CONSTRUCTION+ENGINEERING+AND+MANAGEMENT","COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY","EDUCATIONAL+TECHNOLOGY","CHEMICAL+ENGINEERING","CHEMISTRY","COMPUTER+ENGINEERING","COGNITIVE+SCIENCE","COMPUTATIONAL+SCIENCE+%26+ENGINEERING","ECONOMICS","EDUCATIONAL+SCIENCES","ELECTRICAL+%26+ELECTRONICS+ENGINEERING","ECONOMICS+AND+FINANCE","ENVIRONMENTAL+SCIENCES","ENVIRONMENTAL+TECHNOLOGY","EARTHQUAKE+ENGINEERING","ENGINEERING+AND+TECHNOLOGY+MANAGEMENT","FINANCIAL+ENGINEERING","FOREIGN+LANGUAGE+EDUCATION","GEODESY","GEOPHYSICS","GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING","HISTORY","HUMANITIES+COURSES+COORDINATOR","INDUSTRIAL+ENGINEERING","INTERNATIONAL+COMPETITION+AND+TRADE","CONFERENCE+INTERPRETING","INTERNATIONAL+TRADE","INTERNATIONAL+TRADE+MANAGEMENT","LINGUISTICS","WESTERN+LANGUAGES+%26+LITERATURES","LEARNING+SCIENCES","MATHEMATICS","MECHANICAL+ENGINEERING","MECHATRONICS+ENGINEERING","INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST","INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS","MANAGEMENT+INFORMATION+SYSTEMS","FINE+ARTS","PHYSICAL+EDUCATION","PHILOSOPHY","PHYSICS","POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS","PRIMARY+EDUCATION","PSYCHOLOGY","MATHEMATICS+AND+SCIENCE+EDUCATION","SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION","SYSTEMS+%26+CONTROL+ENGINEERING","SOCIOLOGY","SOCIAL+POLICY+WITH+THESIS","SOFTWARE+ENGINEERING","SOFTWARE+ENGINEERING+WITH+THESIS","TURKISH+COURSES+COORDINATOR","TURKISH+LANGUAGE+%26+LITERATURE","TRANSLATION+AND+INTERPRETING+STUDIES","SUSTAINABLE+TOURISM+MANAGEMENT","TOURISM+ADMINISTRATION","TRANSLATION","EXECUTIVE+MBA","SCHOOL+OF+FOREIGN+LANGUAGES"]
interval1 = sys.argv[1] #Start semester
interval2 = sys.argv[2] #Finish semester
start = 0
start123 = 0
#Calculates the numerical version of the start semester
if(interval1[5:]=="Fall"):
    start = int(interval1[:4])
    start123=1
elif(interval1[5:]=="Spring"):
    start = int(interval1[:4])-1
    start123=2
else:
    start = int(interval1[:4])-1
    start123=3
finish = 0
finish123 = 0
#Calculates the numerical version of the finish semester
if(interval2[5:]=="Fall"):
    finish = int(interval2[:4])
    finish123=1
elif(interval2[5:]=="Spring"):
    finish = int(interval2[:4])-1
    finish123=2
else:
    finish = int(interval2[:4])-1
    finish123=3

foricin = (finish-start)*3+(finish123-start123)+1 # Calculates how many semesters are being processed.
years =[]
liste =["Dept./Prog.(name)","Course Code","Course Name"]
temp=interval1
# Calculates all semesters between given intervals.
for i in range(foricin):
    liste.append(temp)
    if(temp[5:]=="Fall"):
        years.append(str(int(temp[:4]))+"/"+str(int(temp[:4])+1)+"-1")
        temp = str(int(temp[:4])+1)+"-"+"Spring"
    elif(temp[5:]=="Spring"):
        years.append(str(int(temp[:4])-1)+"/"+str(int(temp[:4]))+"-2")
        temp = temp[:5]+"Summer"
    else:
        years.append(str(int(temp[:4])-1)+"/"+str(int(temp[:4]))+"-3")
        temp = temp[:5]+"Fall"


liste.append("Total Offerings")
spamwriter.writerow(liste) # Writes the first row.
sume=0 #Number off staffs which will be removed later.
# Main loop
for i in range(len(dept)):

    templist = [] # The row which will be printed.
    tempstring=shortdept[i]+"("+(dept[i].replace("+"," ").replace("%26","&").replace("%3a",":").replace("%2c",","))+")" # Rearranges the name of the departments.
    templist.append(tempstring)
    temparr=[] # Holds all course codes for that department which is being processed.
    tempinstructor=[] # Holds all instructors for that department which is being processed.
    yearray=[] # Holds U, G, I values for each semester for that department which is being processed.
    yearbyyear=[] # Holds course codes separated by their given semesters.
    tupleset =[] # Holds course codes and course names together for later processes.
    instructorset =[] # Holds course codes and their instructors together for later processes.
    for j in range(foricin):

        r = requests.get("https://registration.boun.edu.tr/scripts/sch.asp?donem={}&kisaadi={}&bolum={}".format(years[j],shortdept[i],dept[i])) # Gets the information from the website for specified semester.
        coursecode = re.findall("font-size:12px'>([A-Z]+ *[0-9A-Z]{3})\.[0-9]{1,2}",r.text) # Find the course codes of specified semester.
        coursenames = re.findall("Desc.[\D]+?<td>([^{]+?)&nbsp;</td>",r.text) # Find the course names of specified semester.
        coursecodetemp = coursecode.copy()
        for k in range(len(coursecode)):
            tupleset.append((coursecode[k],coursenames[k])) # Holds course codes and course names together for later processes.
        coursecode = sorted(list(set(coursecode))) # Removes duplicates and sorts them.
        for k in range(len(coursecode)):
            temparr.append(coursecode[k]) # Holds all coursecodes for a specific department.
        yearbyyear.append(coursecode) # Holds course codes separated by their given semesters.
        totalu =0 # U number for specified semester.
        totalg=0 # G number for specified semester.
        for k in range(len(coursecode)):
            if(coursecode[k][-3]=="5" or coursecode[k][-3]=="6" or coursecode[k][-3]=="7"):
                totalg+=1
            else:
                totalu+=1

        yearray.append(totalu)
        yearray.append(totalg)

        totali = re.findall("Desc.[\D]+?<td>.+?&nbsp;</td>[\D]+?<td>[\S]*?&nbsp;</td>[\D]+?<td>[\S]*?&nbsp;</td>[\D]+?<td>([\D]+?)&nbsp;</td>",r.text) # Find instructors for first semesters.

        totali2 = re.findall(">Info</a>&nbsp;</td>[\D]+?<td>([\D]+?)&nbsp;</td>",r.text) # Find instructors for second and third semesters.
        totali = totali+totali2 # All semesters.

        while(len(totali)!=0):
            if(totali[0].startswith("&nbsp")):
                totali.pop(0) # Remove wrong calculated instructors.
            else:
                break

        for k in range(len(totali)):
            instructorset.append((coursecodetemp[k],totali[k])) # Holds course codes and their instructors together for later processes.
            tempinstructor.append(totali[k]) # Holds all instructors for that department which is being processed.
        yearray.append(len(set(totali))) # Number of instructors for this semester.
        sume=0
        for u in range(len(totali)):
            if(totali[u]=="STAFF STAFF"):
                sume+=1
        yearray[-1] = yearray[-1]-sume # Number of instructors for this semester(Remove "STAFF STAFF").

    totalu =0 # U number for all semesters.
    totalg =0 # G number for all semesters.
    temparr = list(set(temparr)) # Remove duplicates.
    for k in range(len(temparr)):
            if(temparr[k][-3]=="5" or temparr[k][-3]=="6" or temparr[k][-3]=="7"):
                totalg+=1
            else:
                totalu+=1
    templist.append("U"+str(totalu)+" G"+str(totalg)) # Add elements which will be printed.
    templist.append("")
    totalofferingu=0 # Calculate U of the total offering.
    totalofferingg=0 # Calculate G of the total offering.

    for j in range(foricin):
        templist.append("U"+str(yearray[3*j])+" G"+str(yearray[3*j+1])+" I"+str(yearray[3*j+2]))
        totalofferingu += yearray[3*j]
        totalofferingg += yearray[3*j+1]
    tempinstructor = list(set(tempinstructor)) # Remove duplicates.
    sume=0
    for u in range(len(tempinstructor)):
        if(tempinstructor[u]=="STAFF STAFF"):
            sume+=1

    templist.append("U"+str(totalofferingu)+" G"+str(totalofferingg)+" I"+str(len(tempinstructor)-sume))
    spamwriter.writerow(templist) # Prints first row of each department.
    tupleset = sorted(list(set(tupleset))) # Remove duplicates
    instructorset = sorted(list(set(instructorset))) # Remove duplicates
    for j in range(len(tupleset)):
        templist =[]
        templist.append("")
        templist.append(tupleset[j][0]) # Add course code.
        templist.append(tupleset[j][1]) # Add course name.
        numberofx=0
        for k in range(len(yearbyyear)): # Calculates whether it is "x" or not

            if(tupleset[j][0] in yearbyyear[k]):
                templist.append("x")
                numberofx+=1
            else:
                templist.append("")
        dinstructorcount=0 # Number of distinct instructors for specific course.
        for k in range(len(instructorset)): # Removes "STAFF STAFF"

            if(instructorset[k][0]==tupleset[j][0] and instructorset[k][1] != "STAFF STAFF"):
                dinstructorcount+=1
        templist.append(str(numberofx)+"/"+str(dinstructorcount))
        spamwriter.writerow(templist)
