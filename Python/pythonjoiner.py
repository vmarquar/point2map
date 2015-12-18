joined = {}

for ID in IDs:
	for nameSplit in namesSplit:
	    if nameSplit[5:9] == ID:
                    joined[ID] = nameSplit
					print "found smth:{0}{1}".format(joined,nameSplit)

for ID in IDs:
	for nameSplit in namesSplit:
	    if nameSplit[6:10] == ID:
                  joined[ID] = nameSplit

with codecs.open('Z:/point2map_v02/names_processed_joined.txt','w',encoding='utf8') as f:
  f.write(joined)
