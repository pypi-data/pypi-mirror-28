import os
import requests
import datetime
import re

# pull data from CIBC API and format it
class Parse():
    def __init__(self,
                 dateFrom = datetime.datetime(2017,12,25),
                 dateUntil = datetime.datetime(2018,4,20),
                 X_Auth_Token=None,
                 cookies=None,
                 file=None):
        global _username
        global _password
        if not _username:
            _username = input("Bank Account Number: ")
        if not _password:
            _password = input("Bank Account Password: ")
        self.dateUntil = dateUntil
        self.dateFrom = dateFrom
        self.transactions = self.aquireTransactions(dateFrom,dateUntil)
        self.tr_clean = self.removeRepeats()

    # get the credits/debits since datefrom until dateuntil.  If X_auth_token and cookies are provided, will not re authenticate
    # but use the existing X auth Token and cookies provided
    def aquireTransactions(self,dateFrom,dateUntil, X_Auth_Token=None, cookies=None):
        if not (X_Auth_Token and cookies):
            authenticate_request = requests.post(
                url="https://www.cibconline.cibc.com/ebm-anp/api/v1/json/sessions",
                json={"card": {"value": "{}".format(_username), "description": "", "encrypted": False, "encrypt": True},
                      "password": "{}".format(_password)},
                headers={
                    "Host": "www.cibconline.cibc.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
                    "Accept": "application/vnd.api+json",
                    "Accept-Language": "en",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": "https://www.cibconline.cibc.com/ebm-resources/public/banking/cibc/client/web/index.html",
                    "Content-Type": "application/vnd.api+json",
                    "Client-Type": "default_web",
                    "X-Auth-Token": "",
                    "brand": "cibc",
                    "WWW-Authenticate": "CardAndPassword",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Length": "112",
                    "Connection": "keep-alive",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache"
                }
            )
            cookies = dict(authenticate_request.cookies)
            self.cookies = cookies
            authenticate_response_headers = authenticate_request.headers
            X_Auth_Token = authenticate_response_headers['X-Auth-Token']
            self.X_Auth_Token = X_Auth_Token
        login_request = requests.get(
            url="https://www.cibconline.cibc.com/ebm-anp/api/v1/profile/json/userPreferences",
            headers={
                "Host": "www.cibconline.cibc.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
                "Accept": "application/vnd.api+json",
                "Accept-Language": "en",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.cibconline.cibc.com/ebm-resources/public/banking/cibc/client/web/index.html",
                "Content-Type": "application/vnd.api+json",
                "Client-Type": "default_web",
                "brand": "cibc",
                "X-Auth-Token": X_Auth_Token,
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
            },
            cookies=cookies
        )
        print(dateFrom.strftime("%Y-%m-%d"),
                dateUntil.strftime("%Y-%m-%d"))
        login_request_response = login_request.json()
        defaultAccountId = login_request_response['userPreferences'][0]['payeePreferences'][0]['defaultAccountId']
        url = "https://www.cibconline.cibc.com/ebm-ai/api/v1/json/transactions?accountId={}&filterBy=range&fromDate={}&lastFilterBy=range&limit=250&lowerLimitAmount=&offset=0&sortAsc=true&sortByField=date&toDate={}&transactionLocation=&transactionType=&upperLimitAmount=".format(
                defaultAccountId,
                dateFrom.strftime("%Y-%m-%d"),
                dateUntil.strftime("%Y-%m-%d")
            )
        chequing_requests = requests.get(
            url="https://www.cibconline.cibc.com/ebm-ai/api/v1/json/transactions?accountId={}&filterBy=range&fromDate={}&lastFilterBy=range&limit=150&lowerLimitAmount=&offset=0&sortAsc=true&sortByField=date&toDate={}&transactionLocation=&transactionType=&upperLimitAmount=".format(
                defaultAccountId,
                dateFrom.strftime("%Y-%m-%d"),
                dateUntil.strftime("%Y-%m-%d")
            ),
            headers={
                "Host": "www.cibconline.cibc.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
                "Accept": "application/vnd.api+json",
                "Accept-Language": "en",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.cibconline.cibc.com/ebm-resources/public/banking/cibc/client/web/index.html",
                "Content-Type": "application/vnd.api+json",
                "Client-Type": "default_web",
                "brand": "cibc",
                "X-Auth-Token": X_Auth_Token,
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
            },
            cookies=cookies
        )
        print(chequing_requests.json())
        try:
            transactions = chequing_requests.json()['transactions']
        except:
            transactions = []

        for transaction in transactions:
            transaction_type = 'Debit' if transaction['debit'] else 'Credit'
            date_datetime = datetime.datetime.strptime(transaction['date'].split('T')[0],"%Y-%m-%d")
            amount = transaction['debit'] if transaction_type == 'Debit' else transaction['credit']
            yield {
                'transaction': transaction_type,  # 'Debit' or 'Credit'
                'date': date_datetime,
                'details': transaction['transactionDescription'],
                'amount': amount,
                'balance': transaction['runningBalance']
            }

    # If an amount if both credited and debited, that amount is removed from our consideration.
    def removeRepeats(self):
        transaction = list(self.transactions)
        Credits = list(filter(lambda x: x['transaction'] == 'Credit',transaction))
        Debits = list(filter(lambda x: x['transaction'] == 'Debit',transaction))
        DebitPool = [ele['amount'] for ele in Debits]
        CreditPool = [ele['amount'] for ele in Credits]
        properDebits = list(filter(lambda x: x['amount'] not in CreditPool,Debits))
        properCredits = list(filter(lambda x: x['amount'] not in DebitPool, Credits))
        return properCredits + properDebits
