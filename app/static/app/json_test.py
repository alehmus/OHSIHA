import json, requests

url = f'http://api.publictransport.tampere.fi/prod/?user=aleksilehmus&pass=ohsiha123&code=0011&request=stop'
#xml_url = '/Users/aleksilehmus/Documents/Koulu/TLO/OHSIHA/harkka/projekti/app/static/app/pysakkidata.xml'
#temp_url = '/Users/aleksilehmus/Documents/Koulu/TLO/OHSIHA/harkka/projekti/app/static/app/stopdata.txt'

r = requests.get(url)

dep = r.json()[0]["departures"]

for ele in dep:
    s = ele["code"] + ": " + ele["time"]
    print (s)

f = open(xml_url, "r", encoding='utf-8-sig')
temp = open(temp_url, "w", encoding='utf-8-sig')

pysakit = []

for line in f:
    osat = line.split("'")
    pysakki = osat[3].replace("&#228;", "ä")
    pysakki = pysakki.replace("&#246;", "ö")
    pysakki_koodi = osat[1]
    temp.write(pysakki+"/"+pysakki_koodi+"\n")