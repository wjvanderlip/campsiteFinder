## Vanderlip AY250 Final Project

Campsite Finder 1.0 is a web scraping utility to find last minute and hard to get campground sites
at National Parks. Due to the demand at sites at Yosemite, the sites are booked within minutes of release
and when reservations are canceled, they are only available for a small part of the day before they are booked.
This program allows the user to set a search window, specific campgrounds, and an option to run the search on repeat
for several days. If a match is found, the URL of the reservation link is send to the user's e-mail as well as displayed
in the terminal screen.

### To setup the program as a user
#### Step 1- Install Required Packages
```
pip install -r requirements.txt
```
#### Step 2- Enable E-mail alerts
If you would like the program to send you an alert email you need to go into the source.py file, locate the email function at the bottom
and input your Gmail username and password. The program sends the alert via the user's email account.   
```
gmail_user = keys.email_un  
gmail_password = keys.email_pw
```
#### Step 3- Setup the Package
```
python setup.py install
```
### Running the Program
Once setup is complete and you have entered your email account information, run the program from the root directory by:

```
./scripts/finder.py
```
