#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

def check_version():
    v = sys.version_info
    if v.major == 3 and v.minor >= 2:
        curr = os.path.abspath(os.path.dirname(sys.argv[0]))
        downpath = os.path.join(curr,'pythonlib')
        sys.path.append(downpath)
        return True
    print('Your current python is %d.%d. Please use Python 3.4.' % (v.major, v.minor))
    return False

if not check_version():
    exit(1)

import os, io, re, time, sys, socket, urllib
from bs4 import BeautifulSoup
from urllib import parse
from multiprocessing import Pool
from datetime import datetime
from optparse import OptionParser
import requests
from lib_socks_proxy_2013_10_03 import monkey_patch as socks_proxy_monkey_patch
from lib_socks_proxy_2013_10_03 import socks_proxy_context
from requests import Request, Session
from bencodepy import encode as ben
from bencodepy import decode as bde
import hashlib, base64
socks_proxy_monkey_patch.monkey_patch()
findlist = []
tlistSN = []

class getSN:
    def __init__(self,argv):
        self.argv = argv
        self.url_default = r'http://t66y.com/thread0806.php?fid=7'
        self.url_search = r'http://www.t66y.com/search.php'
        self.url_base = r'http://t66y.com/'
        self.url_login = r'http://t66y.com/login.php?'
        self.url_gif_base = r'http://www.t66y.com/thread0806.php?fid=7&search=&page='
        self.url_magnet = ''
        self.url_for_view = None
        self.current_path = os.path.abspath(os.path.dirname(self.argv[0]))
        self.web_head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
        self.web_head_post = None
        self.requestMethod = 'POST'
        self.web_head_to = None
        self.opener=None
        self.session = None
        self.cookies = None
        self.findlist = []
        self.mip = None
        self.mport = None
        self.uname = None
        self.password = None
        self.user = None

    def webHandler(self, url, postValue, method='', saveLocally=False, con=False,type=None):
        content=None
        s = self.session
        s.headers = {}
        try:
            socket.setdefaulttimeout(30)
            if method==None:
                s.headers.update(self.web_head)
                if (self.mip != None) and (self.mport != None):
                    with socks_proxy_context.socks_proxy_context(proxy_address=(self.mip,self.mport)):
                        req = s.get(url, timeout=25, cookies=self.cookies)
                else:
                    req = s.get(url, timeout=25)
            else:
                if type=='torr':
                    s.headers.update(self.web_head_to)
                elif con==False:
                    s.headers.update(self.web_head_post)
                else:
                    s.headers.update(self.web_head_contribute)
                if (self.mip != None) and (self.mport != None):
                    with socks_proxy_context.socks_proxy_context(proxy_address=(self.mip,self.mport)):
                        req = s.post(url, data=postValue, timeout=25, cookies=self.cookies)
                else:
                    req = s.post(url, data=postValue, timeout=25)
            self.cookies = req.cookies
            if type=='gif':
                content=req.content
            elif type=='torr':
                content=req.content
            else:
                req.encoding = 'gbk'
                content=req.text
        except socket.timeout or socket.gaierror or lib_socks_proxy_2013_10_03.socks_proxy.ConnectSocksProxyError as e:
            print('error socket.timeout')
            if type=='gif':
                self.webHandler(url, None, None,type='gif')
            else:
                self.webHandler(url, None, None)
            return content
        except TypeError or ConnectionAbortedError or ConnectionResetError or UnicodeDecodeError or RuntimeError as e:
            print('error ConnectionAbortedError')
            if type=='gif':
                self.webHandler(url, None, None,type='gif')
            else:
                self.webHandler(url, None, None)
            return content
        except requests.exceptions.ReadTimeout or requests.exceptions.HTTPError or requests.exceptions.Timeout as e:
            print('error requests.exceptions.ReadTimeout')
            if type=='gif':
                self.webHandler(url, None, None,type='gif')
            else:
                self.webHandler(url, None, None)
            return content
        except requests.exceptions.ReadTimeout or requests.exceptions.TooManyRedirects  or requests.exceptions.ChunkedEncodingError as e:
            print('error TooManyRedirects')
            if type=='gif':
                self.webHandler(url, None, None,type='gif')
            else:
                self.webHandler(url, None, None)
            # return content
        except requests.exceptions.ConnectTimeout as e:
            print('error ConnectTimeout')
            if type=='gif':
                self.webHandler(url, None, None,type='gif')
            else:
                self.webHandler(url, None, None)
            return content
        except requests.exceptions.ConnectionError as e:
            print('error requests.exceptions.ConnectionError')
            # if type=='gif':
            #     self.webHandler(url, None, None,type='gif')
            # else:
            #     self.webHandler(url, None, None)
            # return content
        except requests.exceptions.ChunkedEncodingError as e:
            print('error requests.exceptions.ChunkedEncodingError')
            if type=='gif':
                self.webHandler(url, None, None,type='gif')
            else:
                self.webHandler(url, None, None)
            return content
        # except  as e:
        #     print('error socket.gaierror')
        #     return content
        # except UnicodeDecodeError as e:
        #     print('error UnicodeDecodeError')
        #     return content
        # except RuntimeError as e:
        #     print('error RuntimeError')
        #     return content
        # except requests.exceptions.HTTPError as e:
        #     print('error HTTPError')
        #     if type=='gif':
        #         self.webHandler(url, None, None,type='gif')
        #     return content
        # except requests.exceptions.Timeout as e:
        #     print('error Timeout')
        #     if type=='gif':
        #         self.webHandler(url, None, None,type='gif')
        #     return content
        # except requests.exceptions.ConnectionError as e:
        #     print('error requests.exceptions.ConnectionError')
        #     if type=='gif':
        #         self.webHandler(url, None, None,type='gif')
        #     return content
        # except requests.exceptions.ChunkedEncodingError as e:
        #     print('error requests.exceptions.ChunkedEncodingError')
        #     if type=='gif':
        #         self.webHandler(url, None, None,type='gif')
        #     return content
        # except requests.exceptions.ReadTimeout as e:
        #     print('error requests.exceptions.ReadTimeout')
        #     if type=='gif':
        #         self.webHandler(url, None, None,type='gif')
        #     return content
        # except TypeError as e:
        #     print('TypeError')
        #     return content

        if saveLocally == True:
            with open(self.local_page_content,"w") as fp:
                try:
                    fp.write(content)
                except UnicodeDecodeError as e:
                    print('error UnicodeDecodeError')
                    return content
        return content

    def downloadGIF(self,list_t):
        url=list_t[0]
        name=list_t[1]
        print('downloading gif:%s' % name)
        path = os.path.join(self.download_path,(str(name) + '.gif'))
        if os.path.exists(path):
            print('File already downloaded!')
            return True
        content = self.webHandler(url, None, None,type='gif')
        if content != None:
            with open(path,'wb') as fp:
                fp.write(content)
                return True
        else:
            return False

    def filterdiv(self,url,type='gif',title=None):
        firstContent=None
        SN = []
        mDate=[]
        mPDate=[]
        if url !=None:
            content = self.webHandler(url, None, None)
            if content !=None:
                try:
                    soup = BeautifulSoup(content,"html.parser")
                except RuntimeError as e:
                    print("error RuntimeError")
                    return False
                if type == 'gif':
                    link_gif_list = []
                    for content_t1 in soup.find_all('li'):
                        if content_t1.find_all('img') != None:
                            for content_t2 in content_t1.find_all('img'):
                                link_gif_list.append(content_t2['src'])
                    for block in soup.find_all('div'):
                        if block.get('class')!=None:
                            if block.get('class')==['tpc_content','do_not_catch']:
                                if block.find_all('img') != None:
                                    for content_t2 in block.find_all('img'):
                                        link_gif_list.append(content_t2['src'])
                    print('link_gif_list: %s' % len(link_gif_list))
                    if len(link_gif_list)<1:
                        return False
                    self.download_path = os.path.join(self.gif_path,title)
                    try:
                        os.mkdir(self.download_path)
                    except FileExistsError as e:
                        print('FileExistsError')
                    num = len(link_gif_list)
                    t_list = list(zip(link_gif_list,range(num)))
                    pool = Pool(5)
                    pool.map(self.downloadGIF,t_list)
                    pool.close()
                    pool.join()
                    print('One post downloaded! \n')
                    return

    def refreshNewPost(self, type='gif'):
        url_new=None
        content = self.webHandler(self.url_default, None, None)
        for i in range(1,6):
            print("Start to download on page :%s" % i)
            url_gif_page = self.url_gif_base + str(i)
            content = self.webHandler(url_gif_page, None, None)
            if content !=None:
                try:
                    soup = BeautifulSoup(content,"html.parser")
                except RuntimeError as e:
                    print("error RuntimeError")
                    return
                for block in soup.find_all('tr'):
                    for pos in block.find_all('td'):
                        if pos.get('class')!=None:
                            if pos.get('class')==['tal', 'f10', 'y-style']:
                                title = block.find('h3').string
                                url_last = block.find('h3').find('a').get('href')
                                if type=='gif':
                                    search_res = re.search(r'gif', title) or re.search(r'GIF', title) or re.search(r'动图', title) or re.search(r'动态', title)
                                if search_res:
                                    if type=='gif':
                                        path = os.path.join(self.gif_path,'findlist.txt')
                                        alreadyfind=False
                                        if os.path.exists(path):
                                            with open(path,'r') as fp:
                                                self.findlist=fp.readlines()
                                        else:
                                            with open(path,'a+') as fp:
                                                self.findlist=fp.readlines()
                                        for j in range(len(self.findlist)-1):
                                            if url_last == self.findlist[j].strip():
                                                alreadyfind=True
                                                print('already downloaded the:%s \n' % url_last)
                                                break
                                        if not alreadyfind:
                                            with open(path,'a') as fp:
                                                fp.write(url_last)
                                                fp.write('\n')
                                            url_new = self.url_base + url_last
                                            try:
                                                print('find match :%s'% title)
                                            except UnicodeEncodeError as e:
                                                print('UnicodeEncodeError')
                                                print('find match :%s'% title.encode("GB18030"))
                                                # break
                                            print('find match :%s'% url_new)
                                            if type=='gif':
                                                if re.search(r'[?？，.！（）\\/\*:<>|]*', title):
                                                    title = re.sub(r'[?？，.！（）\\/\*:<>|]*','',title)
                                                self.filterdiv(url_new,type='gif',title=title)
                                            time.sleep(5)
                print("Finished downloading on page :%s \n\n" % i)
                print('Location:%s' % self.gif_path)
            else:
                print('None content found')

    def getMagnet(self,link):
        content = self.webHandler(link, None, None)
        if content !=None:
            try:
                soup = BeautifulSoup(content,"html.parser")
            except RuntimeError as e:
                print("error RuntimeError")
                return
            for block in soup.find_all('div'):
                if block.get('class')!=None:
                    if block.get('class')==['tpc_content','do_not_catch']:
                        firstContent = block
                        if firstContent!=None:
                            magnetList = re.findall(r'magnet:\?xt=urn:btih:[0-9a-zA-Z-&=\%\_\.]*',content)
                            print("Find totle %s magnet link." % len(magnetList))
                            with open(self.magnet_path,'w',encoding= 'utf-8') as fp:
                                for x in magnetList:
                                    fp.write(x)
                                    fp.write('\n\r')
                            exit()
            print('No magnet find in this website')

    def getGIF(self):
        self.refreshNewPost(type='gif')

