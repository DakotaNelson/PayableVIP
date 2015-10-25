from parse_rest.connection import register as parse_register
from parse_rest.user import User
import random
import datetime
import sys

from objects import Bills

PARSE_APP_ID = ''
PARSE_API_KEY = ''
PARSE_MASTER_KEY = ''

parse_register(PARSE_APP_ID,
               PARSE_API_KEY,
               master_key=PARSE_MASTER_KEY)

u = User.login("arjun", "password")

for i in range(int(sys.argv[1])):
    cost = random.randrange(100, 50000)/100.0
    user = random.choice(['dakota', 'arjun'])
    type = random.choice(['gas', 'electric', 'water'])

    dueDay = random.randint(1,20)
    dueMonth = random.randint(1,12)
    dueDate = datetime.datetime(2015, dueMonth, dueDay)

    b = Bills(due=dueDate, type=type, cost=cost, username=user)
    b.save()
