import json
from web3 import Web3
from .models import History

# initialize contract instance and variables

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
file = json.load(open('truffle/build/contracts/MyToken.json'))
abi = file['abi']
contractAddress = file['networks']['5777']['address']
contract = web3.eth.contract(address=contractAddress, abi=abi)
contractCreator = web3.eth.coinbase
privateKey = "a5674cc84bcfb4ea25216707e968aee4be658bbd587c892e3576b7379d98417d"

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

# function which create a local account with address and
# privatekey storing them in a model continuing in the view function


def getBalance(address):

    try:
        balance = contract.functions.balanceOf(address).call()
        return balance
    except Exception:
        balance = "Incorrect Address!"
        return balance


def totalSupply():

    supply = contract.functions.balanceOf(contractCreator).call()
    return supply
