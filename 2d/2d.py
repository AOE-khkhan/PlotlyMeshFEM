from myclass import database

db = database()
db.importNodes('nodesb.txt')
db.importElements('elements.txt')

if __name__ == "__main__":
    db.createElements()
    db.createContour()
    db.draw()
