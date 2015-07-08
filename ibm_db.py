#coding=utf-8
import types
import ibm_db

limit = 500000

file = open("mengniu.dat","w")

conn = ibm_db.connect("DATABASE=mengniu;HOSTNAME=9.186.52.168;UID=db2admin;PWD=passw0rd;","","")
sql = "SELECT TITLE,MAIN_CONTENT,CONTENT_TYPE FROM webpage"
stmt = ibm_db.prepare(conn, sql)

ibm_db.execute(stmt)
#print ibm_db.num_rows(stmt)

dictionary = ibm_db.fetch_tuple(stmt)
count = 1
while dictionary != False and count <= limit:
	#sample show
    #print dictionary[0] #title
    #print dictionary[1] #main_content
    #print dictionary[2] #content_type
    #sample show end
    print count,':',dictionary[2]
    if dictionary[2] == 0:
    	if dictionary[0] == None:
    		file.write('0\nNone\n')
    	else:
    		file.write('0\n%s\n' % dictionary[0].encode('utf-8'))
    elif dictionary[2] == 1:
    	if dictionary[1] == None:
    		file.write('1\nNone\n')
    	else:
    		file.write('1\n%s\n' % dictionary[1].encode('utf-8'))

    #fetch next
    dictionary = ibm_db.fetch_tuple(stmt)
    count+=1

file.close()