##########################download torrent############################

    def filfromsearch(self,sspath):
        # torr_path = os.path.join(self.current_path,'torrent')
        torr_path = sspath
        spath = os.path.join(torr_path,'search.txt')
        downpath = os.path.join(torr_path,'downloadedlist.txt')
        infopath = os.path.join(torr_path,'info.txt')
        magpath = os.path.join(torr_path,'tomagnet.txt')
        alreadydown = False
        downcount = 0
        with open(spath,'r',encoding= 'gbk') as fp:
            content =fp.read()
        pagetmp = re.findall(r'read.php\?tid=[0-9]{7}\&keyword=',content)
        soup = BeautifulSoup(content,"html.parser")
        all = soup.find_all('a')
        print('find %s links' % len(pagetmp))
        for i in pagetmp:
            for page in all:
                if page.get('href') == i:
                    ttitle = page.string
                    if re.search(r'[?？，.！（）\\/\*:<>|]*', ttitle):
                        ttitle = re.sub(r'[?？，.！（）\\/\*:<>|]*','',ttitle)
                    try:
                        print(ttitle)
                    except UnicodeEncodeError as e:
                        print('UnicodeEncodeError')
                        print(ttitle.encode("GB18030"))
                    break
            tlink = self.url_base + i
            print(tlink)
            linkid = re.findall(r'[0-9]{7}',i)[0]
            if os.path.exists(downpath):
                with open(downpath,'r') as fp:
                    downlist=fp.readlines()
            else:
                with open(downpath,'a+') as fp:
                    downlist=fp.readlines()
            if downlist != None:
                for i in range(len(downlist)):
                    if linkid == downlist[i].strip():
                        alreadydown=True
                        break
                    else:
                        alreadydown=False
            downcount+=1
            if alreadydown!=True:
                flinkt = self.searchtofinal(tlink)
                if flinkt != None:
                    tolinkt = self.filrmdown(flinkt)
                    if tolinkt != None:
                        ttitle = str(downcount) + ' ' + ttitle
                        su,maglink = self.downloadTo(tolinkt,ttitle)
                        if su == True:
                            with open(downpath,'a') as fp:
                                fp.write(linkid)
                                fp.write('\n')
                            with open(magpath,'a') as fp:
                                fp.write(maglink)
                                fp.write('\n')
                            with open(infopath,'a') as fp:
                                try:
                                    fp.write('%s' % str(ttitle))
                                except UnicodeEncodeError as e:
                                    fp.write('%s' % ttitle.encode("GB18030"))
                                fp.write('\n')
                                fp.write(flinkt)
                                fp.write('\n')
                                fp.write(tolinkt)
                                fp.write('\n')
                                fp.write(maglink)
                                fp.write('\n\n')
                            try:
                                print('Successfully download %s downcount torrent \n\n' % ttitle)
                            except UnicodeEncodeError as e:
                                print('UnicodeEncodeError')
                                print('Successfully download %s downcount torrent \n\n' % ttitle.encode("GB18030"))
                            time.sleep(3)
                        # self.session = requests.Session()
                    else:
                        print('Download fail,pls try again later\n\n')
                        time.sleep(3)
                else:
                    print('No link find, sleep 2')
                    time.sleep(3)
            else:
                print('Already downloaded, will skip!\n\n')
                # time.sleep(2)

    def searchtofinal(self,tlink):
        p_content = self.webHandler(tlink, None, None)
        if p_content != None:
            if re.search(r'正在轉入主題',p_content):
                soup = BeautifulSoup(p_content,"html.parser")
                sect = soup.find_all('a')
                final_link = sect[(len(sect)-1)].get('href')
                print(final_link)
                return(final_link)

    def filrmdown(self,linkp):
        p_content = self.webHandler(linkp, None, None)
        rhashl = re.findall(r'[0-9a-zA-Z]{40,50}',p_content)
        if rhashl!=[]:
            rhash = rhashl[(len(rhashl)-1)]
            rmdownlink = r'http://www.rmdown.com/link.php?hash=' + rhash
            print(rmdownlink)
            return rmdownlink
        else:
            # self.filrmdown(linkp)
            return

    def downloadTo(self,link,title):
        self.web_head_to = {'Host':'www.rmdown.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0','Referer':link}
        topost = 'http://www.rmdown.com/download.php'
        content = self.webHandler(link, None, None)
        thash = re.findall(r'[0-9a-zA-Z]{40,50}',link)
        try:
            reff = re.findall(r'[0-9a-zA-Z]{14,20}==',content)
        except TypeError as e:
            return False,None
        torr_path = os.path.join(self.current_path,'torrent')
        torr_path = os.path.join(torr_path,self.uname)
        try:
            os.mkdir(torr_path)
        except FileExistsError as e:
            pass
        toname = title + '.torrent'
        topath = os.path.join(torr_path,toname)
        if (len(thash)<1) or (len(reff)<1):
            print("No ava value found!")
            return False,None
        files={'ref':(None,thash[0]),
            'reff':(None,reff[0]),
            'submit':(None,'download'),
        }
        contentp = self.webHandler(topost, files, self.requestMethod, type='torr')
        try:
            if contentp != None:
                with open(topath,'wb') as fp:
                    fp.write(contentp)
                    maglink = self.changetomag(topath)
                    return True,maglink
        except UnicodeEncodeError as e:
            print('UnicodeEncodeError')
            print(contentp.encode("GB18030"))

    def changetomag(self,tpath):
        with open(tpath,'rb') as fp:
            torrent = fp.read()
        metadata = bde(torrent)
        try:
            hashcontents = ben(metadata[b'info'])
        except TypeError as e:
            return 'None'
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = base64.b32encode(digest).decode('utf-8')
        paramstr = r'magnet:?xt=urn:btih:%s' % b32hash
        print(paramstr)
        return paramstr

    # def getallto(self):
    #     flink,ftitle = self.filfromsearch()
    #     tolink=[]
    #     # print(flink)
    #     if flink!=[]:
    #         for i in flink:
    #             tolinkt = self.filrmdown(i)
    #             tolink.append(tolinkt)
    #             time.sleep(5)
    #     # print(tolink)
    #     if tolink!=[]:
    #         for y in tolink:
    #             su = self.downloadTo(y)
    #             if su == True:
    #                 print('Successfully download %s torrent' % (tolink.index(y)+1))
    #                 time.sleep(5)

