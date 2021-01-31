import json
from audit import saveFile, loadCandidates, loadVoters
import datetime
import sqlite3
from dbconnector import create_db, delete_db, get_cursor
from encryption import decrypt_string, encrypt_string, generate_keys, remove_keys


class Vote():

    _voters = []
    _casts = []

    gVoters = []
    gCandidates = []

    def __init__(self):
        # Check state
        curs, __ = get_cursor()
        curs.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='casts';")
        result = curs.fetchone()
        if result:
            _voters = [voters[0]
                       for voters in curs.execute("SELECT studNr FROM voted")]

            self._voters = [decrypt_string(e) for e in _voters]
            self._casts = [voters[0]
                           for voters in curs.execute("SELECT mdwID FROM casts")]
        curs.close()

        self.gVoters = loadVoters('voters.csv')
        self.gCandidates = loadCandidates('candidates.csv')

    def vote(self, voteId, candId):
        curs, conn = get_cursor()
        curs.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='casts';")
        result = curs.fetchone()
        if not result:
            create_db()
            generate_keys()

        if voteId in self._voters:
            curs, __ = get_cursor()
            v = curs.execute("SELECT COUNT(studNr) FROM voted;")
            c = curs.execute("SELECT COUNT(mdwId) FROM casts;")
            if c == v:
                print("Votes are counted correctly.")
            else:
                print(
                    "The votes have not been stored correctly or have been manipulated.")
            exit()

        now = datetime.datetime.now()
        if voteId in self.gVoters and candId in self.gCandidates:
            eVoteId = encrypt_string(voteId)
            curs.execute("INSERT INTO voted(studNr) VALUES (?)",
                         (sqlite3.Binary(eVoteId),))
            curs.execute("INSERT INTO casts(mdwID) VALUES (?)", (candId,))
            conn.commit()
            return encrypt_string(f'Voter: {voteId} voted {candId} at {now}')

    def delete(self):
        delete_db()
        remove_keys()
        print("Lists deleted")

    def create(self):
        delete_db()
        remove_keys()
        print("Lists deleted")

    def stats(self):
        return {
            'candidates': len(self.gCandidates),
            'registrated': len(self.gVoters),
            'voters': len(self._voters),
            'casts': len(self._casts),
            'turn-out': '{:.2f}%'.format((len(self._voters)/len(self.gVoters)*100))
        }

    def audit(self):
        saveFile('audit_cand.json', json.dumps(self._casts))
        saveFile('audit_vote.json', json.dumps(self._voters))
