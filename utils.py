import requests
from requests.auth import HTTPBasicAuth
from parse_rest.user import User
from datetime import date

from objects import Bills

def achCharge(amount, routingNo, acctNo):
    """
    {
    "InvoiceNo":"111020141127",
    "InvoiceNo":"111020141280",
    "RoutingNo":"490000018",
    "AcctNo":"2441234567134567",
    "SequenceNo":"9999",
    "AcctType":"Checking",
    "ACHMethod":"VerificationOnly",
    "OperatorID":"TEST",
    "Purchase":"1.50",
    }

    curl -k -v -X POST -H "Content-Type:application/json" -H "Authorization: Basic NjAxMzUyMTExNDp4eXo=" -d "@ach.txt" -o output.txt https://w1.mercurycert.net/paymentsapi/ACH/Authorize

    """

    params = {
        "InvoiceNo":"111020141127",
        "InvoiceNo":"111020141280",
        "RoutingNo": str(routingNo),
        "AcctNo": str(acctNo),
        "SequenceNo":"9999",
        "AcctType":"Checking",
        "ACHMethod":"VerificationOnly",
        "OperatorID":"TEST",
        "Purchase": "{0:.2f}".format(amount)
    }

    r = requests.post('https://w1.mercurycert.net/paymentsapi/ACH/Authorize',
                      json = params,
                      timeout = 10,
                      auth = HTTPBasicAuth('6013521114','xyz'))

    return r.json()

def dueDate():
    d = date.today()
    d.replace(day=20)
    return d

def billPay():
    u = User.login("arjun", "password")
    
    bills = Bills.Query.all(username=u.username)
    
    
def monthlyAverage(data = None):
    if data is None:
        data = Bills.Query.all()

    utilities = []
    # get all the unique utilities types
    for datum in data:
        if datum.type not in utilities:
            utilities.append(datum.type)

    ret = {month:{} for month in range(1,13)}
    for utility in utilities:
        for month in range(1,13):
            # [d['Water'] for d in data if d['Month'] == 'Jan']
            vals = [d.cost for d in data if d.due.month == month and d.type == utility]
            if len(vals) == 0:
                ret[month][utility] = 0
            else:
                ret[month][utility] = sum(vals) / len(vals)

    return ret

def predictBills(nMonths, username):
    allBills = monthlyAverage()
    myBills = Bills.Query.filter(username=username)
    myBills = monthlyAverage(myBills)

    # all possible utilities
    possibleUtilities = allBills[1].keys()

    """
    utilities = []
    # get all the unique utilities types
    for month in allBills:
        for k in allBills[month].keys():
            if k not in utilities:
                utilities.append(k)

    bills = {month:{} for month in range(1,13)}
    for month in range(1,13):
        for utility in utilities:
            bills[month][utility] = [d.cost for d in myBills if d.due.month == month and d.type == utility]
    print(bills)
    """

    utilities = {utility:1 for utility in possibleUtilities}
    ratios = {month:utilities for month in range(1,13)}
    for month in range(1,13):
        for utility in possibleUtilities:
            try:
                if allBills[month][utility] == 0:
                    ratios[month][utility] = 1
                else:
                    ratios[month][utility] = myBills[month][utility] / allBills[month][utility]
            except KeyError:
                ratios[month][utility] = 1

    # now use the ratios for prediction
    currentMonth = date.today().month
    monthRange = range(currentMonth, currentMonth+nMonths+1)
    for i in range(len(monthRange)):
        if monthRange[i] > 12:
            monthRange[i] = monthRange[i] % 13 + 1

    bills = {month:{} for month in monthRange}
    for month in monthRange:
        for utility in possibleUtilities:
            bills[month][utility] = ratios[month][utility] * allBills[month][utility]

    return bills