#######################################search################################

    def getsearchres(self,uname):
        torr_path = os.path.join(self.current_path,'torrent')
        torr_path = os.path.join(torr_path,uname)
        try:
            os.mkdir(torr_path)
        except FileExistsError as e:
            pass
        spath = os.path.join(torr_path,'search.txt')
        uname = uname.encode('gbk')
        if self.login():
            self.web_head_post = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Referer':self.url_search,'Host':'www.t66y.com',
            '(Request-Line)':'POST /search.php? HTTP/1.1',
            'DNT':'1',
            'Content-Type':'application/x-www-form-urlencoded',
            'Content-Length':'143'
            }
            content = self.webHandler(self.url_search, None, None)
            if content==None:
                print('Search content none')
                return False
            else:
                if re.search(r'驗證代碼',content):
                    print('Get Search Successfully!')
                    codelist = re.findall(r'<B>[0-9]{2}</B>',content)
                    if codelist[(len(codelist)-1)] != None:
                        rcodet = codelist[(len(codelist)-1)]
                        rcode = re.findall(r'[0-9]{2}',rcodet)[0]
                        print('rcode : %s' % rcode)
                        time.sleep(5)
                    else:
                        print('No rcode found.')
                        return
                else:
                    print('Get search Fail!')
                    return
            postvalue = {
            'step':'2','keyword':'',
            'method':'OR','pwuser':uname,
            'sch_area':'0','s_type':'all',
            'f_fid':'1','sch_time':'all',
            'orderway':'postdate','asc':'DESC',
            'randcode_a':rcode, 'randcode_b':rcode,
            }
            scontent = self.webHandler(self.url_search, postvalue, self.requestMethod)
            if scontent==None:
                print('Searched content none')
                return False
            else:
                if re.search(r'共搜索到',scontent):
                    print('Get Searched result Successfully!')
                    if re.findall(r'sid=[0-9]{8}',scontent)!= []:
                        sid = re.findall(r'sid=[0-9]{8}',scontent)[0]
                        time.sleep(5)
                        for i in range(1,6):
                            searchurl = r'http://www.t66y.com/search.php?step=2&' + str(sid) + r'&keyword=&method=OR&pwuser=%D1%A9%D4%CF&authorid=&orderway=postdate&s_type=all&f_fid=1&c_fid=&sch_time=all&sch_area=0&digest=&page=' + str(i)
                            self.web_head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                                'Referer':self.url_search,'Host':'www.t66y.com',
                                'DNT':'1'
                            }
                            spcontent = self.webHandler(searchurl, None, None)
                            if spcontent!=None:
                                if re.search(r'共搜索到',spcontent):
                                    print('Get Searched page %s result Successfully!' % str(i))
                                    with open(spath,'a') as fp:
                                        try:
                                            fp.write(spcontent)
                                        except UnicodeEncodeError as e:
                                            fp.write('%s' % ttitle.encode("GB18030"))
            time.sleep(5)

    def login(self):
        name1 = self.user.encode('gbk')
        postvalue = {'pwuser':name1, 'pwpwd':self.password, 'hideid':'0', 'cktime':'0', 'forward':self.url_default, 'jumpurl':self.url_default, 'step':'2'}
        self.web_head_post = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0','Referer':self.url_login,'Host':'t66y.com'}
        l_content = self.webHandler(self.url_login, postvalue, self.requestMethod)
        if l_content==None:
            print('Login content none')
            return False
        else:
            if re.search(r'順利登錄',l_content):
                print('Login Successfully!')
                time.sleep(5)
                return True
            else:
                print('Login Fail!')
                print(l_content)
                return False

    def parse_option(self, test=False,simulate=False):
        usage = "getCL.py [-g] [-l <http://link of the page>] "
        parser = OptionParser(usage)
        parser.add_option("-l", "--link", action="store",
                dest = "url", help = "Get magnet link of the page to file")
        parser.add_option("-i", "--ip", action="store",
                dest = "ip", help = "The IP address of your proxy,normally should be 127.0.0.1")
        parser.add_option("-p", "--port", action="store",
                dest = "port", help = "The port number of your proxy, e.g 1080")
        parser.add_option("-s", "--search", action="store",
                dest = "search", help = "Try to get search reslut of the user you typed")
        parser.add_option("-d", "--autosearch", action="store_true", default=False,
                dest = "ssearch", help = "Autosearch get search reslut of the user in user.txt")
        parser.add_option("-g", "--gif", action="store_true", default=False,
                dest = "GIF", help = "Get gif from website")
        parser.add_option("-t", "--tlink", action="store_true", default=False,
                dest = "torr", help = "Get torr from searched content")
        parser.add_option("-u", "--username", action="store",
                dest = "user", help = "Your username")
        parser.add_option("-w", "--password", action="store",
                dest = "password", help = "Your password")
        if (len(self.argv) == 1) and (not test):
            parser.print_help()
            parser.exit()
        (options, self.argv) = parser.parse_args()
        self.session = requests.Session()
        self.session.headers.update(self.web_head)
        if options.ip!= None:
            self.mip = options.ip
        if options.port!= None:
            self.mport = options.port
        if options.user!= None:
            self.user = options.user
        if options.password!= None:
            self.password = options.password
        self.mGIF = options.GIF
        if options.url != None:
            self.url_magnet = options.url
            self.magnet_path = os.path.join(self.current_path,'magnet.txt')
            print('Option Link=%s'%self.url_magnet)
            self.getMagnet(self.url_magnet)
            exit()
        if options.search != None:
            self.uname = options.search
            self.getsearchres(options.search)
            exit()
        if options.ssearch != False:
            sspath = os.path.join(self.current_path,'torrent')
            sspath = os.path.join(sspath,'user.txt')
            with open(sspath,'r',encoding = 'utf-8') as fp:
                userlist=fp.readlines()
            if userlist != None:
                for i in userlist:
                    if i.strip() != None:
                        if re.search(r'\ufeff',i.strip()):
                            i = re.sub(r'\ufeff','',i.strip())
                        else:
                            i = i.strip()
                        self.uname = i.strip()
                        print('\nWill get %s\'s post' % i.strip())
                        self.getsearchres(i.strip())
                        self.session = requests.Session()
                        time.sleep(5)
            exit()
        if options.torr != False:
            # self.getallto()
            ssspath = os.path.join(self.current_path,'torrent')
            supath = os.path.join(ssspath,'user.txt')
            with open(supath,'r',encoding = 'utf-8') as fp:
                userlist=fp.readlines()
            if userlist != None:
                for i in userlist:
                    if i.strip() != None:
                        if re.search(r'\ufeff',i.strip()):
                            i = re.sub(r'\ufeff','',i.strip())
                        else:
                            i = i.strip()
                        self.uname = i
                        sfpath = os.path.join(ssspath,i)
                        # print(i)
                        print('\nWill get %s\'s torrent' % i)
                        self.filfromsearch(sfpath)
            exit()
        if options.GIF != False:
            self.gif_path = os.path.join(self.current_path,'gif')
            try:
                os.mkdir(self.gif_path)
            except FileExistsError as e:
                # print('Gif_path already Exists')
                pass
            print('Try to Get Gif')
            self.getGIF()
            print('Finished download latest 5 page of gif!')
            exit()
        else:
            parser.print_help()
            parser.exit()

if __name__ == '__main__':
    mySN = getSN(sys.argv)
    mySN.parse_option()
