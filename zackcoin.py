#0.2.0

import hashlib as hash_
import datetime

class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self._fromAddress = fromAddress
        self._toAddress = toAddress
        self._amount = amount
        
    def __str__(self):
        string = "from: " + self._fromAddress + "\n"
        string += "to: " + self._toAddress + "\n"
        string += "ZBC: " + str(self._amount) + "\n"
        return string

class Block:
    def __init__(self, timestamp, transactions, previousHash = str(None)):
        self._previousHash = previousHash
        self.__timestamp = timestamp
        self._transactions = transactions
        self.__nonce = 0
        self._hash = self.calculateHash()

    def __str__(self):
        string = "timestamp: " + self.__timestamp + "\n"
        string += "transactions: " + str(self._transactions) + "\n"
        string += "previousHash: " + self._previousHash + "\n"
        string += "hash: " + self._hash + "\n"
        return string

    def calculateHash(self):
        return hash_.sha256((self._previousHash + self.__timestamp + str(self._transactions) + str(self.__nonce)).encode()).hexdigest()

    def mineBlock(self, difficulty):
        while self._hash[0:difficulty] != "0"*difficulty:
            self.__nonce += 1
            self._hash = self.calculateHash()

        print("BLOCK MINED:", self._hash)

class Blockchain:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
        self.__chain = []
        self.__difficulty = 2
        self.__pendingTransactions = []
        self.__miningReward = 100

        self.__chain.append(self.createGenesisBlock())

    def __str__(self):
        string = "chain \n=====\n"
        for block in self.__chain:
            string += str(block) + "-----\n"
        return string

    def createGenesisBlock(self):
        return Block(dateNow(), [Transaction("genesis", "block", "0")], "*genesis block*")

    def getLatestBlock(self):
        return self.__chain[-1]

    def minePendingTransactions(self, miningRewardAddress):
        block = Block(dateNow(), self.__pendingTransactions, self.getLatestBlock()._hash)
        block.mineBlock(self.__difficulty)

        print("Block successfully mined!")
        self.__chain.append(block)

        self.__pendingTransactions = [Transaction(None, miningRewardAddress, self.__miningReward)]

    def createTransaction(self, transaction):
        if transaction._amount > self.getBalanceOfAddress(transaction._fromAddress):
            return "Transaction Failed: Insufficient Funds."
        self.__pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.__chain:
            for trans in block._transactions:
                if trans._fromAddress == address:
                    balance -= trans._amount

                if trans._toAddress == address:
                    balance += trans._amount

        return balance

    def isChainValid(self):
        for i in range(1, len(self.__chain)):
            currentBlock = self.__chain[i]
            previousBlock = self.__chain[i-1]

            if currentBlock._hash != currentBlock.calculateHash():
                return False

            if currentBlock._previousHash != previousBlock._hash:
                return False

        return True

def dateNow(UK = True): #defaults to UK date format, for US date format pass through False.
    d = datetime.datetime.now()
    if UK:
        dString = str(d.day)+"/"+str(d.month)+"/"+str(d.year)
    else:
        dString = str(d.month)+"/"+str(d.day)+"/"+str(d.year)
    return dString

ZackCoin = Blockchain("ZackCoin", "ZBC")

for i in range(10):
    ZackCoin.minePendingTransactions("init-address")

print("\nBalance of initial address is {} {}".format(ZackCoin.getBalanceOfAddress("init-address"), ZackCoin._symbol))

ZackCoin.createTransaction(Transaction("init-address", "shteves-address", 100))

print("\nBalance of Shteve's address is {} {}".format(ZackCoin.getBalanceOfAddress("shteves-address"), ZackCoin._symbol))

ZackCoin.minePendingTransactions("miner-address")

print("\nBalance of Shteve's address is {} {}".format(ZackCoin.getBalanceOfAddress("shteves-address"), ZackCoin._symbol))


        
