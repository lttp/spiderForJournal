#!/usr/bin/env python
# encoding: utf-8

import re
import requests
import time
import random
import sys
from bs4 import BeautifulSoup
requests.adapters.DEFAULT_RETRIES = 5
reload(sys)
sys.setdefaultencoding('utf8')

file_name = 'acm.xml'
file_content = ''  # 最终要写到文件里的内容
articles_begin = '\n' + '<articles>' + '\n'
articles_end = '</articles>' + '\n'
headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'}
]

def get_abstract_acm(url,f3):
    f = open(file_name, 'a')
    file_content = ''
    source_code = ''
    loop_times = 0
    while loop_times < 5:
        try:
            time.sleep(random.randint(1, 10))
            source_code = requests.get(url,headers=random.choice(headers))  #为URL传递参数
            if source_code != '' and source_code.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            print 'try ' + str(loop_times+1) + ' times to open this article, filed!'
        finally:
            loop_times += 1
            if loop_times == 5:
                print 'Warning: Loop over 5 times on this article: ' + url


    if source_code.status_code == 200:
        plain_text = source_code.text     #获得整个html页面
        soup = BeautifulSoup(plain_text, "html.parser")  # 得到列表的soup对象
        author = ''
        insti = ''
        reference = ''

        file_content += articles_begin
        file_content += '<url>' + url + '</url>' + '\n'

        if soup.find('meta',{'name':'citation_abstract_html_url'}):
            abstract_html_url = soup.find('meta',{'name':'citation_abstract_html_url'})
            abstract_html_url = dict(abstract_html_url.attrs)['content']
            file_content += '<abstract_html_url>' + abstract_html_url + '</abstract_html_url>' + '\n'
        else:
            f3.write(url+" no abstract_html_url\n")
            print 'no abstract_html_url'
        if soup.find('meta',{'name':'citation_pdf_url'}):
            pdf_url = soup.find('meta',{'name':'citation_pdf_url'})
            pdf_url = dict(pdf_url.attrs)['content']
            file_content += '<pdf_url>' + pdf_url + '</pdf_url>' + '\n'
        else:
            f3.write(url+" no pdf_url\n")
            print 'no pdf_url'
        if soup.find('meta',{'name':'citation_doi'}):
            doi = soup.find('meta',{'name':'citation_doi'})
            doi = dict(doi.attrs)['content']
            file_content += '<doi>' + doi + '</doi>' + '\n'
        else:
            f3.write(url+" no doi\n")
            print 'no doi'
        if soup.find('meta',{'name':'citation_title'}):
            title = soup.find('meta',{'name':'citation_title'})
            title = dict(title.attrs)['content']
            file_content += '<title>' + title + '</title>' + '\n'
            print title + '\n'
        else:
            f3.write(url+" no title\n")
            print 'no title'
        if soup.find('meta',{'name':'citation_publisher'}):
            publisher = soup.find('meta',{'name':'citation_publisher'})
            publisher = dict(publisher.attrs)['content']
            file_content += '<publisher>' + publisher + '</publisher>' + '\n'
        else:
            f3.write(url+" no publisher\n")
            print 'no publisher'
        if soup.find('meta',{'name':'citation_journal_title'}):
            journal_title = soup.find('meta',{'name':'citation_journal_title'})
            journal_title = dict(journal_title.attrs)['content']
            file_content += '<journal_title>' + journal_title + '</journal_title>' + '\n'
        else:
            f3.write(url+" no journal_title\n")
            print 'no journal_title'
        if soup.find('meta',{'name':'citation_volume'}):
            volume = soup.find('meta',{'name':'citation_volume'})
            volume = dict(volume.attrs)['content']
            file_content += '<volume>' + volume + '</volume>' + '\n'
        else:
            f3.write(url+" no volume\n")
            print 'no volume'
        if soup.find('meta',{'name':'citation_issue'}):
            issue = soup.find('meta',{'name':'citation_issue'})
            issue = dict(issue.attrs)['content']
            file_content += '<issue>' + issue + '</issue>' + '\n'
        else:
            f3.write(url+" no issue\n")
            print 'no issue'
        if soup.find('meta',{'name':'citation_firstpage'}):
            first_page = soup.find('meta',{'name':'citation_firstpage'})
            first_page = dict(first_page.attrs)['content']
            file_content += '<first_page>' + first_page + '</first_page>' + '\n'
        else:
            f3.write(url+" no firstpage\n")
            print 'no firstpage'
        if soup.find('meta',{'name':'citation_lastpage'}):
            last_page = soup.find('meta',{'name':'citation_lastpage'})
            last_page = dict(last_page.attrs)['content']
            file_content += '<last_page>' + last_page + '</last_page>' + '\n'
        else:
            f3.write(url+" no lastpage\n")
            print 'no lastpage'
        if soup.find('meta',{'name':'citation_issn'}):
            issn = soup.find('meta',{'name':'citation_issn'})
            issn = dict(issn.attrs)['content']
            file_content += '<issn>' + issn + '</issn>' + '\n'
        else:
            f3.write(url+" no issn\n")
            print 'no issn'
        if soup.find('meta',{'name':'citation_date'}):
            date_of_publication = soup.find('meta',{'name':'citation_date'})
            date_of_publication = dict(date_of_publication.attrs)['content']
            file_content += '<date_of_publication>' + date_of_publication + '</date_of_publication>' + '\n'
        else:
            f3.write(url+" no date_of_publication\n")
            print 'no date_of_publication'

        # get authors
        authors_list = soup.find('table',{'style':'margin-top: 10px; border-collapse:collapse; padding:2px;'})
        try:
            for tr in authors_list.findAll('tr'):
                for td in tr.findAll('td'):
                    if td.find('a',{'title':'Author Profile Page'}):
                        author = td.find('a',{'title':'Author Profile Page'}).get_text().strip()
                    try:
                        insti = td.find({'title':'Institutional Profile Page'}).get_text().strip()
                    except AttributeError:
                        try:
                            insti = tr.find('small').get_text().strip()
                        except AttributeError:
                            f3.write(url+" no institution")
                            print 'no institution'
                if insti != '':
                    author = author + '  ++  ' + insti
                file_content += '<author>' + author + '</author>' + '\n'
        except AttributeError:
            f3.write(url+" no author and institution\n")
            print 'no author and institution'

        # get abstract
        abstract_url = get_url(soup, 'tab_abstract.cfm')
        if abstract_url is not None:
            source_code = ''
            loop_times = 0
            while loop_times < 5:
                try:
                    time.sleep(random.randint(1, 3))
                    source_code = requests.get(abstract_url,headers=random.choice(headers))  #为URL传递参数
                    if source_code != '' and source_code.status_code == 200:
                        break
                except requests.exceptions.ConnectionError:
                    f3.write(url+" open_abstract_url filed\n")
                    print 'try ' + str(loop_times+1) + ' times to open abstract_url, filed!'
                finally:
                    loop_times += 1
                    if loop_times == 5:
                        f3.write(url+" loop over 5 times to open abstract_url\n")
                        print 'Warning: Loop over 5 times to open abstract_url: ' + abstract_url

            if source_code.status_code == 200:
                plain_text = source_code.text     #获得整个html页面
                soup_abstract = BeautifulSoup(plain_text, "html.parser")  # 得到列表的soup对象
                abstract = ''
                try:
                    if soup_abstract.findAll('p'):
                        for abstract_str in soup_abstract.findAll('p'):
                            abstract += abstract_str.get_text().strip()
                    elif soup_abstract.findAll('par'):
                        for abstract_str in soup_abstract.findAll('par'):
                            abstract += abstract_str.get_text().strip()
                    else:
                        abstract = soup_abstract.find('div').get_text().strip()
                    if abstract != 'An abstract is not available.':
                        abstract = abstract.replace("\r\n", " ")
                        file_content += '<abstract>' + abstract + '</abstract>' +'\n'
                    else:
                        f3.write(url+" no abstract\n")
                        print 'no abstract'
                except AttributeError:
                    f3.write(url+" no abstract\n")
                    print 'no abstract'
            else:
                f3.write(url+" Request error not 200 when get abstract")
                print 'Request error not 200 when get abstract'

        # get keywords
        try:
            keywords = soup.find('meta',{'name':'citation_keywords'})
            keywords = dict(keywords.attrs)['content']
            for one in keywords.split(';'):
                keyword = one.strip()
                file_content += "<keyword>" + keyword + '</keyword>' + '\n'
        except AttributeError:
            f3.write(url+" no keywords\n")
            print 'no keywords'

        # get references
        references_url = get_url(soup, 'tab_references.cfm')
        if references_url is not None:
            source_code = ''
            loop_times = 0
            while loop_times < 5:
                try:
                    time.sleep(random.randint(1, 5))
                    source_code = requests.get(references_url,headers=random.choice(headers))  #为URL传递参数
                    if source_code != '' and source_code.status_code == 200:
                        break
                except requests.exceptions.ConnectionError:
                    print 'Warning: Loop over 5 times to open reference_url' + references_url
                finally:
                    loop_times += 1
                    if loop_times == 5:
                        print 'Loop over 5 times to open reference_url: ' + references_url

            if source_code.status_code == 200:
                plain_text = source_code.text     #获得整个html页面
                soup_reference = BeautifulSoup(plain_text, "html.parser")  # 得到列表的soup对象
                references = soup_reference.find('table')
                try:
                    for one in references.findAll('tr',{'valign':'top'}):
                        for one00 in one.findAll('div'):
                            refs = one00.stripped_strings
                            reference = ''
                            for ref in refs:
                                reference += ref
                            reference.replace('\t','')
                            reference.replace('\n','')
                        file_content += '<reference>' + reference + '</reference>' + '\n'
                except AttributeError:
                    if soup_reference.find('div').get_text().strip() == 'References are not available':
                        f3.write(url+" no references\n")
                        print 'no references'
                    else:
                        f3.write(url+" get references wrong\n")
                        print 'get references wrong'
            else:
                print 'Request error not 200 when get reference'

        file_content += articles_end + '\n'
        f.write(file_content)
        f.close()

    else:
        print 'Request error not 200'

def get_url(soup, start):
    oo = soup.find_all('script')
    startstr = start
    endstr = '\''
    conf_url = ''
    for one in oo:
        one = str(one.string)
        GetMiddleStr(one,startstr,endstr)
        conf_url = GetMiddleStr(one,startstr,endstr)
        if conf_url is not None:
            break
    if conf_url is not None:
        if startstr == 'tab_abstract.cfm':
            conf_url = 'http://dl.acm.org/tab_abstract.cfm' + conf_url
        elif startstr == 'tab_references.cfm':
            conf_url = 'http://dl.acm.org/tab_references.cfm' + conf_url
    return conf_url

def GetMiddleStr(content,startStr,endStr):
    patternStr = r'%s(.+?)%s'%(startStr,endStr)
    p = re.compile(patternStr,re.IGNORECASE)
    m = re.search(p,content)
    if m:
        return m.group(1)

