import json
from web3 import Web3
from eth_account import Account
from .models import History

# variables to initiate transactions and connect to the contract (deployed with Remix, verified and published on the Ropsten)


web3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/cb3427bf216548ba96157079ddac0427"))
contractCreator = '0x960562B0220Aa6058fDfd8eCd135843c6704cc5f'
abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"tokenOwner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"internalType":"uint256","name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
contractAddress = '0x550Bc921abB8260259e713758B2aBE869de47799'
contract = web3.eth.contract(address=contractAddress, abi=abi)

# function which send the amount of ether of the purchase to the contract creator and tokens to the buyer


def buyToken(key, amount, address, value):

    try:
        signedTx1 = web3.eth.account.signTransaction(dict(
            nonce=web3.eth.getTransactionCount(address),
            to=contractCreator,
            gas=100000,
            gasPrice=web3.eth.gasPrice,
            value=web3.toWei(value, 'ether'),
        ), key)
        tx1 = web3.eth.sendRawTransaction(signedTx1.rawTransaction)
        txId1 = web3.toHex(tx1)
        web3.eth.waitForTransactionReceipt(txId)
        print(f"Transaction Success! {txId1}")
        transaction = contract.functions.transfer(address, amount).buildTransaction({
            'from': contractCreator,
            'gas': 1000000,
            'gasPrice': web3.eth.gasPrice,
            'nonce': web3.eth.getTransactionCount(contractCreator),
        })
        print(f"Transaction Created : {transaction}")
        signedTx2 = web3.eth.account.signTransaction(transaction, private_key='4efba20643c86137c0d4f703342c451076c84e539af9b6cd5d367d7c3a3af3dc')
        tx2 = web3.eth.sendRawTransaction(signedTx2.rawTransaction)
        txId2 = web3.toHex(tx2)
        web3.eth.waitForTransactionReceipt(txId2)
        print(f"Transaction Success! {txId2}")
        History.objects.create(paymentTx=txId1, contractTx=txId2)
        result = "Transaction Success!"
        return result
    except ValueError:
        valueError = "Something went wrong, are you sure you have enough Ether in the wallet?"
        return valueError

# function which create a local account with address and privatekey storing them in a model continuing in the view function


def newAccount():

    account = Account.create()
    return account


def getBalanceEther(address):

    balance = float(web3.fromWei(web3.eth.getBalance(address), 'ether'))
    return balance


def getBalanceToken(address):

    balance = contract.functions.balanceOf(address).call()
    return balance


def totalSupply():
    supply = contract.functions.balanceOf(contractCreator).call()
    return supply
