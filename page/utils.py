import json
from web3 import Web3
from .models import History
import datetime

# initialize contract instance and variables


web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
file = json.load(open('truffle/build/contracts/Ico.json'))
abi = file['abi']
contractAddress = file['networks']['5777']['address']
contract = web3.eth.contract(address=contractAddress, abi=abi)
contractCreator = web3.eth.coinbase
privateKey = "Enter the private key of the first ganache account"

# function for faucet functionality of the site


def getEther(address, value):

    try:
        transaction = web3.eth.account.sign_transaction(dict(
            nonce = web3.eth.getTransactionCount(contractCreator),
            to = address,
            gas = 100000,
            gasPrice = web3.eth.gasPrice,
            value = web3.toWei(value, 'ether')
        ), privateKey)
        print(f"Transaction Created : {transaction}")
        tx = web3.eth.sendRawTransaction(transaction.rawTransaction)
        txId = web3.toHex(tx)
        web3.eth.waitForTransactionReceipt(txId)
        print(txId)
        print(f"Transaction Success! {txId}")
        History.objects.create(faucetTx=txId)
        result = "You have received 10 Ether on your account!"
        return result
    except ValueError:
        result = "You have exceded the withdrawals from the faucet!"
        return result

# get token balance of selected address


def getBalance(address):

    try:
        balance = contract.functions.balanceOf(address).call()
        return balance
    except Exception:
        balance = "Incorrect Address!"
        return balance

# get the total supply


def totalSupply():

    supply = contract.functions.balanceOf(contractCreator).call()
    return supply

# get the date when the ico will finish


def endDate():

    end = contract.functions.endDate().call()
    date = datetime.datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')
    return date
