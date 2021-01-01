import db


class Card: 
    conn = db.connect('vocab.db')
    fields = [row[1:3] for row in conn.execute(''' PRAGMA table_info(vocabulary);''')]  

    def __init__(self, **kwargs): 
        for field in self.fields:
           setattr(self, field[0], kwargs.get(field))  
           setattr(self, edit_flag, False)

    def edit(self):
        edit_flag = True

    

    def __str__(self): 
        return "\n".join([att + ": " + 
            str(getattr(self,att)) 
            for att in vars(self) if getattr(self,att)])

