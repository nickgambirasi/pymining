from core.transactions import TransactionSet

import os

class ItemSet():

    #####################################
    #      INITIALIZATION METHOD        #
    #####################################
    def __init__(self, name: str | None = None, transactions: TransactionSet | None = None):

        assert(
            name
        ), "itemset must recieve parameter `name` during initialization"
        self.name = name

        # empty dictionaries for converting items to indexes and
        # indexes to items
        self.item2idx = {}
        self.idx2item = {}

        if transactions:
            # get the items from the transaction set
            self.get_dictionaries(transaction_set=transactions)

        else:
            print("Itemset was successfully intialized, but dictionaries weren't created")
            print("Before using this itemset in mining operations, dictionaries need to be collected")
            print("This can be done with the `ItemSet.get_dictionaries(...)` method")

    #####################################
    #          PUBLIC METHODS           #
    #####################################
    def get_dictionaries(self, transaction_set: TransactionSet):

        self._get_item2idx(transaction_set)
        self._get_idx2item(transaction_set)

    def save_itemsets(self, location: str | None = None):

        self._save_itemsets()
    
    def _get_item2idx(self, transaction_set):

        # id idx2item is already available, simply invert
        # it into item2idx
        if self.idx2item:
            self.item2idx = {v: k for k, v in self.idx2item.items()}

        # otherwise, iterate through the transaction set
        # and create item2idx
        else:
            assert(
                transaction_set
            ), "Cannot create `item2idx` dictionary from empty transaction set"
            idx = 0
            for transactions in transaction_set.transactions:
                for item in transactions:
                    if item not in self.item2idx.keys():
                        self.item2idx[item] = idx
                        idx += 1

    def _get_idx2item(self, transaction_set):

        # if item2idx is already full, create idx2item by
        # inverting it
        if self.item2idx:
            self.idx2item = {v: k for k, v in self.item2idx.items()}

        # otherwise, iterate through the transaction set and create
        # the idx2item
        else:
            assert(
                transaction_set
            ), "Cannot create `idx2item` dictionary from empty transaction set"
            idx = 0
            for transactions in transaction_set.transactions:
                for item in transactions:
                    if item not in self.idx2item.values():
                        self.idx2item[idx] = item
                        idx += 1

    def _save_itemsets(self, location):

        if not os.path.exists(location):
            os.mkdir(location)

        assert(
            location
        ), "`location` is required for saving itemset dictionaries"

        assert(
            self.idx2item and self.item2idx
        ), "cannot save empty itemset dictionaries"

        with open(os.path.join(location, f"{self.name}_item2idx.txt"), "w") as f:
            for index, item in self.idx2item.items():
                f.write(f"{index}: {item}\n")

        with open(os.path.join(location, f"{self.name}_idx2item.txt"), "w") as f:
            for index, item in self.item2idx.items():
                f.write(f"{index}: {item}\n")

    def __len__(self):
        """
        Returns the length of the itemset
        """
        return len(self.item2idx) if len(self.item2idx) == len(self.idx2item) else None
    
    def __str__(self):
        """
        Prints information related to the itemsets
        """
        return f"Name: {self.name}\nNumber of Items: {len(self)}"