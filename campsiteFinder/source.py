import numpy as np
import pandas as pd
import pkg_resources
import datetime as dt
from datetime import datetime, timedelta
import time

import os

import requests as rq
from bs4 import BeautifulSoup
import smtplib

from validate_email import validate_email

from campsiteFinder import keys

import warnings  #the web scraping throws a lot of warning for each search
warnings.filterwarnings('ignore')

'''
The data frame uses a .csv file to pull search data. As this .csv is populated, the program will pull in the added sites for more search options.
'''

park_info_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'park_data.csv'), sep=', ', header =0, index_col=0, engine='python')

def getDateInput():
    '''Requests user input the start and end dates of the search, screens inputs for proper format

    Parameters
    =================
    User Input:     str
                    Date in YYYY-MM-DD format

    Outputs
    =================
    start_date      str
                    date to begin the search

    end_date        str
                    date to end the search

    '''
    ##  Inputs to tweak search
    month_delta = 4  #sets allowable range to search in, the sites open on a staggered rolling release
                     #I think its on a two week release interval about 4 months out

    while True:
        try:
            start_date = (input("Please enter your start date: "))
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            print("Plesae input the proper format YYYY-MM-DD")
            continue
        if datetime.strptime(start_date, '%Y-%m-%d') < datetime.today():
            print('Your start date must be after today.')
            continue
        if datetime.strptime(start_date, '%Y-%m-%d') > (datetime.today() + timedelta(days=30*month_delta)):
            print('Your start date must be within', month_delta, 'months from today.')
            continue
        else:
            break

    while True:
        try:
            end_date = (input("Please enter your end date: "))
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print("Plesae input the proper format YYYY-MM-DD")
            continue
        if datetime.strptime(end_date, '%Y-%m-%d') > (datetime.today() + timedelta(days=30*month_delta)):
            print('Your end date must be within' month_delta, 'months from today.')
            continue
        if datetime.strptime(end_date, '%Y-%m-%d') <= (datetime.strptime(start_date, '%Y-%m-%d')):
            print('Your end date needs to be at least one day after your start date.')
            continue
        else:
            break

    return start_date, end_date

def getSiteNums():
    '''Requests user input to select campsties to search in, checks input for correctness,
    parses input to create list of integers for search

    Parameters
    =================
    User Input:     str
                    inputs of integers linked to campsites

    Outputs
    =================
    site_n          list
                    list of ints of campsites to search in

    '''

    while True:
        try:
            site_inp = input('Please enter campsite #s to search, ex. "1 4 5":  ')
            site_n = clean_up_sites(site_inp).split(' ')
            for s in site_n:
                int(s)
                if not 0<int(s)<7:
                    raise ValueError
            if not len(site_n) < 7:
                raise ValueError


        except ValueError:
            print("Only enter an interger between 1-6.")
            continue

        else:
            return intList(site_n)

def intList(strlist):
    ''' takes user input list of string values, check that there isnt a repeat value
    then appends the value to a new list as an int

    Parameters
    =================
    strlist:    list
                list of strings

    Outputs
    =================
    site_list       list
                    list of ints of campsites to search in
    '''

    site_list = []
    for s in strlist:
        if (int(s)-1) not in site_list:
            site_list.append(int(s)-1)
    return site_list


def getEmailaAddress():
    '''requests users E-mail address, checks that it is a valid address and returns the
    validated address

    Parameters
    =================
    User Input      str
                    user's email address

    Outputs
    =================
    dest_email      str
                    validated email address

    '''
    while True:
            dest_email = input('Please enter your e-mail address for notification (ex. joe@example.com):  ')
            check_valid = validate_email(dest_email)

            if check_valid == False:
                continue
            if check_valid == True:
                break
    return dest_email

def asktoRepeat():
    '''Prompts the user if they would like to automate the search.

    Parameters
    =================
    User Input #1:  str
                    'y' or 'n' if user would like to repeat the searche

    Outputs
    =================
    run_delta:      int
                    time between searches

    run_length:     int
                    length of search in hours

    search          bool
                    True or False if user would like to search
    '''

    while True:
        try:
            choice = input('Would you like to automate this search? [y/n] ')
            if choice == 'y':
                search = True
                run_delta, run_length = autoDetails()
                break  #runs script to get information for automation
            if choice == 'n':
                search = False
                run_length = 0
                run_delta  = 0
                break
            if choice != 'y' or 'n':
                raise ValueError
        except ValueError:
            print('Please respond with "y" or "n"')
            continue

        else:
            break
    return run_delta, run_length, search


