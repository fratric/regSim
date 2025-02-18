from transaction_laboratory import transactionLaboratory
from datetime import datetime, timedelta
import random


class random_behavior(transactionLaboratory):
    
    def __init__(self, N = 100) -> None:
        super().__init__()
        self.behavior_name = 'random'
        self.N = N # Number of entities
        self.compliant_accounts = ['C' + str(i) for i in range(N)]

    def random_amount(self, min_amount = 10, max_amount = 500):
        return round(random.uniform(min_amount, max_amount), 2)

    def random_datetime(self, start, end):
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

    def generate(self, k):
        transactions = []
        transaction_time = self.start
        for _ in range(k):
            from_node, to_node = self.random_accounts(accounts=self.compliant_accounts)
            amount = self.random_amount()
            transaction_time = self.random_time_step(transaction_time)
            transactions.append((from_node, to_node, amount, transaction_time))
        return self.toTable(transactions)

class layering(transactionLaboratory):

    def __init__(self, start, min_time_step = 0,  max_time_step = 10, source_accounts = 2, intermediate_accounts = 5, target_accounts = 1, capital = 10**6) -> None:
        super().__init__(start, min_time_step, max_time_step)
        self.capital = capital
        
        self.source_accounts = ['S' + str(i) for i in range(source_accounts)]
        self.intermediate_accounts = ['I' + str(i) for i in range(intermediate_accounts)]
        self.target_accounts = ['T' + str(i) for i in range(target_accounts)]
        self.noncompliant_accounts = self.source_accounts + self.intermediate_accounts + self.target_accounts
        self.start = start
        self.end = end
    
    
class round_tripping(transactionLaboratory):

    def __init__(self, source_accounts = 10, intermediate_accounts = 25, target_accounts = 4, capital = 10**6) -> None:
        super().__init__()
        self.behavior_name = 'round_trip'
        self.capital = capital
        
        self.source_accounts = ['S' + str(i) for i in range(source_accounts)]
        self.intermediate_accounts = ['I' + str(i) for i in range(intermediate_accounts)]
        self.target_accounts = ['T' + str(i) for i in range(target_accounts)]
        self.noncompliant_accounts = self.source_accounts + self.intermediate_accounts + self.target_accounts
    
    def random_amount(self, min_amount = 100, max_amount = 200000):
        return round(random.uniform(min_amount, max_amount), 2)

    def do_round_trip(self, amount, intermediate_steps):
        transactions = []
        transaction_time = self.random_time_step(self.start)

        #generate a transaction between source and intermediate
        from_node, to_node = self.random_accounts(accounts_from = self.source_accounts, accounts_to = self.intermediate_accounts)
        transactions.append((from_node, to_node, amount, transaction_time))
        
        #generate transaction between intermediate accounts
        for i in range(intermediate_steps):
            transaction_time = self.random_time_step(transaction_time)
            from_node = to_node
            to_node = self.random_account(self.intermediate_accounts, except_account=from_node)
            transactions.append((from_node, to_node, amount, transaction_time))
        
        #generate a transaction between intermediate and target
        from_node = to_node
        to_node = self.random_account(self.target_accounts, except_account=from_node)
        transaction_time = self.random_time_step(transaction_time)
        transactions.append((from_node, to_node, amount, transaction_time))
        
        return transactions

    
    def generate(self, max_intermediate_transactions = 12):
        transactions = []
        
        remaining_capital = self.capital
        while remaining_capital > 0:
            amount = self.random_amount(max_amount = remaining_capital)
            if remaining_capital - amount > 0:
                remaining_capital = remaining_capital - amount
            else:
                amount = remaining_capital
                remaining_capital = 0
            
            intermediate_steps = random.randint(1, max_intermediate_transactions)
            transactions = transactions + self.do_round_trip(amount, intermediate_steps)
        
        return self.toTable(transactions)
        
        