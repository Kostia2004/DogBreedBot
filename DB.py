import sqlite3

class DataBase:
    obj = None
    def __init__(self):
        self.connection = sqlite3.connect('main.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __new__(cls, *args, **kwargs): #Singleton realisation
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj
    
    def getBreedById(self, idlist: list) -> dict:
        ids = tuple(ident+1 for ident in idlist)
        self.cursor.execute(f"SELECT * FROM breeds WHERE id IN {ids}")
        return dict(self.cursor.fetchall())

    def writeRequest(self, 
                    user_id: int,
                    message_id: int,
                    scores: list) -> int:
        values = [message_id, user_id]
        values.extend(scores)
        fields = ['message_id', 'user_id']
        fields.extend(["score"+str(i+1) for i in range(120)])
        try:    
            sql = f"INSERT INTO history{tuple(fields)} VALUES({('?,'*len(fields))[:-1]})"
            print(sql)
        except Exception as e:
            print("sql", e)
        try:
            self.cursor.execute(sql, list(map(str, values)))
        except Exception as e:
            print("execute", e)
        self.connection.commit()
        return 0

