from ib_insync import *
import configparser
import Options
        
INI_FILE_NAME = 'OptionOrderChecker.ini'       
IBKR_CONNECTION = 'ibkr connection'
CONNECTION_HOST = 'host'
CONNECTION_PORT = 'port'
CONNECTION_CLIENTID = 'clientID'
      
def checkTrades(accounts, trades):
    output = []
    for account in accounts.keys():
        output.append(f'Account: {account} :')
        for option in accounts[account][Options.CONTRACTTYPE_OPTION]:
            tradeFound=False
            hasError=False
            for trade in trades:
                if trade.contract == option.contract and trade.order.account == option.account:
                    tradeFound=True
                    if trade.order.action != 'BUY':
                        output.append('trade is not BUY')
                        hasError=True
                    if trade.order.totalQuantity != -option.position:
                        output.append('wrong quantity')
                        hasError=True
            if not tradeFound:           
                output.append('no order found')
                hasError=True
            if hasError:
                output.append(option)    
    return output

config = configparser.ConfigParser()
config.read(INI_FILE_NAME) 
     
ib = IB()
ib.connect(host=config[IBKR_CONNECTION][CONNECTION_HOST], port=config[IBKR_CONNECTION][CONNECTION_PORT], clientId=config[IBKR_CONNECTION][CONNECTION_CLIENTID])

ib_accounts = {}   
ib_positions = ib.positions()

Options.restructurePositions(ib_accounts, ib_positions)

ib_trades = Options.getAllOpenTrades(ib)
print(*checkTrades(ib_accounts, ib_trades), sep = "\n") 

#Options.printAccounts(ib_accounts)
#Options.printTrades(ib_trades)
        
ib.disconnect()