import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

from abc import ABC, abstractmethod

class transactionLaboratory(ABC):

    def __init__(self) -> None:
        self.start = datetime(2025, 3, 1, 8, 0, 0)  # March 1, 2024, 08:00 AM
        self.min_time_step = 0
        self.max_time_step = 10 #maximum time step in seconds between two transactions

    @abstractmethod
    def generate(self):
        pass

    def random_time_step(self, current_time):
        return current_time + timedelta(seconds=random.randint(self.min_time_step, self.max_time_step))

    def random_account(self, accounts, except_account = None):
        account = random.sample(accounts,1)[0]
        if except_account is not None:
            while account == except_account:  # Avoid self-loops
                account = random.sample(accounts,1)[0]
        return account

    def random_accounts(self, accounts = None, accounts_from = None, accounts_to = None):
        if accounts is not None:
            account_list_from = account_list_to = accounts
        elif accounts_from is not None and accounts_to is not None:
            account_list_from = accounts_from
            account_list_to = accounts_to
        else:
            print("Warning: no account list provided")

        from_node = self.random_account(account_list_from)
        to_node = self.random_account(account_list_to, except_account=from_node)
        
        return from_node, to_node

    def toTable(self, data):
        if isinstance(data, list):
            return pd.DataFrame(data, columns =['source', 'target', 'amount', 'time'])

    def plotTransactionGraph(self, dataframe, edgeLables = False, title = 'Transaction graph'):
        if isinstance(dataframe, pd.DataFrame):
            G = nx.from_pandas_edgelist(dataframe, source='source', target='target', edge_attr=['amount', 'time'],create_using=nx.MultiDiGraph)

        # Plot the graph
        plt.figure(figsize=(10, 6))
        pos = nx.forceatlas2_layout(G, scaling_ratio = 0.50, dissuade_hubs = True, seed = 42)  # Layout for better visualization
        #pos = nx.circular_layout(G) # Layout for better visualization
        edges = G.edges(data=True)
        # Draw nodes and edges
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray', arrows=True)
        if edgeLables:
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"${d['amount']}" for u, v, d in edges}, font_size=8)
        plt.title(title)
        plt.show()
