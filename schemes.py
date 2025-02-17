class layering(transactionLaboratory):
  def __init__(self, N, source_accounts, intermediate_accounts, target_accounts, capital = 10**6) -> None:
     super().__init__(N)
     self.capital = capital
     self.source_accounts = source_accounts
     self.intermediate_accounts = intermediate_accounts
     self.target_accounts = target_accounts

  def perform_fraud(self, start_date, end_date, step, camouflage = False):
    G = nx.DiGraph()
    fraudListG = []


    return fraudListG
