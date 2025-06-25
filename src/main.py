"""
	@file main.py
	@author Matěj Říčný
	@brief Setup parametres 
	@details Defines parameters: start and end dates, capital, asset weights, and the list of assets to test.
            It then calls the backtest function to run simulations and saves the output using a results-saving function.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
from backtest import run_backtest
from save_results import save_results
import pandas as pd

def main():
    file = "data/merged_btc_data.csv"
    try:
        with open(file, "r") as f:
            data = pd.read_csv(f, index_col="date", parse_dates=True)
    except FileNotFoundError:
        print("File:", file, "was not found")
        return
    # Same name as column in file
    assets = ["BTC-USD"]
    start_dates = [
    '2021-01-15',
    '2021-03-18',
    '2021-06-10',
    '2021-08-30',
    '2021-11-05',
    '2022-01-21',
    '2022-04-01',
    '2022-07-20',
    '2022-10-10',
    '2022-12-01',
    ]
    end_dates = [
    '2023-12-15',
    '2024-03-30',
    '2024-06-15',
    '2024-09-30',
    '2024-11-30',
    '2024-12-31'
    ]
    investment = 30000
    # Two Assets example {'BTC-USD': 0.5, 'ETH-USD' : 0.5}
    weights = {'BTC-USD': 1}
    results = run_backtest(data,assets, start_dates, end_dates, investment, weights)
    save_results(results)
if __name__ == '__main__':
    main()
