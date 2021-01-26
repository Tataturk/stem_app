import datetime
import sqlite3
from vote_frans import loadCandidates, loadVoters
from dbconnector import delete_db, get_cursor
from encryption import decrypt_string, encrypt_string, generate_keys, remove_keys


class Vote():
    
    _voters = []
    _casts = []

    gVoters = []
    gCandidates = []

    def __init__(self):
        #Check state
        curs, __ = get_cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='casts';")
        if curs.fetchone()[0]=='casts' :
            print('Table exists.')
            _voters = [voters[0] for voters in curs.execute("SELECT studNr FROM voted")]
            for e in _voters:
                print(e)

            self._voters = [decrypt_string(e) for e in _voters]
            self._casts = [voters[0] for voters in curs.execute("SELECT studNr FROM voted")]
        
            print(self._voters)
        else:
            #Generate new public private keys
            generate_keys()
        curs.close()

        self.gVoters = loadVoters('voters.csv')
        self.gCandidates = loadCandidates('candidates.csv')

        
    def vote(self, voteId, candId):
        if voteId in self._voters:
            pass

        print(voteId)
        now = datetime.datetime.now()
        if voteId in self.gVoters and candId in self.gCandidates:
            curs, conn = get_cursor()
            eVoteId = encrypt_string(voteId)
            print(eVoteId)
            curs.execute("INSERT INTO voted(studNr) VALUES (?)",(sqlite3.Binary(eVoteId),))
            conn.commit()
            return f'Voter: {voteId} voted {candId} at {now}'

            
            
    def delete(self):
        delete_db()
        remove_keys()
        print("Lists deleted")

    def create(self):
        delete_db()
        remove_keys()
        print("Lists deleted")

    
    def res(self):
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='casts';")
        print()
        pass



            