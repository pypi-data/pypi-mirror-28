from cibc import CIBC

c = CIBC('4506445678314160', 'TheRocker99')
c.Accounts()
print(c.accounts)
print(c.CHEQUING_CAD)
print(c.SAVINGS_CAD)
print(c.SAVINGS_USD)
print(c.CREDIT_CARD_CAD)

