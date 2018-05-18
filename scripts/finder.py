#!/usr/bin/env python3

#by Joe Vanderlip

'''
Final Project for AY250, Spring 2018, UC Berkeley
by: Joe Vanderlip

Campsite Finder 1.0

This program allows a user to build a search engine to scrape Recreation.gov
for hard to get camp sites. While this program is designed for picking up one
night reservations at Yosemitie National Park, it can search in any national
park that requires a reservation. Once the engine begins its search, it will stop
when it finds any available site and will notify the user in both the terminal and
via email.

Inputs
===============
start_date          str
                    in YYYY-MM-DD format

end_date            str
                    in YYYY-MM-DD format

n_sites_text        str
                    string of index values for sites to check, this input is checked
                    to make sure each input is an int

dest_email          str
                    e-mail address to send notification to, proper entry checked by validate_email

## add search itteration here

Returns
================
site_text           str
                    pulls a string from the returned html so let the user know if there are multiple
                    locations availale within the campsite

link                str
                    URL for the site reservation page

site_name           str
                    name of the campsite

date                date object
                    date of the reservation

'''

import warnings
warnings.filterwarnings('ignore')
from campsiteFinder import source

print('*********************************************************************')
print('**************** Welcome to Campsite Finder 1.0 *********************')
print('*********************************************************************')
print('')
print('First I need the date range you wish to search in: (YYYY-MM-DD)')

start_date, end_date = source.getDateInput()

print('Next we will select which camisites to search:')
print('Campsite # \t Site Name  \t\t Park \t\t State \t ParkID')
print('=========================================================================')
ln = 0
for s in range(0, 6):
    ln += 1
    data_l = source.pullinfo(s)
    if len(data_l[0]) <12:
        print(ln,'\t\t', data_l[0],'\t\t',data_l[1], '\t', data_l[2], '\t', data_l[3])
    else:
        print(ln, '\t\t', data_l[0],'\t',data_l[1], '\t', data_l[2], '\t', data_l[3])

site_n = source.getSiteNums()
dest_email = source.getEmailaAddress()
run_delta, run_length, search = source.asktoRepeat()

print('')
print('')
print('************************Searching************************')
print('From: ', start_date)
print('To ', end_date)
print('Campsite  \t\t Park \t\t State \t ParkID')
print('=========================================================')

for s in site_n:
    data_l = source.pullinfo(s)
    if len(data_l[0]) <12:
        print(data_l[0],'\t\t',data_l[1], '\t', data_l[2], '\t', data_l[3])
    else:
        print(data_l[0],'\t',data_l[1], '\t', data_l[2], '\t', data_l[3])
print('=========================================================')
print('Notification will be sent to '+dest_email)
if search == False:
    print('Is search automated?   NO')
if search == True:
    print('Is search automated?   YES')
    print('Searching every ',run_delta,' min for ',run_length,' hours')
    ##maybe put status bar here??
#print(site_list)
print("STARTING SEARCH...")

'''
Running the search engine:
the wrapandfind function wraps all the functions in location_data.py together taking the user inputs to search
recreation.gov.  The first site found within a date range stops the search, and sends an email alert to the user
as well as displaying the reservation URL with the site name and date. If no site is found, the engine alerts
the user and enters into its wait period before running the serach again.
'''

if search == True:
    source.loopit(site_n, run_length, run_delta, start_date, end_date, dest_email)
if search == False:
    site_text, link, site_name, date = source.wrapandfind(site_n, start_date, end_date)
    if site_text == 0:
        print(date)
    else:
        print('Campsite found on '+date+' at '+site_name+'. Follow this link to complete reservation: '+link)
        print('Sending e-mail to '+dest_email)
        source.email(site_name, date, site_text, link, dest_email)
print("Thank you for using Campsite Finder")
raise SystemExit
