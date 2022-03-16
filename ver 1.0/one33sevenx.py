#!/usr/bin/env python3
import requests,re,os,datetime,asyncio,psutil
from prettytable import PrettyTable; from bs4 import BeautifulSoup;from os import path;from qbittorrent import Client
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Red="\u001b[31m"; Green="\u001b[32m"; Yellow="\u001b[33m"; LightCyan='\033[96m'; Magenta="\033[35m"; LightBlue="\033[94m"; LightGray="\033[37m"; LightgreyBG='\033[47m'; Bold="\033[1m"; Reset = "\u001b[0m";
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_if_pos_running(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
            else:
                pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("Error match process name")
    return False
qB = check_if_pos_running('qBittorrent')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if qB == False:
   os.system("./qBittorrentLauncher-S.sh")
   qb = Client("http://127.0.0.1:8080/")
   qb.login("admin", "123456")
elif qB == True:
    qb = Client("http://127.0.0.1:8080/")
    qb.login("admin", "123456")
current_page=""
def torrentInfo_scraper():
    global current_page
    if path.exists("torrentdata.txt") == True:
        os.remove('torrentdata.txt')
    pages = {1:"https://1337x.to/home/",2:"https://1337x.to/popular-movies",3:"https://1337x.to/popular-foreign-movies",4:"https://1337x.to/popular-tv",5:"https://1337x.to/popular-music",6:"https://1337x.to/popular-apps",7:"https://1337x.to/popular-games",8:"https://1337x.to/popular-other"}
    intext =''
    while True:
        inAnswer = input("Enter => "+Yellow+"0:"+Green+"search, "+Yellow+"1:"+Green+"home,"+Yellow+" 2:"+Green+"movies, "+Yellow+"3:"+Green+"foreign movies, "+Yellow+"4:"+Green+"tv "+Yellow+"5:"+Green+"music "+Yellow+"6:"+Green+"app "+Yellow+"7:"+Green+"games "+Yellow+"8:"+Green+"other "+Magenta+":=> "+Reset)
        if inAnswer.isdigit():
            intext += inAnswer
            break;

    if intext.isdigit() and int(intext) < 9 and int(intext) != 0:
        URL = pages.get(int(intext))
        current_page += URL.split("/")[-1].rstrip(" ")
        req = requests.get(URL)
        soup = BeautifulSoup(req.text,"html.parser")
        f = open('torrentdata.txt','a')
        for link in soup.find_all('td'):
            f.write(str(link)+'\n')
        f.close()

    if intext.isdigit() and int(intext) == 0:
        headers = {"User-Agent":"Mozilla/5.0"}
        searchtxt = input("\nEnter"+LightCyan+" search item "+Magenta+":=> "+Reset)
        searchpnum = input("\nEnter"+LightCyan+" page# or return for default of 1"+Magenta+":=> "+Reset)
        pnum = ''
        if searchpnum == "":
            pnum += str(1)
        else:
            pnum += searchpnum
        URL = ''
        recentORseed = input("\nEnter"+LightCyan+" r for most recent OR s for top seeded OR return for default"+Magenta+":=> "+Reset)
        # f = open("searchState.txt","w")
        # f.write(searchtxt+"\n")
        # f.write(pnum+"\n")
        # f.write(recentORseed+"\n")
        # f.close()

        if recentORseed == 'r':
            URL += 'https://1337x.to/sort-search/{}/time/desc/{}/'.format(searchtxt,pnum)
        elif recentORseed == 's':
            URL += 'https://1337x.to/sort-search/{}/seeders/desc/{}/'.format(searchtxt,pnum)
        else:
            URL += "https://1337x.to/search/{}/{}/".format(searchtxt,pnum)
        req = requests.get(URL,headers=headers)
        soup = BeautifulSoup(req.text,"html.parser")
        f = open('torrentdata.txt','a')
        for link in soup.find_all('td'):
            f.write(str(link)+'\n')
        f.close()
    if current_page == "":
        current_page += "Search"
torrentInfo_scraper()

def pagePrintOut():
    global current_page;
    f = open('torrentdata.txt')
    tdata = f.read().split("\n")
    TL = tdata
    indexcount = 1
    PT = PrettyTable()
    print(LightCyan+"",end="")
    PT.field_names = ["Index","Name", "Seeders", "Leechers","Size","Time","Page"]
    for i in range(int(len(TL)/6)):
        name = re.sub(r".*<a href=\"","", TL[0],flags=re.IGNORECASE)
        name = re.sub(r"\">.*","", name,flags=re.IGNORECASE)
        displayname = re.sub(r"/torrent/[0-9]+/","", name,flags=re.IGNORECASE).replace('.',' ').replace('_',' ').replace('-',' ').replace("/","")

        seeder = re.sub(r".*seeds\">","", TL[1],flags=re.IGNORECASE)
        seeder = re.sub(r"</td>","",seeder,flags=re.IGNORECASE)

        leecher = re.sub(r".*leeches\">","", TL[2],flags=re.IGNORECASE)
        leecher = re.sub(r"</td>","",leecher,flags=re.IGNORECASE)

        size = re.sub(r".*uploader\">","", TL[4],flags=re.IGNORECASE)
        size = re.sub(r"<span.*","",size,flags=re.IGNORECASE)
        size = re.sub(r".*vip\">","",size,flags=re.IGNORECASE)
        size = re.sub(r".*user\">","",size,flags=re.IGNORECASE)

        time = re.sub(r".*\">","", TL[3],flags=re.IGNORECASE)
        time = re.sub(r"</td>","",time,flags=re.IGNORECASE)


        seeder = Green+seeder+Reset
        leecher = Red+leecher+Reset
        time = Magenta+time+Reset
        size = Yellow+size+Reset
        indexcountx = Yellow+str(indexcount)+Reset
        curp = ''
        pagex = LightBlue+current_page+Reset

        if indexcount % 2 == 0:
            displayname = Yellow+displayname+" "+Magenta+str(indexcount)+Reset
            indexcountx = Yellow+str(indexcount)+Reset
            PT.add_row([indexcountx,displayname,seeder,leecher,size,time,pagex])
            #PT.add_row([" "," "," "," "," "," "," "])
            indexcount += 1
            for i in range(6):
                TL.pop(0)
        else:
            displayname = Reset+ displayname+" "+LightCyan+str(indexcount)+Reset
            indexcountx = Reset+str(indexcount)+Reset
            PT.add_row([indexcountx,displayname,seeder,leecher,size,time,pagex])
            #PT.add_row([" "," "," "," "," "," "," "])
            indexcount += 1
            for i in range(6):
                TL.pop(0)

    print(PT)
pagePrintOut()

def torrentInfo_parser():
    torrentDict = {}
    f = open('torrentdata.txt')
    tordata = f.read(); f.close();
    torrent = re.findall(r'/torrent.*/">',tordata,flags=re.IGNORECASE);
    count = 1
    for line in torrent:
        line = 'https://1337x.to'+line.rstrip('">')
        d_in = {count:line}
        torrentDict.update(d_in)
        count += 1;
    return torrentDict
dictp = torrentInfo_parser()


def magnet_torrent_downloader(dictionary):
    f = open('tm.txt','a')
    print(Red+'\nEnter any non digit char to quite at any time\n'+Reset)
    while True:
        torrentgrab = input(Reset+"Enter # of torrent 2 be downloaded or all to download all torrents:"+Red)
        if torrentgrab.isalpha() == False and torrentgrab.isdigit() and torrentgrab != 'all':
            tdict  = dictionary.get(int(torrentgrab))
            if tdict != None:
                f.write(str(tdict)+'\n')
        elif torrentgrab == 'all':
                for key, value in dictionary.items():
                    f.write(str(value)+'\n')
                break
        else:
            break
    f.close()

    magnets = []
    if path.exists("tm.txt"):
        f = open('tm.txt')
        torrents = f.read().split('\n'); f.close(); torrents.remove('')
        os.remove('tm.txt')
        for torrent in torrents:
            req = requests.get(torrent)
            soup = BeautifulSoup(req.text,"html.parser")
            for link in soup.find_all('a'):
                linkstr = str(link.get('href'))
                if linkstr.startswith('magnet:') and linkstr not in magnets:
                    magnets.append(linkstr)
    if len(magnets) > 0:
        for mag in magnets:
            qb.download_from_link(mag)

magnet_torrent_downloader(dictp)

os.system("clear && printf '\e[3J'")
