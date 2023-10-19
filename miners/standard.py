from typing import List
from itertools import combinations
import math

from core.transactions import TransactionSet
from core.itemsets import ItemSet

class AprioriMiner():
    """
    Apriori pattern mining for non-sequential frequent patterns
    """
    def __init__(self, transactions: TransactionSet | None = None, relative_support: float | None = None, absolute_support: int | None = None):

        # assertion statements that validate the following:
        # 
        # 1) only one of relative_support and absolute_support are given in the initialization
        # 
        # 2) if absolute_support is provided, transactions must also be provided at initialization,
        #    and the value of absolute_support must be less or equal to the number of transactions
        #    in the transaction set
        #
        # 3) if relative support is provided, its value must be greater than zero and <= 1

        # 1) assert that only one of absolute support and relative support are provided
        assert(
            absolute_support ^ relative_support
        ), "Either `absolute_support` or `relative_support` must be provided for initialization of AprioriMiner"

        if absolute_support:
            # 2) if absolute support is provided, list of transactions must also be provided,
            # and value of absolute support cannot exceed the number of transactions
            assert(
                transactions
            ), "`transactions` must be provided if `absolute_support` is provided"

            assert(
                absolute_support > 0 and absolute_support <= len(transactions)
            ), "`absolute_support` must be greater than zero and cannot exceed the number of transactions"

            self.transactions = transactions
            self.absolute_support = absolute_support
            self.relative_support = self.absolute_support / len(self.transactions)

        if relative_support:

            # 3) if relative support is provided, its value must be greater than zero and <= 1
            assert(
                relative_support > 0 and relative_support <= 1
            ), "`relative_support` must be greater than zero and cannot exceed 1"

            self.relative_support = relative_support

            # if a relative support is provided, then the set of transactions doesn't need to
            # be set immediately. it does, however, need to be set before any mining processes
            # can occur
            if not transactions:
                
                print("Parameter `transactions` was not set during initialization of miner")
                print("In order to mine patterns, you will need to set the `AprioriMiner.transactions` variable by calling the `set_transactions` function")
                self.transactions = None
                self.absolute_support = None

        self.frequent_patterns = {}

    def set_transactions(self, transactions: TransactionSet):
        """
        Method to set a given TransactionSet `transactions` to
        the AprioriMiner object
        """
        self.transactions = transactions

    