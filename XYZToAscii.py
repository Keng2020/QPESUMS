import math
import numpy as np


class XYZtoAscii:
    def __init__(self, xyzContent):
        self.xList, self.yList, self.zList = [], [], []
        self.outList = np.array([])
        for xyz in xyzContent:
            self.xList.append(xyz[0])
            self.yList.append(xyz[1])
            self.zList.append(xyz[2])
            self.cellSize = 0.0125
            self.noData = '-99'

    def round_half_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier

    def round_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def setProperty(self,):
        self.maxX = self.round_half_up(max(self.xList)+0.5*self.cellSize, 5)
        self.maxY = self.round_half_up(max(self.yList)+0.5*self.cellSize, 5)
        self.minX = self.round_half_up(min(self.xList)-0.5*self.cellSize, 5)
        self.minY = self.round_half_up(min(self.yList)-0.5*self.cellSize, 5)
        self.row = int(self.round_up(
            (self.maxY - self.minY)/self.cellSize, 4)) + 2
        self.col = int(self.round_up(
            (self.maxX - self.minX)/self.cellSize, 4)) + 2
        maxX = self.round_half_up(self.col*self.cellSize + self.minX, 5)
        minY = self.round_half_up(self.maxY - self.row*self.cellSize, 5)
        self.bottomX = self.round_half_up(self.minX + self.cellSize/2, 5)
        self.bottomY = self.round_half_up(minY + self.cellSize/2, 5)
        self.topX = self.round_half_up(maxX - self.cellSize/2, 5)
        self.topY = self.round_half_up(self.maxY - self.cellSize/2, 5)

    def initialTreeMap(self, ):
        self.outTree = {}
        row, col = self.row, self.col
        for tempRow in range(row):
            rowTree = {}
            for tempCol in range(col):
                rowTree.update({tempCol: []})
            self.outTree.update({tempRow: rowTree})

    def getSortedTree(self, ):
        boundaryMinX = self.minX
        boundaryMaxY = self.maxY
        for index in range(len(self.xList)):
            tempRow = int(self.round_half_up(
                (boundaryMaxY-self.yList[index])/self.cellSize, 5))
            tempCol = int(self.round_half_up(
                (self.xList[index]-boundaryMinX)/self.cellSize, 5))
            self.outTree.get(tempRow).get(tempCol).append(self.zList[index])

    def setAsciiContent(self, ):
        for row in range(self.row):
            tempList = []
            for col in range(self.col):
                valueList = self.outTree.get(row).get(col)
                if len(valueList) == 1:
                    tempList.append(valueList[0])
                elif len(valueList) == 0:
                    tempList.append(self.noData)
                else:
                    mean = round(sum(tempList)/len(tempList), 4)
                    tempList.append(mean)
                self.outTree.get(row).pop(col)
            self.outList = np.append(self.outList, tempList)
            # self.outTree.pop(row)

    def saveAscii(self, fileAdd):
        outArray = []
        with open(fileAdd, 'w') as f:
            f.write('NCOLS' + "  " + str(self.col) + "\n")
            f.write('NROWS' + "  " + str(self.row) + "\n")
            f.write('XLLCENTER' + "  " + str(self.bottomX) + "\n")
            f.write('YLLCENTER' + "  " + str(self.bottomY) + "\n")
            f.write('CELLSIZE' + "  " + str(self.cellSize) + "\n")
            f.write('NODATA_VALUE' + "  " + self.noData + "\n")
            count = 0;
            for i in range(self.row):
                for j in range(self.col):
                    f.write(str(self.outList[count]) + "  ")
                    count += 1
                f.write("\n")
