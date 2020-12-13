import requests
import json
import datetime

scrape_url = "https://scrape.pastebin.com/api_scraping.php?limit:250"

def scrape():
    r = requests.get(scrape_url)
    data = r.json()
    return data

def date(paste):
    date = paste["date"]
    timestamp = (
        datetime.datetime.fromtimestamp(
            int(date)
        ).strftime('%Y-%m-%d %H:%M:%S')
    )
    return timestamp

def key(paste):
    return paste["key"]

def syntax(paste):
    return paste["syntax"]

def main():
    data = scrape()
    for paste in data:
        timestamp = date(paste)
        paste_key = key(paste)
        paste_syntax = syntax(paste)
        print("Date: "+ timestamp + " Key: " + paste_key + " Syntax: " + paste_syntax)

if __name__ == "__main__":
    main()
    

## Grab content from scrape_url and add into field in db
## Add general error handling
## Add requests-specific error handling
## Do a check, before adding anything, to see if key is in the db already
## Do we want to allow for multiple outputs? Mongo, elk, straight up text files, SQL? Just one to start, allow for modularity
## How often should it run? Once an hour is probably enough if the checks work
## searching component should be separate
