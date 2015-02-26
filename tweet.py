import twitter, feedparser, tinyurl, hashlib
import time

i=0
api =""

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    ENDC = '\033[0m'

def twitterLogin():
    global api
    api = twitter.Api(consumer_key='', consumer_secret='', access_token_key='', access_token_secret='')
    #print api

def checkNewFeeds():
    now = time.strftime("%c")
    print bcolors.OKBLUE + time.strftime("%c") + bcolors.ENDC
    d = feedparser.parse('https://www.ncsc.nl/rss/beveiligingsadviezen')
    global i
    while (i < len(d['entries'])):
        titel = d['entries'][i]['title']
        url = d['entries'][i]['link']
        url = tinyurl.create_one(url)
        while (url == "Error") or (url == "http://tinyurl.com/yp9ewb"):
            url = tinyurl.create_one(url)               
        compleet = titel + " - " + url
        
        #Fix: UnicodeEncodeError
        compleet = compleet.encode('utf-8')

        hashCompleet = hashlib.md5(compleet).hexdigest()
        if hashCompleet in open('md5sum').read():
            print bcolors.OKGREEN + compleet + bcolors.ENDC
            #continue
        else:
            global api
            print bcolors.WARNING + compleet + bcolors.ENDC
            try:
                twitterLogin()
            except:
                print bcolors.WARNING + "Twitter limit exceeded" + bcolors.ENDC
                time.sleep(900)
                checkNewFeeds()
            status = api.PostUpdate(compleet)
            f = open('md5sum','a')
            f.write(hashCompleet + '\n')
            f.close() 
        i=i+1
    time.sleep(14400)
    i=0
    checkNewFeeds() 
    
checkNewFeeds()
