# -*- coding: utf-8 -*-
import requests
from urllib.parse import unquote, quote

# Data is JSON:
#
# {"channelname": "MTV3", "programs": [
#  {"id":"6587279","name":"Emmerdale%20(7)","simple_start_time":"10:35",
#   "simple_end_time":"11:05","start_time":"12.6.2017 10:35:00",
#   "end_time":"12.6.2017 11:05:00"},
#           etc...
#  {"id":"6600374","name":"Emmerdale%20(7)","simple_start_time":"10:35",
#  "simple_end_time":"11:05","start_time":"13.6.2017 10:35:00",
#  "end_time":"13.6.2017 11:05:00"}
# ]}"""


MAIL_ADDR   = "your name here <your email address here>"
BASE_URL    = "http://api.elisaviihde.fi/etvrecorder//ajaxprograminfo.sl?24h="

CHANNELS    = ("MTV3", "Yle TV1", "Yle TV2", "Nelonen", "Sub", "Yle Teema & Fem",
               "Jim", "Liv", "AVA", "TV5", "Kutonen", "FOX", "Hero")
channelData = []
mailTitle   = "TV-ohjelmamuistutus"
matches     = ("jääkiek", "kaara", "auto", "huonot", "pitääkö")  # small caps only!
excluded    = ("autokoulu", "autoparoni")   # if this is found, skip match!


def fetchChannelData():
    for channel in CHANNELS:
        channelData.append([channel, requests.get(BASE_URL + quote(channel)).json()])


def searchResults():
    global mailTitle
    results = ""

    for channel, jsonData in channelData:
        for i in range(len(jsonData["programs"])):
            for keyword in matches:
                program = unquote(jsonData["programs"][i]["name"])
                if program.find(keyword) > -1:
                    for exl in excluded:
                        if program.lower().find(exl) > -1:
                            print("skipping:", program)
                            break
                    else:
                        startTime = unquote(jsonData["programs"][i]["start_time"])
                        results += "{0:17}  {1:50}  {2:}\n".format(channel, program, startTime)

    #print("\nResults:\n\n" + results)
    if results == "":
        mailTitle = "TV-ohjelmamuistutus (ei osumia)"
        results = "Ei löytyneitä TV-ohjelmia!" # body needs some text, without, mail disappears!?
    return results


def sendResults(infoMessage):
    """
    See your mailgun account for a proper call for you, this is just an example
    """
    return requests.post( "https://xxxxxx.mailgun.net/xxxxxxxxxx",
        auth=("api", "key-xxxxxxxxxxxxxx"),
        data={"from": "Mailgun Sandbox <xxxxxxxxxxxxx>",
              "to": "%s" % MAIL_ADDR,
              "subject": "%s" % mailTitle,
              "text": "%s" % infoMessage})


def main():
    fetchChannelData()
    sendResults(searchResults())
    print("Script executed")


if __name__ == "__main__":
    main()


