# -*- coding: utf-8 -*-
# Module: default
# Author: MB
# Created on: 02.12.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import requests
from bs4 import BeautifulSoup

def get_linklist(link="http://www.sxyprn.com"):

    s = requests.Session()

    r = s.get(link)
    print(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    ELLIST = []

    step = soup.find_all("div", {"class": "post_el_small"})

    for element in step:
        linkstream = element.find('a', {"class": "js-pop"}).get('href')

        titlestream = element.find('div', {"class": "post_text"}).text
        titlestream = titlestream.encode('ascii', 'ignore')
        try:
            thumbstream = element.find('img', {"class": "mini_post_vid_thumb"}).get('src')
            thumbstream = thumbstream.replace('"', "")
            thumbstream = thumbstream.replace('=//', "")
            thumbstream = thumbstream.replace('//', '/')
            thumbstream = 'http://' + thumbstream
            thumbstream = thumbstream.replace('///', '//')
        except:
            thumbstream = ""
        ELEMENT = {'name': str(titlestream), 'thumb': str(thumbstream), 'video': str(linkstream), 'genre': 'New'}
        ELLIST.append(ELEMENT)

    return ELLIST


def get_moviesrc(link):

    r = requests.get("http://www.sxyprn.com"+link)
    soup = BeautifulSoup(r.text,'html.parser')

    ### Mgic Key
    buffer = r.text.split("class='vidsnfo'")
    linkstream = (buffer[1])
    buffer = linkstream.split("></span>")
    linkstream=buffer[0]
    buffer = linkstream.split(":")
    linkstream = (buffer[1])
    linkstream = linkstream.replace('"',"")
    linkstream = linkstream.replace('\\',"")
    linkstream = linkstream.replace('}',"")
    linkstream = linkstream.replace("'","")
    linkstream = linkstream.replace('cdn','cdn8')

    linkstream= decrypting(linkstream)

    linkstream = "https://sxyprn.com"+linkstream

    return linkstream


def decrypting(link):
    buffer = link.split('/')
    bbuffer = buffer

    c=int(buffer[5])

    a=stripdown(buffer[6])
    b=stripdown(buffer[7])

    a=quersumm(a)
    b=quersumm(b)

    c = c-(a+b)
    bbuffer[5] = c

    linkresponse = ""
    for el in bbuffer:
        linkresponse = linkresponse + '/'
        linkresponse = linkresponse + str(el)
    return linkresponse

def stripdown(string):
    string = ''.join(c for c in string if c.isdigit())
    return string

def quersumm(string):
    quersumme = sum([int(i) for i in string])
    return quersumme


def rawLinkHelper():
    menulinks = {"New": "http://www.sxyprn.com"}

    r = requests.get("http://www.sxyprn.com")
    soup = BeautifulSoup(r.text, 'html.parser')
    soup = soup.find_all("div", {"class": "block_header"})
    for element in soup:
        if element.find("span").text == "Popular HashTags":
            soup = element
            soup = soup.find_all("a", {"class": "tdn"})

    for element in soup:
        link = element.get("href")
        name = element.find("span", {"class":"htag_el_tag"}).text
        menulinks[name] = "http://www.sxyprn.com"+link

    return menulinks

def get_container():
    menupoints = rawLinkHelper()
    VIDEOS = {}

    for tag in menupoints:
        VIDEOS[tag] = menupoints[tag]

    return VIDEOS

def get_categories():
    menulinks = []
    menulinks.append({"name": "### New", "thumb": "", "link": "http://www.sxyprn.com"})

    r = requests.get("http://www.sxyprn.com")
    soup = BeautifulSoup(r.text, 'html.parser')
    soup = soup.find_all("div", {"class": "block_header"})
    for element in soup:
        if element.find("span").text == "Popular HashTags":
            soup = element
            soup = soup.find_all("a", {"class": "tdn"})

    for element in soup:
        link = element.get("href")
        name = element.find("span", {"class": "htag_el_tag"}).text

        menulinks.append({"name": name, "thumb": "", "link": "http://www.sxyprn.com" + link})

    return menulinks

def get_videos(categories):
    category = eval(categories)
    return get_linklist(category['link'])


if __name__ == "__main__":
    ###Self Test

    testCategories = get_categories()
    testList = get_videos(str(testCategories[0]))
    testVid = get_moviesrc(testList[0]["video"])
    print("end")