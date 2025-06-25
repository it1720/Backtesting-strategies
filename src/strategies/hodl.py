"""
	@file strategies/hodl.py
	@author Matěj Říčný
	@brief Simulates the HODL strategy
	@details Implements the buy-and-hold strategy Averaging strategy
            by investing the entire capital on the first date and holding it over the period.
            It tracks portfolio value and max loss.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
""" 
import pandas as pd

def hodl_strategy(data, assets,investment, weights):
    initial_price = data.iloc[0]
    portfolio = pd.DataFrame(index=data.index)
    # Buying on the first date
    for asset in assets:
        initial_price_value = initial_price[asset]
        units = (weights[asset] * investment) / initial_price_value 
        
        portfolio[f'{asset}_value'] = units * data[asset]

    portfolio['portfolio_value'] = portfolio[[f'{asset}_value' for asset in assets]].sum(axis=1)
    portfolio['max_loss'] = (portfolio['portfolio_value'] / investment - 1) * 100
    
    return portfolio
