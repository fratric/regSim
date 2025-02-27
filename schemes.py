from transaction_laboratory import transactionLaboratory
from datetime import datetime, timedelta
import random
from itertools import cycle
import numpy as np

class random_behavior(transactionLaboratory):
    
    def __init__(self, accounts) -> None:
        super().__init__()
        self.accounts = accounts
        self.behavior_name = 'random'

    def random_amount(self):
        #return round(random.uniform(min_amount, max_amount), 2)
        return round(np.random.exponential(scale=3000))

    def random_datetime(self, start, end):
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

    def generate(self, k):
        transactions = []
        transaction_time = self.start
        for _ in range(k):
            from_node, to_node = self.random_accounts(accounts=self.accounts)
            amount = self.random_amount()
            transaction_time = self.random_time_step(transaction_time)
            transactions.append((from_node, to_node, amount, transaction_time))
        return self.toTable(transactions)

class layering(transactionLaboratory):

    def __init__(self, accounts) -> None:
        super().__init__()
        self.behavior_name = 'layering'
        
        self.source_account = accounts['source_account']
        self.intermediate_accounts = accounts['intermediate_accounts']
        self.target_account = accounts['target_account']
        self.noncompliant_accounts = [self.source_account] + self.intermediate_accounts + [self.target_account]
    
    def generate(self, amount_per_send, capital = 10**6):
        transactions = []
        transaction_time = self.start
        account_cycle = cycle(self.intermediate_accounts)
        remaining_capital = capital
        next_account = next(account_cycle)
        while remaining_capital > 0:
            
            if remaining_capital - amount_per_send > 0:
                remaining_capital = remaining_capital - amount_per_send
            else:
                amount_per_send = remaining_capital
                remaining_capital = 0

            account, next_account = next_account, next(account_cycle)

            transaction_time = self.random_time_step(transaction_time)
            transactions.append((self.source_account, account, amount_per_send, transaction_time))

            transaction_time = self.random_time_step(transaction_time)
            transactions.append((account, self.target_account, amount_per_send, transaction_time))

        
        return self.toTable(transactions)
    
    
class round_tripping(transactionLaboratory):

    def __init__(self, accounts) -> None:
        super().__init__()
        self.behavior_name = 'round_trip'
        
        self.source_accounts = accounts['source_accounts']
        self.intermediate_accounts = accounts['intermediate_accounts']
        self.target_accounts = accounts['target_accounts']
        self.noncompliant_accounts = self.source_accounts + self.intermediate_accounts + self.target_accounts
    
    def random_amount(self, min_amount = 100, max_amount = 20000):
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

    
    def generate(self, max_intermediate_transactions = 12, capital = 10**6):
        transactions = []
        
        remaining_capital = capital
        while remaining_capital > 0:
            amount = self.random_amount()
            if remaining_capital - amount > 0:
                remaining_capital = remaining_capital - amount
            else:
                amount = remaining_capital
                remaining_capital = 0
            
            intermediate_steps = random.randint(1, max_intermediate_transactions)
            transactions = transactions + self.do_round_trip(amount, intermediate_steps)
        
        return self.toTable(transactions)
        
    
class sanctionAvoidance(transactionLaboratory):
    
    def __init__(self, time_switch, amount1 = 100, amount2 = 130):
        super().__init__()
        self.time_switch = time_switch
        self.supplier = 'chip-supplier'
        self.evader = 'Yangjie-Tech'
        #self.target = 'Kalashnikov-Concern'
        
        self.chip_name = 'chip'
        self.sanction_time = time_switch #datetime(2025, 5, 1, 0, 0, 0)
        
        self.std = 5
        self.amount1 = amount1
        self.amount2 = amount2
    
    def random_amount(self, time):
        if time < self.time_switch:
            return round(random.normalvariate(self.amount1, self.std), 0)
        else:
            return round(random.normalvariate(self.amount2, self.std), 0)
    
    def add_months(self, current_date, months_to_add):
        new_date = datetime(current_date.year + (current_date.month + months_to_add - 1) // 12,
                            (current_date.month + months_to_add - 1) % 12 + 1,
                            current_date.day, current_date.hour, current_date.minute, current_date.second)
        return new_date
    
    def generate(self, n_months):
        transactions = []
        transaction_time = self.start
        for k in range(n_months):
            from_node, to_node = self.supplier, self.evader
            transaction_time = self.add_months(self.start, k)
            amount = self.random_amount(transaction_time)
            product_name = self.chip_name
            transactions.append((from_node, to_node, amount, product_name, transaction_time))
        return self.toTable(transactions, columns=['source','target','amount_per_month','product','time'])
    

        
