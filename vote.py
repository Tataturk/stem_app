from dbconnector import get_cursor
from dbconnector import delete_db
from encryption import generate_keys
class Vote():
    
    _voters = []
    _casts = []

    def __init__(self):
        #Check state
        curs = get_cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='casts';")
        if curs.fetchone()[0]=='casts' :
            print('Table exists.')
            self._voters = [voters[0] for voters in curs.execute("SELECT studNr FROM voted")]
            self._casts = [voters[0] for voters in curs.execute("SELECT studNr FROM voted")]
        
            print(self._voters)
        else:
            #Generate new public private keys
            generate_keys()

        
    def vote(self, voteId, candId):
        if voteId in self._voters:
            pass

    def delete(self):
        delete_db()
        print("Lists deleted")

    def create(self):
        delete_db()
        print("Lists deleted")

    
    def res(self):
        pass



voter = Vote()