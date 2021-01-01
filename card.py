import db


class Card: 
    conn = db.connect('vocab.db')
    fields = [row[1:3] for row in conn.execute(''' PRAGMA table_info(vocabulary);''')]  

    def __init__(self, **kwargs): 
        for field in self.fields:
           setattr(self, field[0], kwargs.get(field))  
        self.edit_flag = False

    def __setattr__(self, name, value):
        self.__dict__['edit_flag'] = True
        self.__dict__[name] = value

    def __str__(self): 
        return "\n".join([att + ": " + 
            str(getattr(self,att)) 
            for att in vars(self) if getattr(self,att)])

