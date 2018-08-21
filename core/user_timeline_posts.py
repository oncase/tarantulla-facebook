import facebook
import requests
import os
from optparse import OptionParser
import json
from face import facebook_intg
import time
import datetime


if __name__ == "__main__":

    baseDir = os.path.dirname(os.path.abspath(__file__)) + '/'

    '''Load API keys'''
    with open(baseDir + '../api-keys.json') as f:
        keys = json.load(f)

    '''Load config-timeline.json'''
    with open(baseDir + '../config-timeline.json') as fileName:
        confs = json.load(fileName)

    '''Set vars'''
    outputFolder = baseDir+confs['temp_output']
    publishers = confs['publishers']
    dateFrom = confs['dateFrom']
    dateTo = confs['dateTo']
    currDate = time.strftime("%d-%m-%Y")
    start = datetime.datetime.now()


    for publisher in publishers:
        
        pubStart = datetime.datetime.now()
        
        currPub = publisher['userName']
        pubName = publisher['name']

        outputFile=outputFolder+currPub.lower()+currDate+'-fb.json'

        facebook_intg(outfile=outputFile, publisher=currPub, access_token=keys['ACSSTKFB'], dateFrom=dateFrom, dateTo=dateTo)
        
        pubEnd = datetime.datetime.now()

        print("Process Finished for "+ pubName + " in " +str(pubEnd-pubStart))
        print('\n')

    end = datetime.datetime.now()
    print("Total elapsed time: "+str(end-start))    