from cibc import CIBC

if __name__ == '__main__':
    c = CIBC('4506445678314160', 'TheRocker99')
    print(c.Accounts())
    for account in c.accounts:
        print(account.information)
        transactions = account.aquireTransactions(dateFrom=datetime.datetime(year=2016, month=1,day=1),
                                                  dateUntil= datetime.datetime(year=2016, month=4, day=30))
        print(transactions)
        account.tocsv(filename='{}.csv'.format(str(account)))