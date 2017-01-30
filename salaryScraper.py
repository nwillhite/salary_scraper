# import libararies


import urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime

#specify the url

for numb in range(1,2):
    #url = ("http://transparentcalifornia.com/salaries/all/?page=" + str(numb))
    url = ("http://transparentcalifornia.com/salaries/all/2015/cities/?page=" + str(numb))
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    print type(soup)

    letters = soup.find_all('td')

    letters2 = soup.find_all('small', {'class': 'muted'})

'''
    Allows us to pull only the job titles out of the of the table instead of the title and city in one.
'''
    j = 0
    for a in letters:
        just_title = a.find_all('a')
        for a in just_title:
            if ((a.get_text() == '(See note)') and (j % 3) == 1):
                break
            elif (j % 3) == 1:
                print a.get_text()
            j += 1

'''
variables used
'''
    i = 0

    name = []
    job_title = []
    location = []
    reg_pay = []
    overtime_pay = []
    other_pay = []
    total_pay = []

    totalVar = 0
    totalVar_string = ""

    for small in letters2:
        locations = small.find_all('a')
        for a in locations:
            location.append(a.get_text())

    for item in letters:
        if ((i % 7) == 0):
            name.append(item.get_text())
        if ((i % 7) == 1):
            job_title.append(item.get_text())

        if ((i % 7) == 2):
            reg_pay.append(item.get_text())

            totalVar_string = item.get_text()
            totalVar_string = totalVar_string[1:]
            totalVar = float(totalVar_string.replace(',', ''))

        if ((i % 7) == 3):
            overtime_pay.append(item.get_text())

            totalVar_string = item.get_text()
            totalVar_string = totalVar_string[1:]
            totalVar += float(totalVar_string.replace(',', ''))

        if ((i % 7) == 4):
            other_pay.append(item.get_text())

            totalVar_string = item.get_text()
            totalVar_string = totalVar_string[1:]
            totalVar += float(totalVar_string.replace(',', ''))
            totalVar_string = '${:,.2f}'.format(totalVar)
            total_pay.append(totalVar_string)
        i += 1


    for item in locations:
        location.append(item.get_text().encode('ascii', 'ignore'))


    #for i in range(len(location)):
    #    print location[i]

'''
     # open a csv file with append, so old data will not be erased
    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for item in range(0, len(job_title)):
            writer.writerow([name[item], job_title[item], location[item], reg_pay[item], overtime_pay[item], other_pay[item], total_pay[item], datetime.now()])
            #writer.writerow([location[item]])

'''