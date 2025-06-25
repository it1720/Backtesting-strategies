"""
	@file strategies/rebalancing.py
	@author Matěj Říčný
	@brief Simulates the hourly Rebalancing strategy
	@details Rebalances the portfolio to predefined asset weights on every date in the simulation,
            requiring hourly data. It tracks portfolio value and max loss.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
""" 
import pandas as pd

def rebalancing_strategy(data, assets, investment, weights):
    initial_prices = data.iloc[0]
    # Buying on the first date
    units = {asset: (weights[asset] * investment) / initial_prices[asset] for asset in assets}
    portfolio = pd.DataFrame(index=data.index)
    for date, row in data.iterrows():
        for asset in assets:
            portfolio.loc[date, f'{asset}_value'] = units[asset] * row[asset]
        portfolio.loc[date, 'portfolio_value'] = portfolio.loc[date, [f'{asset}_value' for asset in assets]].sum()
        # Rebalancing every date based on weights
        for asset in assets:
            units[asset] = (weights[asset] * portfolio.loc[date, 'portfolio_value']) / row[asset]

    return portfolio