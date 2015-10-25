# Reads the electricbill dataset, generates data based off of it, uploads
# that data to parse.com

from parse_rest.connection import register as parse_register
from parse_rest.user import User
import random
import datetime
import sys
import csv
import calendar
from time import sleep

from config import *
from objects import Bills

data = []

with open('electricbill.dat.txt') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        data.append([e for e in row if e != ''])

parse_register(PARSE_APP_ID,
               PARSE_API_KEY,
               master_key=PARSE_MASTER_KEY)

u = User.login("arjun", "password")

user = 'arjun'

toMonthNumber = {v: k for k,v in enumerate(calendar.month_abbr)}

for row in data:
    cost = row[3]
    year = row[1]
    month = row[2]

    dueDate = datetime.datetime(int(year), int(toMonthNumber[month]), 20)

    # electric bill
    b = Bills(due=dueDate, type='electric', cost=float(cost), username=user)
    b.save()
    print([dueDate, 'electric', cost, user])

    # water bill
    waterCost = random.gauss(50, 8)
    wb = Bills(due=dueDate, type='water', cost=waterCost, username=user)
    wb.save()
    print([dueDate, 'water', waterCost, user])

    # gas bill
    gasCost = float(random.gauss(1, .1)) * float(cost)
    gb = Bills(due=dueDate, type='gas', cost=gasCost, username=user)
    gb.save()
    print([dueDate, 'gas', gasCost, user])

    sleep(.5)
