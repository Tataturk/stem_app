#TODO
# Registratie. 
# Dubbel stemmen voorkomen. List van stemmers die hebben gestemd.

#TODO
# Anonimiteit
# Elk persoon anoniem stemmen. Niet terug kunnen koppelen.

#TODO
# Geheimhouding.
# Opgeslagen data is beveiligd.

#TODO
# Bewijsbaarheid
# Betrouwbare gegevens een hertelling

#TODO
# Realisatie
# Werkend product opleveren

#TODO
# Format stemmen:
# stem -p -k
# -p: persoon
# -k: keuze
#
# --new: start met stemmen.
# --res: display tussenresultaten
# --del: verwijder alle informatie

#TODO
# Database
# Setup a database and connector. Class for easy access?
from encryption import decrypt_string
import getopt
import sys
from vote import Vote
import sqlite3


if __name__ == '__main__':
    cmd = ''
    opts, args = getopt.getopt(sys.argv[1:], 'hp:c:', [ 'create', 'vote', 'res', 'stat', 'delete' ])
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: vote --create')
            print('\tInitialize vote system')
            print('Usage: vote --vote -p <persId> -c <candId>')
            print('\tCast vote')
            print('Usage: vote --res')
            print('\tShow results')
            print('Usage: vote --stat')
            print('\tShow statistics')
            print('Usage: vote --delete')
            print('\tDelete all information (securily)')
            sys.exit()
        if opt == '-D': gDbg = True

        if opt == '-p': persId = arg
        if opt == '-c': candId = arg
        if opt[0:2] == '--': cmd = opt[2:]

    voting = Vote()
    if cmd == 'create':
        voting.create()
        print('bro this shit aint working yet. please wait....')
    if cmd == 'vote':
        try:
            receipt = voting.vote(persId,candId)
            print(decrypt_string(receipt))
            #print(f'{persId} wait for voting on {candId}')
        except NameError:
            print("Missing arguments.")
    if cmd == 'res':
        voting.audit()
    if cmd == 'stat':
        print(voting.stats())
    if cmd == 'delete':
        voting.delete()
            