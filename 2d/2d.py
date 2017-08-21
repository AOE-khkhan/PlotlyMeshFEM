from myclass import database

db = database()
db.importNodes('node.txt')
db.importElements('element.txt')

if __name__ == "__main__":
    db.createElements()
    db.createContour()
    db.draw()
