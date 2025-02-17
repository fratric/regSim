import networkx as nx
import random
from datetime import datetime, timedelta

class transactionLaboratory():

  def __init__(self, N = 100) -> None:
    self.N = N # Number of entities

  def getRandomAmount(self):
    return round(random.uniform(10, 500), 2)  # Random transaction amount

  def random_datetime(self, start, end):
      delta = end - start
      random_seconds = random.randint(0, int(delta.total_seconds()))
      return start + timedelta(seconds=random_seconds)

  def generate_transactions(self, start, end):
    # Create a directed graph
    G = nx.DiGraph()
    # Add nodes (entities)
    G.add_nodes_from(range(self.N))
    # Randomly add directed edges (transactions) between entities
    num_edges = random.randint(self.N, self.N * 2)  # Ensure at least N edges, but no more than N*2
    for _ in range(num_edges):
        from_node = random.randint(0, self.N-1)
        to_node = random.randint(0, self.N-1)
        while to_node == from_node:  # Avoid self-loops
            to_node = random.randint(0, self.N-1)
        amount = self.getRandomAmount()
        transaction_time = self.random_datetime(start, end)
        G.add_edge(from_node, to_node, weight=amount, time=transaction_time)
    return G

  def generate_transactions_in_time(self, start_date, end_date, step):
    current_date = start_date
    transaction_graphs = []
    while current_date <= end_date:
        transaction_graphs.append(self.generate_transactions(current_date, current_date + step))
        current_date += step
    return transaction_graphs

  def plotTransactionGraph(self, G):
    # Plot the graph
    plt.figure(figsize=(10, 6))
    pos = nx.forceatlas2_layout(G, scaling_ratio = 0.50, dissuade_hubs = True, seed = 42)  # Layout for better visualization
    #pos = nx.circular_layout(G) # Layout for better visualization
    edges = G.edges(data=True)
    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"${d['weight']}" for u, v, d in edges}, font_size=8)
    plt.title("Transaction Graph Between" + str(self.N)  + "Entities")
    plt.show()

  #formats a transaction graph (or a sequence of graphs) into a table
  def toTable(self, arg):
    if isinstance(arg, nx.DiGraph):
      arg = [arg]
    dfs = []
    for G in arg:
      dfs.append(nx.to_pandas_edgelist(G))
    return pd.concat(dfs)