def clean_up_sites(text):
    '''removes commas and extra spaces from site number input

    Parameters
    =================
    text:           str
                    input value from selected sites

    Outputs
    =================
    clean:          str
                    str with int like values
    '''

    replace_list = [',']
    for r in replace_list:
        text1 = text.replace(r, '')
    text2 = text1.replace('   ', '  ')
    clean = text2.replace('  ', ' ')

    return clean


def pullinfo(site_number):
    '''extracts data from park info DataFrame

    Parameters
    =================
    site_number:    int
                    index of site info

    Outputs
    =================
    hold:           DataFrame objet
                    object with site data
    '''

    hold = park_info_df.iloc[site_number]
    return hold


def autoDetails():
    '''If user selects they would like to repeat the search, this function prompts the
    user with two more inputs questions for time between itterations and length of the
    search.

    Parameters
    =================
    User Input #1:  int
                    time inbetween itterations in  minutes

    User Input #2:  int
                    length of search in hours

    Outputs
    =================
    run_delta:      int
                    time between searches

    run_length:     int
                    length of search in hours
    '''

    while True:
        try:
            run_delta = input('How many minutes do you want in between itterations? 5-60min: ')
            int(run_delta)
            if not 4<int(run_delta)<61:
                    raise ValueError
        except ValueError:
            print('Please enter an int value between 5 and 60')
            continue
        else:
            break

    while True:
        try:
            run_length = input('How many hours do you want to run the engine? 1-24hr: ')
            int(run_length)
            if not 0<int(run_length)<25:
                    raise ValueError
        except ValueError:
            print('Please enter an int value between 1 and 24')
            continue
        else:
            break

    return int(run_delta), int(run_length)



login_payload = keys.recreation_login  #use in the future to login prior to search
login_url = 'https://www.recreation.gov/memberSignInSignUp.do'
#not needed right now result_url = 'https://www.recreation.gov/unifSearchResults.do'
search_url = 'https://www.recreation.gov/campsiteSearch.do'
base_url = 'https://www.recreation.gov'

payload_1 = {'arrivalDate': 'start', 'departureDate': 'end', 'camping_common_3012': "4"}


def pingSite(site_url, payload):
    '''uses request to access Recreation.gov search area, and delievers payload
    to run search for campsite for one night. If payload delivery is successful,
    it will return the html text for parsing.  It will also let the user know if there
    is an error with the request.

    Parameters
    =================
    site_url:       str
                    input value from selected sites

    payload:        dict
                    payload to populate search areas in website
    Outputs
    =================
    rr.text:        text
                    html text from webpage after payload processed
    '''

    with rq.Session() as sesh:
        #post = sesh.post(login_url, data=login_payload)
        r = sesh.get(site_url, verify= False)
        rr = sesh.post(search_url, data=payload)

        #still need to check request error
        if (rr.status_code != 200):
            raise Exception("failedRequest","ERROR, {0} code received from {1}".format(rr.status_code, search_url))
        else:
            return rr.text


def addDates(start_date, end_date):
    '''takes user input date format YYYY-MM-DD, converts to required format for
    payload ddd MMM DD YYYY

    Parameters
    =================
    start_date:     str
                    input value from selected sites
    end_date:       str
                    payload to populate search areas in website
    Outputs
    =================
    payload_1:      dict
                    search payload to send to Recreation.gov
    '''

    start2 = datetime.strftime(start_date, "%a %b %d %Y")
    end2 = datetime.strftime(end_date, "%a %b %d %Y")
    payload_1['arrivalDate'] = start2
    payload_1['departureDate'] = end2
    return payload_1


def buildURL(location):
    '''builds the url to send to requests

    Parameters
    =================
    location:       int
                    DataFrame index value

    Outputs
    =================
    url_1:          str
                    url of target campsite search page
    '''

    name = park_info_df.iloc[location, 0]
    #name_split = name.split(' ')
    name_f = name.replace(' ', '-')
    #print(name_f)
    park_ID = park_info_df.iloc[location, 3]
    url_1 = ('https://www.recreation.gov/camping/{0}/r/campgroundDetails.do?'
                'contractCode=NRSO&parkId={1}'.format(name_f, park_ID))
    #print(url_1)
    return url_1


