from flask import Flask, render_template, request
from parse_rest.connection import register
import json

from utils import achCharge

app = Flask(__name__)
app.config.from_object('config')

# register for parse.com
register(app.config['PARSE_APP_ID'],
         app.config['PARSE_API_KEY'],
         master_key=app.config['PARSE_MASTER_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    customers = [{"fname":"Bob"}, {"fname":"Joe"}]
    return render_template('dashboard.html', inStore=customers)

@app.route('/api/add-account', methods=['POST'])
def addAccount():
    req = request.get_json()

    if req is None:
        return json.dumps({"status": "fail",
                "reason": "Must include JSON."})

    if not 'username' in req:
        return json.dumps({"status": "fail",
                "reason": "Must include username."})

    if not 'routingNo' in req or not 'acctNo' in req:
        return json.dumps({"status": "fail",
                "reason": "Must include routing and account number."})

    # validate the account with a $1 charge
    res = achCharge(1, req['routingNo'], req['acctNo'])

    if res['CmdStatus'] != 'Approved':
        return json.dumps({"status": "fail",
                "reason": "Account invalid."})

    """
    {u'Authorize': u'5.00', u'Purchase': u'5.00', u'AcctNo': u'XXXXXXXXXXXXXX67', u'ResponseOrigin': u'Processor', u'CmdStatus': u'Approved', u'AuthCode': u'272-172', u'TranCode': u'Authorize', u'UserTraceData': u'', u'TextResponse': u'Approved', u'InvoiceNo': u'111020141280', u'CardType': u'ACH', u'DSIXReturnCode': u'000000', u'MerchantID': u'6013521114', u'OperatorID': u'TEST'}
    """

    # store the routing and account number in the db
    # make sure to credit the user for the dollar we took earlier

    return json.dumps({"status":"success"})

if __name__ == '__main__':
    app.run()
