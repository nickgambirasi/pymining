import pandas as pd
import os

class TransactionSet():
    """
    Representation of a set of transactions from multiple sources
    """
    def __init__(self, set_name: str | None = None, get_transactions_on_init: bool=False, **kwargs):

        """
        Creates the itemset based on a provided source and
        input arguments. If the `get_transactions_on_init`
        argument is passed, we initialize the argument and
        call the `get_transactions(...)` method to load the
        transaction set based on the keyword arguments pro-
        vided
        """
        assert(
            set_name
        ), "name for the transaction set must be provided"

        self.set_name = set_name
        self.transactions = []

        # if the transactions are available for import when
        # the TransactionSet is initialized, this flag must
        # be passed and the required arguments, including
        # the transaction data
        if get_transactions_on_init:

            transactions_source = kwargs.pop("source", None)
            
            # check that transactions source is collected,
            # otherwise error
            assert(
                transactions_source
            ), "`get_transactions_on_init` was set to True, but 'source' was not provided"

            self.get_transactions(source=transactions_source, kwargs=kwargs)


    def _from_txt(self, filepath, sep):
        """
        Builds an transaction set from a textfile at location `filepath`
        with separator `sep`
        """
        with open(filepath, 'r') as f:

            # iterate through the lines of the file
            # and add transactions
            for line in f.readlines():

                # strip the line, split on the sep,
                # and append the list of items in
                # the transaction
                l = line.strip().split(sep)
                self.transactions.append(l)

        f.close()

    def _from_pandas(self, frame: pd.DataFrame, cell: str = "item"):
        """
        Builds a transaction set from a pandas dataframe `frame`
        by treating each cell as a transaction `cell='transaction'`,
        or as an item `cell='item'`
        """
        assert(
            cell in {"transaction", "item"}
        ), "`cell` parameter must be set to either `transaction` or `item`"

        assert(
            frame
        ), "Dataframe cannot be empty"

        match cell:

            case "item":

                # here each row corresponds to a list of items in one transaction,
                # so we apply the to_list function to each row
                frame.apply(lambda x: self.transactions.append(x.to_list()), axis=1)

            case "transaction":

                # here each cell corresponds to a full transaction, so we apply the to_list
                # function to each element
                frame.map(lambda x: self.transactions.append([item for item in x]))
                # this needs to be rigorously tested

            case _:

                raise AssertionError("`cell` must be either `item` or `transaction`")
            
    def _from_csv(self, filepath):
        """
        Builds transaction set from a comma-separated-value
        file (implements `TransactionSet.from_txt`)
        """
        self._from_txt(filepath=filepath, sep=",")
    
    def _from_tsv(self, filepath):
        """
        Builds transaction set from a tab-separated value file
        (implements `TransactionSet.from_txt`)
        """
        self._from_txt(filepath=filepath, sep="\t")

    def _save_transaction_set(self, location: str, format: str):
        """
        Saves the transaction set in the specified format
        """
        # create the directory specified by the user if it
        # doesn't already exist
        if not os.path.exists(location):
            os.mkdir(location)
    
        assert(
            format in {"txt", "csv", "tsv"}
        ), "supported formats are `txt`, `csv`, and `tsv`"

        match format:

            case "txt":
                sep = " "

            case "csv":
                sep = ", "

            case "tsv":
                sep = "\t"

            case _:
                raise AssertionError("Invalid format specified")

        # write the transaction set with the specified format type
        with open(os.path.join(location, f"{self.name}_transactions.{format}"), 'w') as f:
            # iterate through each item in the transactions and append them to a file
            for transaction in self.transactions:
                for item in transaction:
                    f.write(f"{item}{sep}")
                f.write("\n")

    def save(self, location: str, format: str="csv"):
        """
        Accessible method to save the transaction dataset at 
        the specified `location`, with the specified `format`
        """
        self._save_transaction_set(location, format)

    def get_transactions(self, source, **kwargs):
        """
        Method to collect the transactions from the data
        sources
        """
        match source:

            case "dataframe":

                # get the dataframe argument
                frame = kwargs.get("frame", None)
                assert (
                    frame
                ), "`frame` argument cannot be None if trying to build TransactionSet from dataframe"

                # get the cell argument, defaulting to the "item" method
                cell = kwargs.get("cell", "item")

                # collect the transactions and return them to the TransactionSet item
                self._from_pandas(frame=frame, cell=cell)

            case "txt":

                # get the file_path argument
                file_path = kwargs.get("file_path", None)

                assert(
                    file_path
                ), "`file_path` cannot be when trying to read from a .txt file"

                assert(
                    file_path.endswith(".txt")
                ), "`file_path` must end in .txt when trying to build a TransactionSet from .txt file"

                # get the separator argument, defaulting to a space between items
                # in the file
                sep = kwargs.get("sep", " ")

                self._from_txt(file_path, sep)

            case "csv":

                # get the filename argument
                file_path = kwargs.get("file_path", None)

                assert(
                    file_path
                ), "`file_path` cannot be None when trying to build a TransactionSet from a .csv file"

                assert(
                    file_path.endswith(".csv")
                ), "file_path must end with .csv when trying to build a TransactionSet from .csv file"

                self._from_csv(filepath=file_path)

            case "tsv":

                # get the filename argument
                file_path = kwargs.get("file_path", None)

                assert(
                    file_path
                ), "`file_path` cannot be None when trying to build a TransactionSet from a .tsv file"

                assert(
                    file_path.endswith(".tsv")
                ), "`file_path` must end with .tsv when trying to build a TransactionSet from a .tsv file"

                self._from_tsv(filepath=file_path)

            case _:

                raise AssertionError("`source` must be one of ['dataframe', 'txt', 'csv', 'tsv']")
    
    def __len__(self):

        return len(self.transactions)

    def __str__(self):

        return f"Transaction set\nNum Transactions: {len(self)}\n"