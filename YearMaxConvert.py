from SQLiteFunction import *
from XYZToAscii import XYZtoAscii

database = r"C:\Users\Tan Yong Keng\Desktop\SQLite\QPESUM_test5.db"
conn = createConnection(database)
selectLocation = "SELECT location_id FROM Locations"
locationIDListTemp = selectSQL(conn, selectLocation)
locationIDList = []
for locationIDTemp in locationIDListTemp:
    locationIDList.append(locationIDTemp[0])

# for duration in [1, 3, 6, 12]:
#     for year in range(2006, 2021):
duration, year = 1, 2006
outXYZ = []
for locationID in locationIDList:
    x = float(locationID.split('_')[0])
    y = float(locationID.split('_')[1])
    selectMaxRainfall = f"SELECT maxRainfall FROM MaxRainfalls WHERE location_id = '{locationID}' AND year = {year} AND duration = {duration}"
    maxRainfall = selectSQL(conn, selectMaxRainfall)
    outXYZ.append((x, y, maxRainfall[0][0]))
toAscii = XYZtoAscii(outXYZ)
toAscii.setProperty()
toAscii.initialTreeMap()
toAscii.getSortedTree()
toAscii.setAsciiContent()
print(toAscii.outList)
print(len(toAscii.outList))
fileAdd = r'C:\Users\Tan Yong Keng\Desktop\QPESUM Project' + r'\test.asc'
toAscii.saveAscii(fileAdd)