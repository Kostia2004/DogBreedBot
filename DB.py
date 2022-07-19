import sqlite3

class DataBase:
    obj = None
    def __init__(self):
        connection = sqlite3.connect('main.db', check_same_thread=False)
        self.cursor = connection.cursor()

    def __new__(cls, *args, **kwargs): #Singleton realisation
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj
    
    def getBreedById(self, idlist: list) -> dict:
        self.cursor.execute(f"SELECT * FROM breeds WHERE id IN {tuple(idlist)}")
        return dict(self.cursor.fetchall())
