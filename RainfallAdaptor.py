from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

originalFolder = r"C:\QPESUM\RainfallTest\original"
xmlFileList = [f for f in listdir(
    originalFolder) if isfile(join(originalFolder, f))]

prefix = r'{http://www.wldelft.nl/fews/PI}'

fileName = join(originalFolder, xmlFileList[0])
tree = ET.parse(fileName)

root = tree.getroot()
seriesList = root.findall(prefix + 'series')

for series in seriesList:
    header = series.find(prefix + 'header')
    x = header.find(prefix + 'x').text
    y = header.find(prefix + 'y').text

    eventList = series.findall(prefix + 'event')
    for event in eventList:
        date = event.attrib['date']
        time = event.attrib['time']
        rainfallValue = event.attrib['value']
        if rainfallValue > 0 and rainfallValue < 200:
