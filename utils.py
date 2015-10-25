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

def getMonthlyBillingInfo(username):
    month = date.today().month

    allBills = Bills.Query.filter(username=username)
    monthlyBills = []
    monthlyCost = 0
    utilitySplit = {}
    for bill in allBills:
        m = bill.due.month
        cost = bill.cost
        bType = bill.type
        if month == m:
            monthlyBills.append(bill)
            monthlyCost += cost
            if bType in utilitySplit:
                utilitySplit[bType] += cost
            else:
                utilitySplit[bType] = cost

    monthlyBreakdown = {}
    monthlyBreakdown["bills"] = monthlyBills
    monthlyBreakdown["cost"] = monthlyCost
    monthlyBreakdown["split"] = utilitySplit

    return monthlyBreakdown


def billPay(billid=None):
    u = User.login("arjun", "password")

    if not billid:
        return

    bill = Bills.Query.all(objectId=u.username)
    c = bill.cost

    acc_balance = u.acctBalance
    if acc_balance > c:
        acc_balance = acc_balance - c
        u.acctBalance = acc_balance
        u.save()
        bill.paid = True
        bill.save()


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

def convertIntToMonth(n):
    if n > 12:
        return (n % 13 + 1)
    while n < 1:
        n += 12
    return n
#     if n > 0:
#         return n
#     elif n == 0:
#         return 12
#     else:
#         if int(n/12) < 0:
#             return (n+12)
#         else:
#             multiples = int(n/12)
#             m = multiples * 12
#             r = n-m
#             return (n+m+r)


def breakDownMonthlyCosts(months, period, padding):

#     monthlyBills = []
#     utilitySplit = {}
#     for bill in bills:
#         m = bill.due.month
#         cost = bill.cost
#         bType = bill.type
#         if month == m:
#             monthlyBills.append(bill)
#             if bType in utilitySplit:
#                 utilitySplit[bType] += cost
#             else:
#                 utilitySplit[bType] = cost

    expenseSplit = {}
    for utilitySplit in months:
        for bType in months[utilitySplit]:
            cost = months[utilitySplit][bType]
            if bType in expenseSplit:
                expenseSplit[bType] += cost
            else:
                expenseSplit[bType] = cost

    monthlyCost = 0
    for utility in expenseSplit:
        print "utility"
        total = expenseSplit[utility]
        expenseSplit[utility] = (float(total/period))*padding
        monthlyCost += expenseSplit[utility]

    monthlyBreakdown = {}
    monthlyBreakdown["cost"] = monthlyCost
    monthlyBreakdown["split"] = expenseSplit
    monthlyBreakdown["months"] = months


    return monthlyBreakdown

def getMonthlyRates(username, prior_weight=8, future_weight=3, padding=1.05):
    myBills = monthlyAverage(Bills.Query.filter(username=username))
    predBills = predictBills(future_weight, username)
    month = date.today().month
    found_months = {}

    for m in xrange(1,prior_weight+1):
        prior_month = convertIntToMonth(month-m)
        found_months[prior_month] = myBills[prior_month]

    for m in xrange(1,future_weight+1):
        next_month = convertIntToMonth(month+m)
        found_months[next_month] = predBills[next_month]

    breakdown = breakDownMonthlyCosts(found_months, prior_weight+future_weight, padding)

    return breakdown

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
