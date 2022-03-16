#!/usr/bin/env python3
#-------------------------------------------------------------------------------
''' imports '''
import os,requests,re,textwrap,psutil,sys;
from bs4 import BeautifulSoup;
from prettytable import PrettyTable;
from os import path
from qbittorrent import Client
from os.path import exists
#-------------------------------------------------------------------------------
''' Color Varibles for coloring printed output '''
RED="\u001b[31m"; GREEN="\u001b[32m"; YELLOW="\u001b[33m"; LIGHTCYAN='\033[96m';
MAGENTA="\033[35m"; LIGHTBLUE="\033[94m"; RESET="\u001b[0m"; SKYBLUEBG='\33[46m';
LIGHTGREYBG='\033[47m'  
#-------------------------------------------------------------------------------
''' return a list of 3 pages to be scraped '''
def search():
    URL = []
    print("\nEnter %stext%s only for default settings%s"%(YELLOW,LIGHTCYAN,RESET))
    print("\nEnter %stext +r%s for %smost recent%s %s{%sex%s:ubuntu +r}%s"%
    (YELLOW,LIGHTCYAN,YELLOW,LIGHTCYAN,LIGHTCYAN,YELLOW,LIGHTCYAN,RESET))
    print("\nEnter %stext +s%s for %stop seeded%s  %s{%sex%s:kali linux +s}%s"%
    (YELLOW,LIGHTCYAN,YELLOW,LIGHTCYAN,LIGHTCYAN,YELLOW,LIGHTCYAN,RESET))
    searchtxt = input("\nEnter"+LIGHTCYAN+" search item "+MAGENTA+":=> "+RESET);
    if searchtxt.endswith('+r'):
        for i in range(1,8):
            URL.append('https://1337x.to/sort-search/{}/time/desc/{}/'.
            format(searchtxt.replace(' +r',''),i))
    elif searchtxt.endswith('+s'):
        for i in range(1,8):
            URL.append('https://1337x.to/sort-search/{}/seeders/desc/{}/'.
            format(searchtxt.replace(' +s',''),i))
    else:
        for i in range(1,8):
            URL.append("https://1337x.to/search/{}/{}/".
            format(searchtxt,i))
    return URL
#-------------------------------------------------------------------------------
''' WebPages Index '''
def link_grabber(incomingIndexNum):
    if incomingIndexNum == 0:
        return search()
    page_links_dictionary = {
    1:"https://1337x.to/home/",
    2:"https://1337x.to/popular-movies",
    3:"https://1337x.to/popular-foreign-movies",
    4:"https://1337x.to/popular-tv",
    5:"https://1337x.to/popular-music",
    6:"https://1337x.to/popular-apps",
    7:"https://1337x.to/popular-games",
    8:"https://1337x.to/popular-other",}
    return page_links_dictionary.get(incomingIndexNum)
#-------------------------------------------------------------------------------
''' prompts for input regard page(s) fetches'''
def input_grabber():
    print("\n%sABOUT%s This program grabs torrent files from %shttps://1337x.to.com%s"%(RED,RESET,RED,RESET))
    print("\n%sOPTIONS%s %s0%s will ask for more input, while %s1-8%s will return a given default page"%(RED,RESET,YELLOW,RESET,YELLOW,RESET))
    while True:
        inNum = input("\nEnter => %s0:%ssearch, %s1:%shome, %s2:%smovies, %s3:%sforeign movies, %s4:%stv, %s5:%smusic, %s6:%sapp, %s7:%sgames, %s8:%sother %s:=> %s"%
        (YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,YELLOW,GREEN,MAGENTA,RESET))
        if inNum.isdigit() and int(inNum) > -1 and int(inNum) < 9:
            os.system("clear && printf '\e[3J'")
            return link_grabber(int(inNum))
#-------------------------------------------------------------------------------
''' base webpage scraper '''
def link_toFile_writer():
    HEADERS = {"User-Agent":"Mozilla/5.0"};
    global current_page;
    URL_S = input_grabber()
    if isinstance(URL_S,list):
        current_page = "Search";
        for URL in URL_S:
            req = requests.get(URL,headers=HEADERS)
            soup = BeautifulSoup(req.text,"html.parser")
            with open("torrentdata.txt","a") as file:
                for link in soup.find_all('td'):
                    file.write(str(link)+'\n')
    else:
        URL = URL_S
        current_page = URL.rstrip("/").split("/")[-1].rstrip(" ").replace("popular-",'').replace("-movies",'')
        req = requests.get(URL,headers=HEADERS)
        soup = BeautifulSoup(req.text,"html.parser")
        with open("torrentdata.txt","a") as file:
            for link in soup.find_all('td'):
                file.write(str(link)+'\n')
