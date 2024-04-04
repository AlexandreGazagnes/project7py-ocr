import csv

MAX_INVEST = 500

def find_best_investments(filename, max_invest):
  
  best_investments = []
  remaining = max_invest

  with open(filename) as f:
    rows = csv.reader(f)
    next(rows)
    
    for name, buy_price, sell_price in rows:
      buy_price = float(buy_price)
      sell_price = float(sell_price)

      return_rate = (sell_price - buy_price) / buy_price
      invest_amount = min(remaining, buy_price)

      if remaining > 0:
        best_investments.append((name, invest_amount, return_rate))
        remaining -= invest_amount

  print("\n Meilleur stratégie d'investissement: \n")  

  total_return = 0
  for name, amount, rate in best_investments:
    total_return += amount
    print(f"- Investir {amount} dans {name}")

  print(f"\n Total de l'investissement: {total_return}")

find_best_investments("data/originalfile.csv", MAX_INVEST)