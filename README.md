# stem_app
Contributers:
- Erencan Kanmaz    500750496
- Axel Valent       500757310   

Dependencies:
>> pip -r requirements.txt

# Usage
Start new voting session:
>> python main.py --new

Register vote:
>> python main.py --vote -p [voter] -c [candidate]

Show statistics:
>> python main.py --stat

Export current votes with trustworthy signature:
>> python main.py --res

Delete current voting session:
>> python main.py --delete

List of commands:
>> python main.py -h