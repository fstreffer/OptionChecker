from ib_insync import *

CONTRACTTYPE_OPTION = 'Option'

def restructurePositions(accounts, positions):
    for position in positions:
        if position.account in accounts.keys():
            if type(position.contract).__name__ in accounts[position.account].keys():
                accounts[position.account][type(position.contract).__name__].append(position)
            else:
                accounts[position.account][type(position.contract).__name__] = [position]
        else:
            accounts[position.account] = {type(position.contract).__name__ : [position]}
            
def getAllOpenTrades(ib_local):    
    ib_local.client.reqAllOpenOrders()  # issue reqAllOpenOrders() directly to IB API, this is a non blocking call
    ib_local.reqOpenOrders()    # blocking until openOrderEnd messages (may receive two, ib_insync seems not to care
    return ib_local.openTrades()  # the orders received from issuing reqAllOpenOrders() are correctly captured


def printAccounts(accounts):
    for acc, val in accounts.items():
        print(f'Account: {acc} :')
        for posType, values in val.items():
            print(f'  type {posType}')
            print(*values, sep = "\n")

def printTrades(trades):
    for order in trades:
        print(order)
