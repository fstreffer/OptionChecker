from ib_insync import *

def restructurePositions(accounts, positions):
    for position in positions:
        if position.account in accounts.keys():
            if type(position.contract).__name__ in accounts[position.account].keys():
                accounts[position.account][type(position.contract).__name__].append(position)
            else:
                accounts[position.account][type(position.contract).__name__] = [position]
        else:
            accounts[position.account] = {type(position.contract).__name__ : [position]}
            
def getAllOpenTrades():    
    ib.client.reqAllOpenOrders()  # issue reqAllOpenOrders() directly to IB API, this is a non blocking call
    ib.reqOpenOrders()    # blocking until openOrderEnd messages (may receive two, ib_insync seems not to care
    return ib.openTrades()  # the orders received from issuing reqAllOpenOrders() are correctly captured


def printAccounts(accounts):
    for acc, val in accounts.items():
        print(f'Account: {acc} :')
        for posType, values in val.items():
            print(f'  type {posType}')
            print(*values, sep = "\n")

def printTrades(trades):
    for order in trades:
        print(order)
        
def checkTrades(accounts, trades):
    for account in accounts.keys():
        print(f'Account: {account} :')
        for option in accounts[account]['Option']:
            tradeFound=False
            hasError=False
            for trade in trades:
                if trade.contract == option.contract and trade.order.account == option.account:
                    tradeFound=True
                    if trade.order.action != 'BUY':
                        print('trade is not BUY')
                        hasError=True
                    if trade.order.totalQuantity != -option.position:
                        print('wrong quantity')
                        hasError=True
            if not tradeFound:           
                print('no order found')
                hasError=True
            if hasError:
                print(option)    
    
ib = IB()
ib.connect(host='127.0.0.1', port=7497, clientId=10)

ib_accounts = {}   
ib_positions = ib.positions()

restructurePositions(ib_accounts, ib_positions)

ib_trades = getAllOpenTrades()
checkTrades(ib_accounts, ib_trades)

#printAccounts(ib_accounts)
#printTrades(ib_trades)
        
ib.disconnect()