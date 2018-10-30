#!/usr/bin/python

import csv
import os


def getpercentage(dictlist, count):
    dico = {}
    for key in dictlist:
        dico[key] = round((dictlist[key]*100)/count, 2)
    return dico


def getfile(path):
    dirs = os.listdir(path)
    return dirs[0]


def gettop10(mydict):
    count = 0
    top10list = list()
    for key, value in sorted(mydict.items(), key=lambda kv: (kv[1], kv[0])):
        count += 1
        top10list.append(key)
        if count == 10:
            break
    #print(top10list)
    return top10list


def main():
    stateList = {}
    positionList = {}
    total = 0
    inputFolder = './input'
    file = getfile(inputFolder)

    with open(inputFolder+"/"+file) as csvfile:
        freader = csv.DictReader(csvfile, delimiter=';', quotechar='|')

        if 'STATUS' in freader.fieldnames:
            keyStatus = 'STATUS'
        else:
            keyStatus = 'CASE_STATUS'

        if 'LCA_CASE_EMPLOYER_STATE' in freader.fieldnames:
            keyState = 'LCA_CASE_EMPLOYER_STATE'
        else:
            keyState = 'EMPLOYER_STATE'

        if 'LCA_CASE_JOB_TITLE' in freader.fieldnames:
            keyPos = 'LCA_CASE_JOB_TITLE'
        else:
            keyPos = 'JOB_TITLE'


        for row in freader:
            #print(row['STATUS'], row['LCA_CASE_EMPLOYER_STATE'], row['LCA_CASE_JOB_TITLE'])
            stateName = row[keyState]
            positionName = row[keyPos]
            total += 1
            if row[keyStatus] == 'CERTIFIED':
                if stateName in stateList:
                    stateList[stateName] += 1
                else:
                    stateList[stateName] = 1

                if positionName in positionList:
                    positionList[positionName] += 1
                else:
                    positionList[positionName] = 1

        statePercentage = getpercentage(stateList, total)
        positionPercentage = getpercentage(positionList, total)

        topposition = gettop10(positionPercentage)
        topstate = gettop10(statePercentage)

        occupationFileOutput = open("./output/top_10_occupations.txt", "w")
        occupationFileOutput.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE \n")
        for position in topposition:
            position = position.strip('\'"')
            if position != '' and position in positionPercentage and position in positionList:
                occupationFileOutput.write(position + ";" + str(positionList[position]) + ";" + str(positionPercentage[position]) + "%" + '\n')

        stateFileOutput = open("./output/top_10_states.txt", "w")
        stateFileOutput.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE \n")
        for stateKey in topstate:
            stateKey = stateKey.strip('\'"')
            stateFileOutput.write(stateKey + ";" + str(stateList[stateKey]) + ";" + str(statePercentage[stateKey]) + "%" + '\n')


#main function call
if __name__ == '__main__':
    main()