import json
from web3 import Web3
from .models import History

# variables to initiate transactions and connect to the contract (deployed with Remix, verified and published on the Ropsten)

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
file = json.load(open('brownie/build/contracts/Start2Token.json'))
abi = file['abi']
bytecode = file['bytecode']
greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
Greeter = greeter.constructor().transact({'from': web3.eth.accounts[0]})
tx = web3.eth.waitForTransactionReceipt(Greeter)
contractAddress = tx.contractAddress
contract = web3.eth.contract(address=contractAddress, abi=abi)
contractCreator = web3.eth.coinbase

def buyToken(amount, address):

        gas = contract.functions.transfer(address, amount).estimateGas()

        transaction = contract.functions.transfer(address, amount).buildTransaction({
            'gas': gas,
            'gasPrice': web3.eth.gasPrice,
            'nonce': web3.eth.getTransactionCount(contractCreator)
        })
        print(f"Transaction Created : {transaction}")
        signedTx2 = web3.eth.account.signTransaction(transaction, private_key="0x470215d9ba8d605a65fbd7c9a8c56547cdccda812ebeeaf1a3ce0b685a008989")
        tx2 = web3.eth.sendRawTransaction(signedTx2.rawTransaction)
        txId2 = web3.toHex(tx2)
        web3.eth.waitForTransactionReceipt(txId2)
        print(txId2)
        print(f"Transaction Success! {txId2}")
        History.objects.create(contractTx=txId2)
        result = "Transaction Success!"
        return result




# function which create a local account with address and privatekey storing them in a model continuing in the view function


def getBalanceEther(address):

    balance = float(web3.fromWei(web3.eth.getBalance(address), 'ether'))
    return balance


def getBalanceToken(address):

    balance = contract.functions.balanceOf(address).call()
    return balance


def totalSupply():
    supply = contract.functions.balanceOf(web3.eth.accounts[0]).call()
    return supply

def getEther(address, value):

    transaction = web3.eth.account.signTransaction(dict(
        nonce = web3.eth.getTransactionCount(contractCreator),
        to = address,
        gas = 100000,
        gasPrice = web3.eth.gasPrice,
        value = web3.toWei(value, 'ether')
    ), "0x470215d9ba8d605a65fbd7c9a8c56547cdccda812ebeeaf1a3ce0b685a008989")
    print(f"Transaction Created : {transaction}")
    tx2 = web3.eth.sendRawTransaction(transaction.rawTransaction)
    txId2 = web3.toHex(tx2)
    web3.eth.waitForTransactionReceipt(txId2)
    print(txId2)
    print(f"Transaction Success! {txId2}")