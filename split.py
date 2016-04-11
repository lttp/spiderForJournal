file_content = ''
file_name_proceedings = 'get_ee_journals.txt'
f = open(file_name_proceedings,'r')
line = f.readline()
temp=1

f2 = open('get_ee_journals_part3.txt','a')

while line:

    line = f.readline()
    temp+=1


    if temp>124507:
        f2.write(line)
f.close()
f2.close()