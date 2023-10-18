import pandas as pd

class TransactionSet():
    """
    Universal representation of a transaction set
    """
    def __init__(self, **kwargs):

        """
        Creates the itemset based on a provided source and
        input arguments
        """
        self.transactions = []

        source = kwargs.get("source")
        assert(
            source is not None
        ), "transaction set source cannot be None"


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