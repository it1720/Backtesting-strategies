"""
	@file strategies/dca.py
	@author Matěj Říčný
	@brief Simulates the DCA strategy
	@details Implements the Dollar-Cost Averaging strategy
            by investing fixed amounts at end of the month and recording 
            portfolio value, max loss and invested capital over time.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
import pandas as pd

def dca_strategy(data, assets, investment, weights):
    investment_dates = pd.date_range(data.index[0], data.index[-1], freq='M')
    monthly_investment = investment / len(investment_dates)

    portfolio = pd.DataFrame(index=data.index)
    portfolio['total_invested'] = 0.0
    for asset in assets:
        investment_prices = data.loc[investment_dates, asset].dropna()
        units = 0
        invested = 0
        # Buying every month
        for date, price in investment_prices.items():
            units += (weights[asset] * monthly_investment) / price
            invested += monthly_investment
            # Value of each asset in $
            portfolio.loc[date:,f'{asset}_value'] = units * data.loc[date:, asset]
            portfolio.loc[date:,'total_invested'] = invested

    portfolio['portfolio_value'] = portfolio[[f'{asset}_value' for asset in assets]].sum(axis=1)
    portfolio['max_loss'] = ((portfolio['portfolio_value'] / portfolio['total_invested']) - 1) * 100

    return portfolio
