#0.1.2

import hashlib as hash_
import datetime

global symbol
symbol = "ZBC"

class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        
    def __str__(self):
        string = "from: " + self.fromAddress + "\n"
        string += "to: " + self.toAddress + "\n"
        string += "ZBC: " + str(self.amount) + "\n"
        return string

class Block:
    def __init__(self, timestamp, transactions, previousHash = str(None)):
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculateHash()

    def __str__(self):
        string = "timestamp: " + self.timestamp + "\n"
        string += "transactions: " + str(self.transactions) + "\n"
        string += "previousHash: " + self.previousHash + "\n"
        string += "hash: " + self.hash + "\n"
        return string

    def calculateHash(self):
        return hash_.sha256((self.previousHash + self.timestamp + str(self.transactions) + str(self.nonce)).encode()).hexdigest()

    def mineBlock(self, difficulty):
        while self.hash[0:difficulty] != "0"*difficulty:
            self.nonce += 1
            self.hash = self.calculateHash()

        print("BLOCK MINED:", self.hash)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.pendingTransactions = []
        self.miningReward = 100

        self.chain.append(self.createGenesisBlock())

    def __str__(self):
        string = "chain \n=====\n"
        for block in self.chain:
            string += str(block) + "-----\n"
        return string

    def createGenesisBlock(self):
        return Block("04/03/2018", [Transaction("genesis", "block", "0")], "*genesis block*")

    def getLatestBlock(self):
        return self.chain[-1]

    def minePendingTransactions(self, miningRewardAddress):
        block = Block(dateNow(), self.pendingTransactions, self.getLatestBlock().hash)
        block.mineBlock(self.difficulty)

        print("Block successfully mined!")
        self.chain.append(block)

        self.pendingTransactions = [Transaction(None, miningRewardAddress, self.miningReward)]

    def createTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            #print(block)
            for trans in block.transactions:
                #print("Trans: ", trans)
                if trans.fromAddress == address:
                    balance -= trans.amount

                if trans.toAddress == address:
                    balance += trans.amount

        return balance

    def isChainValid(self):
        for i in range(1, len(self.chain)+ 1):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]

            if currentBlock.hash != currentBlock.calculateHash():
                return False

            if currentBlock.previousHash != previousBlock.hash:
                return False

        return True

def dateNow(UK = True): #defaults to UK date format, for US date format pass through False.
    d = datetime.datetime.now()
    if UK:
        dString = str(d.day)+"/"+str(d.month)+"/"+str(d.year)
    else:
        dString = str(d.month)+"/"+str(d.day)+"/"+str(d.year)
    return dString

ZackCoin = Blockchain()

ZackCoin.createTransaction(Transaction("address1", "address2", 100))
ZackCoin.createTransaction(Transaction("address2", "address1", 50))

print("\nStarting the miner...")
ZackCoin.minePendingTransactions("xaviers-address")

print("\nBalance of xavier is", symbol, ZackCoin.getBalanceOfAddress("xaviers-address"))

print("\nStarting the miner again...")
ZackCoin.minePendingTransactions("xaviers-address")

print("\nBalance of xavier is", symbol, ZackCoin.getBalanceOfAddress("xaviers-address"))


        
