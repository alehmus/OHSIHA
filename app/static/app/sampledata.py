import csv

aikataulut = {
    'Itsenaisyydenkatu 10': {},
    'Uintikeskus': {'0400': '3A'},
    'Testi': {'xxxx': 'yyyy'}
}

path = '/Users/aleksilehmus/Documents/Koulu/TLO/OHSIHA/harkka/projekti/app/static/app/sampledata2.csv'

file=open( path, "r", encoding='utf-8-sig')
reader = csv.reader(file)
for list in reader:
    for line in list:
        osat = line.split(";")
        aikataulut['Itsenaisyydenkatu 10'].update({osat[0]: osat[1]})