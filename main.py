#!/usr/bin/env python
# encoding: utf-8

from ieee import get_abstract_ieee
from springer import get_abstract_springer
from acm import get_abstract_acm
from de_gruyter import get_abstract_dg
from projecteuclid import get_abstract_projecteuclid

file_content = ''
file_name_proceedings = 'get_ee_journals_part3.txt'
f = open(file_name_proceedings,'r')
line = f.readline()
temp=1
cometo=15081
f2 = open('other_urls.txt','a')
f3=open('informationLost.txt','a')
while line:
    print line.strip()
    if temp>cometo and temp<20000:
        if line == '\n':
            line = f.readline()
            continue
        url = line.strip()
        if url[0:26] == 'http://ieeexplore.ieee.org' or url[0:25] == 'http://dx.doi.org/10.1109' or url[0:42]=='http://doi.ieeecomputersociety.org/10.1109':
            get_abstract_ieee(url,f3)
        elif url[0:25] == 'http://dx.doi.org/10.1007' or url[0:24] == 'http://link.springer.com'\
                or url[0:25] == 'http://dx.doi.org/10.1023':
            get_abstract_springer(url,f3)
        elif url[0:17] == 'http://dl.acm.org' or url[0:26] == 'http://doi.acm.org/10.1145' \
                or url[0:25] == 'http://dx.doi.org/10.1145':
            get_abstract_acm(url,f3)
        elif url[0:25] == 'http://dx.doi.org/10.1215'or url[0:25] == 'http://dx.doi.org/10.1305'\
                or url[0:24] == 'http://projecteuclid.org':
            get_abstract_projecteuclid(url,f3)
        elif url[0:24] == 'http://www.degruyter.com' or url[0:25] == 'http://dx.doi.org/10.2478':
            get_abstract_dg(url,f3)
        else:
           f2.write(url+'\n')
    print 'come to '+str(temp)+'\n'
    line = f.readline()
    temp+=1
f.close()
f2.close()
f3.close()