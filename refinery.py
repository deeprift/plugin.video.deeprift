import requests
from bs4 import BeautifulSoup

class refinery():

    def __init__(self):
        self.Videos = None

    def get_linklist(self):

        s = requests.Session()
        r = s.get("http://www.sxyprn.com")
        soup = BeautifulSoup(r.text,'html.parser')

        ### Get List of Shitty Fuk Links
        ELEMENT = {}
        ELLIST = []


        step = soup.find_all("div", {"class": "post_el_small"})

        for element in step:

            linkstream = element.find('a', {"class": "js-pop"}).get('href')

            titlestream = element.find('div', {"class": "post_text"}).text
            titlestream = titlestream.encode('ascii', 'ignore')

            thumbstream = element.find('img', {"class": "mini_post_vid_thumb"}).get('src')
            thumbstream = thumbstream.replace('"', "")
            thumbstream = thumbstream.replace('=//', "")
            thumbstream = thumbstream.replace('//', '/')
            thumbstream = 'http://' + thumbstream
            thumbstream = thumbstream.replace('///', '//')
            ELEMENT = {'name': str(titlestream), 'thumb': str(thumbstream), 'video': str(linkstream), 'genre': 'New'}
            ELLIST.append(ELEMENT)

        return ELLIST


    def get_moviesrc(self,link):


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

        linkstream= self.decrypting(linkstream)

        linkstream = "https://sxyprn.com"+linkstream

        return linkstream


    def decrypting(self, link):
        buffer = link.split('/')
        bbuffer = buffer

        c=int(buffer[5])

        a=self.stripdown(buffer[6])
        b=self.stripdown(buffer[7])

        a=self.quersumm(a)
        b=self.quersumm(b)

        c = c-(a+b)
        print (c)
        bbuffer[5] = c

        linkresponse = ""
        for el in bbuffer:
            linkresponse = linkresponse + '/'
            linkresponse = linkresponse + str(el)
        return linkresponse

    def stripdown(self, string):
        string = ''.join(c for c in string if c.isdigit())
        return string

    def quersumm(self, string):
        quersumme = sum([int(i) for i in string])
        return quersumme


    @property
    def get_container(self):
        VIDEOS = {}
        SUB = {}
        ELEMENT = {}

        ELLIST =self.get_linklist()

        SUB = {'New': ELLIST}
        VIDEOS = SUB
        print("FUCKERY FUCKERY FUCKERY")

        return VIDEOS


    def get_videos(self):
        self.Videos = self.get_container
        return self.Videos


if __name__ == "__main__":

    x = refinery()
    print(x.get_videos())
    print("end")