#-------------------------------------------------------------------------------
def sorter():
    with open('torrentdata.txt') as file:
        torDataList = file.read().split("\n")
        for i in range(int(len(torDataList)/6)):
            displayname = re.sub(r".*<a href=\"|\">.*|/torrent/[0-9]+/|/|WEBRip|WEBDL","",torDataList[0],flags=re.IGNORECASE).replace('.',' ').replace('_',' ').replace('-',' ')
            displayname = re.sub(r"720p .*|1080p.*| Mp3.*|WEB DL|WEB .*|HDTV.*|REPACK|2160p.*|480p.*","",displayname)
            displayname = re.sub(r'\b([SE])(\d{1,2})', r'\1\2 ', displayname) #\1 refers to group 1 which is SE and \2 refers to group 2 which is \d
            displayname = re.sub(r'\b([E])(\d{1,2}) ', r'\1\2 ENDLINE-Show' ,displayname) #\1 refers to group 1 which is SE and \2 refers to group 2 which is \d
            displayname = re.sub(r'(\b(\d){4}\b)','', displayname)
            displayname = re.sub(r' ENDLINE-Show.*$', '', displayname) #\1 refers to group 1 which is SE and \2 refers to group 2 which is \d
            displayname = re.sub(r'[ \s]{1,}', ' ', displayname)

            seeder = re.sub(r".*seeds\">|</td>","", torDataList[1],flags=re.IGNORECASE)
            leecher = re.sub(r".*leeches\">|</td>","", torDataList[2],flags=re.IGNORECASE)
            size = re.sub(r".*uploader\">|<span.*|.*vip\">|.*mob-moderator\">|.*user\">","", torDataList[4],flags=re.IGNORECASE).replace('KB','AAA').replace('MB','BBB').replace('GB','CCC').replace('TB','DDD').split(" ")
            with open('temp.txt','a') as f:
                f.write(displayname+'^'+size[1]+'^'+size[0]+'^'+seeder+'^'+leecher+'^'+torDataList[0]+'^'+torDataList[1]+'^'+torDataList[2]+'^'+torDataList[3]+'^'+torDataList[4]+'^'+torDataList[5]+'\n')
            for i in range(6):
                torDataList.pop(0)
    if exists('./temp.txt') == True: os.system('cat temp.txt | sort -u > torrentdata.txt')
    if exists('./temp.txt') == True: os.remove('temp.txt')
    with open('torrentdata.txt') as file:
        updatedTorDataList = file.read().split("\n")
        for line in updatedTorDataList:
            if line != "":
                lineList = line.split("^")[5:]
                for item in lineList:
                    with open('temp.txt','a') as file2:
                        file2.write(item+'\n')
    if exists('./temp.txt') == True: os.system('cat temp.txt > torrentdata.txt')
    if exists('./temp.txt') == True: os.remove('temp.txt')
                
#-------------------------------------------------------------------------------

