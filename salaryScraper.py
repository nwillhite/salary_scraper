#!/usr/bin/python

#import libararies

import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import re

from bs4 import BeautifulSoup
from datetime import datetime




#####################################################################################################
'''
    specifies the urls to pull the data from, using a for loop we are able to increment through
    the number of pages in the site as they follow the same format
'''
#####################################################################################################
count = 1

for numb in range(1,11):
    #url = ("http://transparentcalifornia.com/salaries/all/?page=" + str(numb))
    url = ("http://transparentcalifornia.com/salaries/all/2015/cities/?page=" + str(numb))
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    #print type(soup)
    print count

    letters = soup.find_all('td')   #finds all the data within html element td

    letters2 = soup.find_all('small', {'class': 'muted'})   #takes all the data with element small with class muted



    #####################################################################################################
    '''
        variables used
    '''
    #####################################################################################################
    name = []
    job_title = []
    location = []
    reg_pay = []
    overtime_pay = []
    other_pay = []
    total_pay = []

    totalVar = 0
    totalVar_string = ""


    #####################################################################################################
    '''
        Allows us to pull only the job titles out of the of the table instead of the title and city in one.
    '''
    #####################################################################################################
    j = 0
    for a in letters:
        just_title = a.find_all('a')
        for a in just_title:
            if (a.get_text() == '(See note)') and (j % 3) == 1:
                break
            elif (j % 3) == 1:
                job_title.append(a.get_text())
            j += 1



    #####################################################################################################
    '''
        Allows for us to pull the location of the salary
    '''
    #####################################################################################################
    for small in letters2:
        locations = small.find_all('a')
        for a in locations:
            tmplocation = a.get_text()
            tmplocation = re.sub('[,0-9]', '', tmplocation) # takes out the , 2015 from location
            location.append(tmplocation)



    #####################################################################################################
    '''
        parses the name, reg pay, overtime pay, other pay, and adds them together for total sum
    '''
    #####################################################################################################
    i = 0
    for item in letters:
        errorCheck = item.get_text()
        if (i % 7) == 0:
            name.append(item.get_text())

        #if ((i % 7) == 1):
            #job_title.append(item.get_text())

        if ((errorCheck == 'Aggregate') and (i % 7) == 2) or ((errorCheck == 'Not provided') and (i % 7) == 2):
            reg_pay.append(0)
            totalVar = 0

        elif (i % 7) == 2:
            reg_pay.append(item.get_text())
            totalVar_string = item.get_text()
            totalVar_string = re.sub('[()$,]', '', totalVar_string)
            totalVar = float(totalVar_string)

        if ((errorCheck == 'Aggregate') and (i % 7) == 3) or ((errorCheck == 'Not provided') and (i % 7) == 3):
            overtime_pay.append(0)
            totalVar += 0
        elif (i % 7) == 3:
            overtime_pay.append(item.get_text())
            totalVar_string = item.get_text()
            totalVar_string = re.sub('[()$,]', '', totalVar_string)
            totalVar += float(totalVar_string)

        if ((errorCheck == 'Aggregate') and (i % 7) == 4) or ((errorCheck == 'Not provided') and (i % 7) == 4):
            other_pay.append(0)
            totalVar += 0
            total_pay.append(totalVar)

        elif (i % 7) == 4:
            other_pay.append(item.get_text())

            totalVar_string = item.get_text()
            totalVar_string = re.sub('[()$,]', '', totalVar_string)
            totalVar += float(totalVar_string)

            totalVar_string = '${:,.2f}'.format(totalVar)
            total_pay.append(totalVar_string)

        i += 1

    count +=1
    #####################################################################################################
    '''
        Print functions to help test that we are getting the right output
    '''
    #####################################################################################################
    #for item in locations:
    #   location.append(item.get_text())  # .encode('ascii', 'ignore'))

    #for t in range(len(name)):
    #   print name[t]


    #####################################################################################################
    '''
        Handles the inputting of the data into our .csv file
    '''
    #####################################################################################################


    # open a csv file with append, so old data will not be erased
    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for item in range(0, len(job_title)):
            writer.writerow([name[item], job_title[item], location[item], reg_pay[item], overtime_pay[item], other_pay[item], total_pay[item], datetime.now()])
