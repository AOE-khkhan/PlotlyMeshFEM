# help
# node and element No.
# camera angle
# scale
import argparse
from myclass import database
#=====================================
# Argparse Command Line Options
#=====================================
print('Please type -h for a list of commands')
parser = argparse.ArgumentParser(description='Display the section of the 3D model...')
parser.add_argument('-sect', nargs=2, help='E.g. "python 3d.py -sect x 15" => show the sectional view at x=15')
parser.add_argument('-cam', nargs=3, type=float)
args = parser.parse_args()
print(args)
#=====================================
# Create an instance of Database class
# and import .txt files
#=====================================
db = database()
db.importNodes('node.txt')
db.importElements('element.txt')
if not args.sect == None:
    db.select2dPlotNodes(args)
    db.select2dPlotElements()
    # db.create2dPlotNodesData(args)
    db.create2dPlotElementsData(args)
    db.draw2d(args)
else:
    db.create3dPlotNodesData()
    # db.create3dPlotElementsData()
    db.draw3d()
