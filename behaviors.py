from simulator import Simulator
from datetime import datetime, timedelta
import random
from itertools import cycle
import numpy as np

class random_behavior(Simulator):
    
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

class layering(Simulator):

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
    
    
class round_tripping(Simulator):

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
        

class business_profile(Simulator):
    
    def __init__(self):
        super().__init__()
    
    def generate_per_month(self, month):
        total_units_sold = int(random.gauss(180000, 20000))  # Mean: 180k units, StdDev: 20k
        
        avg_price_per_unit = random.gauss(6.5, 0.5)  # Avg price per unit in $
        total_revenue = total_units_sold * avg_price_per_unit
        
        gross_margin = random.gauss(0.30, 0.03)
        gross_profit = total_revenue * gross_margin
        
        base_operating_expense = 200000
        variable_expense = total_revenue * random.gauss(0.08, 0.01)  # 8% ± 1% of revenue
        operating_expenses = base_operating_expense + variable_expense
        
        net_profit = gross_profit - operating_expenses
        
        report = {
            "month": month,
            "total_units_sold": total_units_sold,
            "average_price_per_unit": round(avg_price_per_unit, 2),
            "total_revenue": round(total_revenue, 2),
            "gross_margin": round(gross_margin, 4),
            "gross_profit": round(gross_profit, 2),
            "operating_expenses": round(operating_expenses, 2),
            "net_profit": round(net_profit, 2)
        }

        return report

    def generate(self, start_date, n_months, company_id = None):
        reports = []
        for i in range(n_months):
            report = self.generate_per_month(month=self.add_months(start_date, i))
            if company_id is not None:
                report['company_id'] = company_id
            reports.append(report)
        return reports

class business_trading_activity(Simulator):
    
    def __init__(self, time_switch = None, amount = 100):
        super().__init__()
        self.supplier = 'chip-supplier'
        self.importer = 'Yangjie-Tech'
        #self.target = 'Kalashnikov-Concern'
        
        self.chip_name = 'chip'
        
        self.std = 5
        self.amount = amount
    
    def random_amount(self, time):
        return round(random.normalvariate(self.amount, self.std), 0)
    
    def generate(self, n_months):
        transactions = []
        transaction_time = self.start
        for k in range(n_months):
            from_node, to_node = self.supplier, self.importer
            transaction_time = self.add_months(self.start, k)
            amount = self.random_amount(transaction_time)
            product_name = self.chip_name
            transactions.append((from_node, to_node, amount, product_name, transaction_time))
        return self.toTable(transactions, columns=['source','target','amount_per_month','product','time'])
    

        