def extractSites(html):
    '''takes the html.text file returned from the request post and parses it
    to determine if there are any available sites, and if there are, extracts
    the number of available tent sites and booking url.

    Parameters
    =================
    html:           html.text object
                    return from request post of searh

    Outputs
    =================
    n_site_text:    str
                    string that shows how many tent sites are available

    booking_link    str
                    link to book site
    '''

    soup = BeautifulSoup(html, 'html.parser')
    sites = soup.findAll('div', {"class": "matchSummary"})

    if int(sites[0].text.split(' ')[0]) == 0:
        n_sites_text = 0
        booking_link = 0

    if int(sites[0].text.split(' ')[0]) != 0:
        n_sites_text = sites[0].text[:-45]
        link_grab = soup.findAll('a', {'class': 'book now'})
        booking_link = base_url+link_grab[1]['href']
    return n_sites_text, booking_link


def wrapandfind(site_list, start_date, end_date):
    '''wrapper that runs the whole search by site by day.

    Parameters
    =================
    site_list:      list
                    list of ints for campsites to search

    start_date      str
                    start date in format YYYY-MM-DD

    end_date        str
                    end date in format YYYY-MM-DD

    Outputs
    =================
    n_site_text     str
                    string of how many tent sites are avialable on date

    booking_link    str
                    link to book the site

    pullinfo        str
                    name of the campsite

    date            date object
                    date of found reservation YYYY-MM-DD

    '''

    datelist = pd.date_range(start=start_date, end=end_date, periods=None, freq="D").to_pydatetime()

    for s in site_list:
        d1 = 0
        d2 = 0
        site_url_load = buildURL(s)
        for d in range(len(datelist)-1):
            payload_2 = addDates(datelist[d], datelist[d+1])
            html = pingSite(site_url_load, payload_2)
            n_site_text, booking_link = extractSites(html)
            if n_site_text == 0:
                d1 +=1
                #print('passed days: ',d1)
                continue

            if n_site_text != 0:
                d2 += 1
                #print('Found one: ',d2)
                #print(n_site_text)
                #print(booking_link)
                return n_site_text, booking_link, pullinfo(s)[0], datetime.strftime(datelist[d], "%Y-%m-%d")
                #return also closes the loop, can alter so it returns each day
    spot1 = 0
    spot2 = 0
    spot3 = 0
    spot4 = "No sites currently available between "+start_date+' and '+end_date
    return(spot1, spot2, spot3, spot4)


def email(location, date, body1, link, dest_email):
    '''connects to gmail account and sends alert e-mail to user with reservation link. Also checks if the user went into the source code
    and added their e-mail account information to allow the program to send the notification.  If login information is not found, it will
    prompt the user to add this information and still display the reservation link.

    Parameters
    =================
    location:       str
                    location of the found site

    date            str
                    date of the found reservation

    body1           str
                    additional information about the reservation

    link            str
                    URL to reservation page

    dest_email      str
                    user supplied email to send alert

    Outputs
    =================
    E-mail is sent to user or failure message

    '''

    try:
        gmail_user =  keys.email_un
        gmail_password = keys.email_pw

    except AttributeError:
        print("Check E-mail account log in information in source file, e-mail alerts are disabeled until this"
                  " issue is resolved, please follow the link in the terminal screen for your reservation")
    except NameError:
        print("Check E-mail account log in information in source file, e-mail alerts are disabeled until this"
                  " issue is resolved, please follow the link in the terminal screen for your reservation")
        ## catches errors thrown if user does not enter their own email log in info to send alert, this bypasses the email push and just does
        ## an onscreen notification
    else:
        sent_from = 'Campsite Finder 1.0'
        to = dest_email
        subject = 'Campsite at '+location+' on '+date
        body = "On "+date+" at "+location+' there are/is '+body1+'. To book this site click on the following link '+link

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, to, subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print( 'Email sent!')
        except:
            print( 'Something went wrong...')


def loopit(site_list, run_length, run_delta, start_date, end_date, dest_email):
    '''repeats the search based on user inputs, if a site is found it calls the email function
    and alerts the user

    Parameters
    =================
    site_list       list
                    list of ints of sites to search

    run_length      int
                    time in hours of how long to run the search

    run_delta       int
                    time in minutes between searches

    start_date      date object
                    start date of search

    end_date        date object
                    end date of search

    dest_email      str
                    user email to send notification

    Outputs
    =================
    calls function to send email to user with alert

    '''

    counter = 0
    tot_iter = run_length*60/run_delta  #in min
    while counter < tot_iter:
        counter +=1
        site_text, link, site_name, date = wrapandfind(site_list, start_date, end_date)

        if site_text == 0:
            print('Search #',counter,'of',tot_iter, date)  #added status line for print update
        else:
            print('Campsite found on '+date+' at '+site_name+'. Follow this link to complete reservation: '+link)
            print('Sending e-mail to '+dest_email)
            email(site_name, date, site_text, link, dest_email)
            break

        time.sleep(run_delta*60)
