Session 3 Homework
==================

#Assignment #3 Mashup

#This was a enjoyable assignment that I learned a lot from.  I tried to do a few more complicated tasks, but ran out of time.

#This program is custom NPR News feed.  It returns all my local npr station info and the full text, images, and audio of the news stories I'm interested in.  But since sometimes the news is hard I also mashed in some imageges of kittens.

#You should just be able to run this code.

from urllib2 import urlopen
from json import load, dumps

#NPR Key
key = "MDEyNTA4NzYxMDEzODMzMjY0NDQ5YTg4MQ001"

def build_api_call(key, zip_code):
    url = 'http://api.npr.org/stations?apiKey=' + key
    url+='&format=json' 
    url += "&zip=" + str(zip_code)
    return url 

def call_station_api(url):
    response = urlopen(url)
    j = load(response)
    return j
	
def parse_station_json(json_obj):
    for station in json_obj['station']:
        print (station['callLetters']['$text']+ ": " + 
	    station['marketCity']['$text'] + ", " + 
	    station['state']['$text'])
        print "Frequency:" , station['frequency']['$text'] , station['band']['$text']

        if 'url' in station:
            print "MP3 Streams: "
            for link in station['url']:
                if link["type"] == "Audio MP3 Stream":
                    print "\t" , link["title"], " - " , link["$text"]

def NPR_Stories(key, subject):
    url = 'http://api.npr.org/query?apiKey=' 
    url = url + key
    url += '&numResults=10&format=json'
    url += '&id=' + str(subject) +'&requiredAssets=image,text,audio' 
    response = urlopen(url)
    json_obj = load(response)

    f = open('output.json', 'w')
    f.write(dumps(json_obj, indent=4))
    f.close()

    for story in json_obj['list']['story']:
        print "TITLE: " + story['title']['$text'] + "\n"
        print "DATE: " + story['storyDate']['$text'] + "\n"
        print "TEASER: " + story['teaser']['$text'] + "\n"
	
        if 'byline' in story:
            print "BYLINE: " + story['byline'][0]['name']['$text'] + "\n"
        if 'show' in story:
            print "PROGRAM: " + story['show'][0]['program']['$text']+"\n"
        print "NPR URL: " + story['link'][0]['$text'] +"\n"
        print "IMAGE: " +story['image'][0]['src'] +"\n"
        if 'caption' in story:
            print "IMAGE CAPTION: " +story['image'][0]['caption']['$text']  +"\n"
        if 'producer' in story:
            print 'IMAGE CREDIT: ' + story['image'][0]['producer']['$text'] +"\n"
        print "MP3 AUDIO: " + story['audio'][0]['format']['mp3'][0]['$text'] +"\n"
        for paragraph in story['textWithHtml']['paragraph']:
            print paragraph['$text'] + "\n"

def kittens():
    url = 'http://placekitten.com/250/250'
    kitten = urlopen(url).read()
    f = open('kittens.jpeg', 'w')
    f.write(kitten)
    print f
    f.close()


if __name__ =='__main__':
    url = build_api_call(key, 98115)
    kittens()
    print "URL: ", url
    json_obj = call_station_api(url)
    kittens()
    parse_station_json(json_obj)
    kittens()
    NPR_Stories(key, 1049)


