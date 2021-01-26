from dbconnector import get_cursor
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
        curs = get_cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voted'")
        if curs.fetchone()[0]==1 :
            print("List found, deleting...")
            curs.execute("DROP table voted;")
            curs.commit()
            curs.close()
            print("List deleted")
        else:
            print("No voted list found, Please create one using '-new'")

    def create(self):
        curs = get_cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voted'")
        if curs.fetchone()[0]==1 :
            print("List found, starting reset")
            curs.execute("DROP table voted;")
            print("List removed. Creating new list")
            curs.execute("CREATE TABLE voted(studNr TEXT)")
            curs.commit()
            curs.close()
        else:
            print("Creating new list")
            curs.execute("CREATE TABLE voted(studNr TEXT)")
            curs.commit()
            curs.close()


voter = Vote()