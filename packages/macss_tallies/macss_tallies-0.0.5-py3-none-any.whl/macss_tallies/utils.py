import urllib
import json
import dateutil
import dateutil.parser
import shutil
import os.path

import datetime
import requests
#import pandas
#import matplotlib.pyplot as plt

apiURL = 'https://api.github.com'

#mostly for testing
tokenPath = os.path.normpath(os.path.join(os.path.dirname(__file__) + '/..' , 'token.txt'))

#Name of the organization, hard coded for now
workshopOrgName = 'uchicago-computation-workshop'

#This is likely to change, https://developer.github.com/v3/reactions/
reactionsHeader = {'Accept' : 'application/vnd.github.squirrel-girl-preview'}

#The API returns ASCII strings instead of the emoji directly
emojiMapping = {
    '+1' : '👍',
    '-1' : '👎',
    'heart' : '❤️',
    'hooray' : '🎉',
    'laugh' : '😄',
    'confused' : '😕',
}

def getGithubURL(target, auth = None, headers = None, links = False):
    if auth is None:
        try:
            with open(tokenPath) as f:
                username, token = f.readline().strip().split()
                auth = (username, token)
        except FileNotFoundError:
            auth = None
    if target.startswith('http'):
        url = target
    else:
        url = urllib.parse.urljoin(apiURL, target)
    r = requests.get(url, auth = auth, headers = headers)
    if not r.ok:
        raise RuntimeError('Invalid request: {}\n{}'.format(url, r.text))
    try:
        if links:
            links = {}
            if r.links and len(r.links) > 0:
                links = r.links
            return json.loads(r.text), links
        return json.loads(r.text)
    except json.JSONDecodeError:
        return []

def checkRate():
    rateLimiting = getGithubURL('{}/rate_limit'.format(apiURL))
    #print("remaining : {}".format(rateLimiting['rate']['remaining']))
    #print("reset : {}".format(datetime.datetime.fromtimestamp(rateLimiting['rate']['reset']).strftime('%H:%M')))
    return rateLimiting['rate']['remaining']

def getRepos(tokenFile = None):
    """Gets the JSON for the repo and converts to a dict for each of the org's repos, then sorts by date dropping the first two since they are not for speakers"""
    #This is not the correct way of doing this
    #But I don't want to restructure stuff right now
    if tokenFile is not None:
        global tokenPath
        tokenPath = tokenFile
    orgInfo = getGithubURL('orgs/{}'.format(workshopOrgName))
    reposInfo = getGithubURL(orgInfo['repos_url'])
    currentRepos = sorted(reposInfo, key = lambda x : dateutil.parser.parse(x['created_at']), reverse = False)[2:]
    return currentRepos

def getIssueInfo(issueDict):
    """Gets and trims down the JSON for an issue's reactions"""
    reactions = getGithubURL('{}/reactions'.format(issueDict['url']), headers = reactionsHeader)

    return {
        'title' : issueDict['title'],
        'body' : issueDict['body'],
        'url' : issueDict['html_url'],
        'auth' : issueDict['user']['login'],
        'reactions' : ''.join(sorted([emojiMapping[r['content']] for r in reactions], reverse = True)),
        }

def printIssue(issueDat):
    """Prints an issue's info and hopefuuly won't oveflow the screen"""
    width = shutil.get_terminal_size((80, 20)).columns
    print(issueDat['title'][:width])
    print(issueDat['url'][:width])
    print(issueDat['auth'][:width])
    print("[{}] {}".format(len(issueDat['reactions']), issueDat['reactions'])[:width])

def getIssues(repoDict):
    """This gets and prints all the issues for a repo"""
    print("Getting questions for: {}".format(repoDict['name']))
    issues, links = getGithubURL("{}/issues".format(repoDict['url']), links = True)
    while 'next' in links:
        issuesNext, links = getGithubURL(links['next']['url'], links = True)
        issues += issuesNext
    issuesInfo = []
    for i, issue in enumerate(issues):
        #We have to make one API call for each issue
        print("Querying GitHub: {:.0f}%".format(i / len(issues) * 100), end = '\r')
        issuesInfo.append(getIssueInfo(issue))
    issuesInfo = sorted(issuesInfo, key = lambda x : len(x['reactions']))
    for issueDat in issuesInfo:
        printIssue(issueDat)
    print("There are {} total questions".format(len(issuesInfo)))
