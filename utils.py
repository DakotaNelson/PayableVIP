import requests
from requests.auth import HTTPBasicAuth

from datetime import date

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
