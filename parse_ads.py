#! /usr/bin/env python3

import requests
import time
import config


def CheckDate(resp, currentTime):  # check if post published in last 24 hours
    return currentTime - resp["response"]["items"][0]["date"] < 86400 # 60 * 60 * 24


def SearchRepost(resp):
    #print(resp["response"]["items"][0])
    #if "copy_history" in resp["response"]["items"][0]:
    if "copy_history" in resp["response"]["items"][0]:
        return resp["response"]["items"][0]["id"]
    else:
        return False


def SearchSource(resp):
    result = ''''''
    if "link" in resp["response"]["items"][0]:
        return resp["response"]["items"][0]["link"]  # & return it
    else:
        return False


def CheckBlackList(blackList, tmp):
    notFound = True
    for i in range(0, len(blackList)):
        if tmp.find(blackList[i]):
            notFound = False
    return notFound


def WallPost(accessToken, text):
    wallPost="https://api.vk.com/method/wall.post?access_token="
    owner = '&owner_id=-197501499&v=5.92&from_group=1'
    message='&message='
    r = requests.get(wallPost + accessToken + owner + message + text)
    print(r)


def FiscusWall(accessToken, tmp):
    WallPost(accessToken, tmp)


# not used #correcting currentIndex after searching copyright link
def RectificationIndex(str, currentIndex):
    return str.find('''"link":"''', currentIndex)


currentTime = time.time()
wallGet = "https://api.vk.com/method/wall.get?access_token="
ownerId = '&owner_id=-'
offsetValue = "&offset="
otherPar = '&count=1&v=5.92'

accumulated_result = ""

for i in config.PublicId:
    lastDay = True
    offset = 0
    while (lastDay):
        req = requests.get(wallGet + config.accessToken + ownerId +
                           i + offsetValue + (str(offset)) + otherPar)
        res = req.json()

        if "error" in res:
            time.sleep(1)
            continue

        if (CheckDate(res, currentTime)):
            tmp = SearchSource(res)

            if (tmp and CheckBlackList(config.blackList, tmp)): #if source founded & not blacklisted
                print (tmp)
                FiscusWall(config.accessToken,tmp)

            tmp = SearchRepost(res)

            if (tmp): #if repost founded
                repost = "https://vk.com/wall-" + i + "_" + str(tmp)
                accumulated_result += '\n' + repost
                print (repost)

            offset += 1
        else:
            lastDay = False

FiscusWall(config.accessToken, accumulated_result)
