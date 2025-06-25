"""
	@file strategies/improved_dca.py
	@author Matěj Říčný
	@brief Simulates the improved DCA strategy
	@details Implements a modified Dollar-Cost Averaging strategy that invests
            at the beginning of each month, with the amount dynamically adjusted
            based on CBBI confidence and Fear & Greed Index.
            It tracks portfolio value, max loss, and total invested capital over time.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
import pandas as pd
import numpy as np

def improved_dca_strategy(data, assets, investment):
    buy_signal_multiplier = 2.6
    regular_multiplier = 0.6
    fng_threshold = 30
    confidence_threshold = 0.35

    investment_dates = pd.date_range(data.index[0], data.index[-1], freq='MS')
    monthly_investment = investment / len(investment_dates)

    data = data.copy()
    data.loc[:,'buy_signal'] = np.where((data["confidence"] < confidence_threshold) &  (data["fng_value"] < fng_threshold), 1, 0)

    portfolio = pd.DataFrame(index=data.index)
    portfolio['total_invested'] = 0.0
    invested = 0
    for asset in assets:
        investment_prices = data.loc[investment_dates, asset].dropna()
        units = 0
        # Buying every month, amount depends on signal
        for date, price in investment_prices.items():
            if data.loc[date, 'buy_signal'] == 1:
                invest_amount = monthly_investment * buy_signal_multiplier
            else:
                invest_amount = monthly_investment * regular_multiplier
            units += invest_amount / price
            invested += invest_amount
            # Value of each asset in $
            portfolio.loc[date:,f'{asset}_value'] = units * data.loc[date:, asset]
            portfolio.loc[date:,'total_invested'] = invested
    
    portfolio['portfolio_value'] = portfolio[[f'{asset}_value' for asset in assets]].sum(axis=1)
    portfolio['max_loss'] = ((portfolio['portfolio_value'] / portfolio['total_invested']) - 1) * 100

    return portfolio