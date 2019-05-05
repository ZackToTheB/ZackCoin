import hashlib as hash_
import datetime

class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self._fromAddress = fromAddress
        self._toAddress = toAddress
        self._amount = amount
        
    def __str__(self):
        string = "from: {}\n".format(self._fromAddress)
        string += "to: {}\n".format(self._toAddress)
        string += "amount: {}\n".format(self._amount)
        return string

class Block:
    def __init__(self, timestamp, transactions, previousHash = str(None)):
        self._previousHash = previousHash
        self.__timestamp = timestamp
        self._transactions = transactions
        self.__nonce = 0
        self._hash = self.calculate_hash()

    def __str__(self):
        string = "timestamp: " + self.__timestamp + "\n"
        string += "transactions: " + str(self._transactions) + "\n"
        string += "previousHash: " + self._previousHash + "\n"
        string += "hash: " + self._hash + "\n"
        return string

    def calculate_hash(self):
        return hash_.sha256((self._previousHash + self.__timestamp + str(self._transactions) + str(self.__nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        while self._hash[0:difficulty] != "0"*difficulty:
            self.__nonce += 1
            self._hash = self.calculate_hash()

        print("BLOCK MINED:", self._hash)

class Blockchain:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
        self.__chain = []
        self.__difficulty = 2
        self.__pendingTransactions = []
        self.__miningReward = 100

        self.__chain.append(self._create_genesis_block())

    def __str__(self):
        string = "chain \n=====\n"
        for block in self.__chain:
            string += str(block) + "-----\n"
        return string

    def _create_genesis_block(self):
        return Block(get_date(), [Transaction("genesis", "block", "0")], "*genesis block*")

    def get_latest_block(self):
        return self.__chain[-1]

    def get_chain(self):
        return self.__chain
    
    def mine_pending_transactions(self, miningRewardAddress):
        block = Block(get_date(), self.__pendingTransactions, self.get_latest_block()._hash)
        block.mine_block(self.__difficulty)

        print("Block successfully mined!")
        self.__chain.append(block)

        self.__pendingTransactions = [Transaction(None, miningRewardAddress, self.__miningReward)]

    def create_transaction(self, transaction):
        if transaction._amount > self.get_balance_of_address(transaction._fromAddress):
            return "Transaction Failed: Insufficient Funds."
        self.__pendingTransactions.append(transaction)

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.__chain:
            for trans in block._transactions:
                if trans._fromAddress == address:
                    balance -= trans._amount

                if trans._toAddress == address:
                    balance += trans._amount

        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.__chain)):
            currentBlock = self.__chain[i]
            previousBlock = self.__chain[i-1]

            if currentBlock._hash != currentBlock.calculateHash():
                return False

            if currentBlock._previousHash != previousBlock._hash:
                return False

        return True

def get_date(UK = True): #defaults to UK date format, for US date format pass through False.
    d = datetime.datetime.now()
    if UK:
        dString = str(d.day)+"/"+str(d.month)+"/"+str(d.year)
    else:
        dString = str(d.month)+"/"+str(d.day)+"/"+str(d.year)
    return dString

ZackCoin = Blockchain("ZackCoin", "ZBC")

for i in range(10):
    ZackCoin.mine_pending_transactions("init-address")

print("\nBalance of initial address is {} {}".format(ZackCoin.get_balance_of_address("init-address"), ZackCoin._symbol))

ZackCoin.create_transaction(Transaction("init-address", "shteves-address", 100))

print("\nBalance of Shteve's address is {} {}".format(ZackCoin.get_balance_of_address("shteves-address"), ZackCoin._symbol))

ZackCoin.mine_pending_transactions("miner-address")

print("\nBalance of Shteve's address is {} {}".format(ZackCoin.get_balance_of_address("shteves-address"), ZackCoin._symbol))


        
