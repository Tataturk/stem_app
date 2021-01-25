from dbconnector import get_cursor

class Vote():
    
    _voters = []
    _casts = []

    def __init__(self):
        #Check state
        curs = get_cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='casts';")
        if curs.fetchone()[0]==1 : 
            print('Table exists.')

        

    def vote(self, voteId, candId):
        if voteId in self._voters:
            pass