def tableGenPrintOut():
    with open('torrentdata.txt') as file:
        torDataList = file.read().split("\n")
        indexcount = 1
        PT = PrettyTable()
        PT.field_names = [
        SKYBLUEBG+"Index"+RESET,
        SKYBLUEBG+"Name"+RESET,
        SKYBLUEBG+"Seeders"+RESET,
        SKYBLUEBG+"Leechers"+RESET,
        SKYBLUEBG+"Size"+RESET,
        SKYBLUEBG+"Time"+RESET,
        SKYBLUEBG+"Page"+RESET]

        for i in range(int(len(torDataList)/6)):
            displayname = re.sub(r".*<a href=\"|\">.*|/torrent/[0-9]+/|/|WEBRip|WEBDL","",torDataList[0],flags=re.IGNORECASE).replace('.',' ').replace('_',' ').replace('-',' ')
            displayname = re.sub(r"720p .*|1080p.*| Mp3.*|WEB DL|WEB .*|HDTV.*|REPACK|2160p.*|480p.*","",displayname)
            displayname = re.sub(r'\b([SE])(\d{1,2})', r'\1\2 ', displayname) #\1 refers to group 1 which is SE and \2 refers to group 2 which is \d
            displayname = re.sub(r'\b([E])(\d{1,2}) ', r'\1\2 ENDLINE-Show' ,displayname) #\1 refers to group 1 which is SE and \2 refers to group 2 which is \d
            displayname = re.sub(r'(\b(\d){4}\b)','', displayname)
            displayname = re.sub(r' ENDLINE-Show.*$', '', displayname) #\1 refers to group 1 which is SE and \2 refers to group 2 which is \d
            displayname = textwrap.shorten(re.sub(r'[ \s]{1,}', ' ', displayname), width=70)

            seeder = re.sub(r".*seeds\">|</td>","", torDataList[1],flags=re.IGNORECASE)
            leecher = re.sub(r".*leeches\">|</td>","", torDataList[2],flags=re.IGNORECASE)
            size = re.sub(r".*uploader\">|<span.*|.*vip\">|.*mob-moderator\">|.*user\">","", torDataList[4],flags=re.IGNORECASE)
            time = re.sub(r".*\">|</td>","", torDataList[3],flags=re.IGNORECASE)

            seeder = GREEN+seeder+RESET
            leecher = RED+leecher+RESET
            time = MAGENTA+time+RESET
            pagex = LIGHTBLUE+current_page+RESET

            if indexcount % 2 == 0:
                displayname = YELLOW+displayname+" "+MAGENTA+str(indexcount)+RESET
                size = YELLOW+size+RESET
                indexcountx = MAGENTA+str(indexcount)+RESET
                PT.add_row([indexcountx,displayname,seeder,leecher,size,time,pagex])
                if len(sys.argv) > 1:
                    PT.add_row([str(len(indexcountx)*"-"),str(50*"-"),str(len(seeder)*"-"),str(len(leecher)*"-"),str(len(size)*"-"),str(len(time)*"-"),str(len(pagex)*"-")])
                indexcount += 1
                for i in range(6):
                    torDataList.pop(0)
            else:
                displayname = RESET+ displayname+" "+LIGHTCYAN+str(indexcount)+RESET
                size = RESET+size+RESET
                indexcountx = LIGHTCYAN+str(indexcount)+RESET
                PT.add_row([indexcountx,displayname,seeder,leecher,size,time,pagex])
                if len(sys.argv) > 1:
                    PT.add_row([str(len(indexcountx)*"-"),str(50*"-"),str(len(seeder)*"-"),str(len(leecher)*"-"),str(len(size)*"-"),str(len(time)*"-"),str(len(pagex)*"-")])
                indexcount += 1
                for i in range(6):
                    torDataList.pop(0)
    
    print(PT)
#-------------------------------------------------------------------------------
def torrentLinksDictionaryBuilder():
    torrentDict = {}
    with open('torrentdata.txt') as f:
        tordata = f.read();
        torrent = re.findall(r'/torrent.*/">',tordata,flags=re.IGNORECASE);
        count = 1
        for line in torrent:
            line = 'https://1337x.to'+line.rstrip('">')
            d_in = {count:line}
            torrentDict.update(d_in)
            count += 1;
        return torrentDict
#-------------------------------------------------------------------------------
def check_if_pos_running(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                qb = Client("http://127.0.0.1:8080/")
                qb.login("admin", "123456")
                return qb
            else:
                pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("Error match process name")
    os.system("./qBittorrentLauncher-S.sh")
    qb = Client("http://127.0.0.1:8080/")
    qb.login("admin", "123456")
    return qb
#-------------------------------------------------------------------------------
def magnet_torrent_download_Selector(dictionary):
    with open('tm.txt','a') as f:
        print(RED+'\nEnter any non digit char to quite at any time\n'+RESET)
        while True:
            torrentgrab = input(RESET+"Enter # of torrent to be downloaded or all to download all torrents:"+RED)
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
#-------------------------------------------------------------------------------
def magnet_torrent_downloader():
    magnets = []
    if path.exists("tm.txt"):
        with open('tm.txt') as f:
            torrents = f.read().split('\n')[:-1];
            if exists('./tm.txt') == True: os.remove('tm.txt')
            if exists('./temp.txt') == True: os.remove('temp.txt')
            if exists('./torrentdata.txt') == True: os.remove('./torrentdata.txt')
            for torrent in torrents:
                req = requests.get(torrent)
                soup = BeautifulSoup(req.text,"html.parser")
                for link in soup.find_all('a'):
                    linkstr = str(link.get('href'))
                    if linkstr.startswith('magnet:') and linkstr not in magnets:
                        magnets.append(linkstr)
        if len(magnets) > 0:
            qb = check_if_pos_running('qBittorrent')
            for mag in magnets:
                qb.download_from_link(mag)
#-------------------------------------------------------------------------------
def main():
    if exists('./tm.txt') == True: os.remove('tm.txt')
    if exists('./temp.txt') == True: os.remove('temp.txt')
    if exists('./torrentdata.txt') == True: os.remove('./torrentdata.txt')
    link_toFile_writer()
    sorter()
    tableGenPrintOut()
    torDictionary = torrentLinksDictionaryBuilder()
    magnet_torrent_download_Selector(torDictionary)
    magnet_torrent_downloader()
    os.system("clear && printf '\e[3J'")
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
