"""
	@file backtest.py
	@author Matěj Říčný
	@brief Runs defined strategies
	@details Runs defined strategies over a selected date range
            and collects performance results.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
from strategies.hodl import hodl_strategy
from strategies.dca import dca_strategy
from strategies.rebalancing import rebalancing_strategy
from strategies.improved_dca import improved_dca_strategy
import pandas as pd

def roi(portfolio, invested):
    return ((portfolio / invested) - 1) * 100

def run_backtest(data, assets, start_dates, end_dates, investment, weights):
    if round(sum(weights.values()), 4) != 1.0:
        raise ValueError("Weights must sum to 1")
    results = []
    for start_date in start_dates:
        for end_date in end_dates:
            # Investment date range with datas
            date = data.loc[start_date:end_date]
            improved_dca_portfolio = improved_dca_strategy(date,assets, investment)
            hodl_portfolio = hodl_strategy(date, assets, investment, weights)
            dca_portfolio = dca_strategy(date, assets, investment, weights)
            #rebalancing_portfolio = rebalancing_strategy(date, assets, investment, weights) Working but not used with just Bitcoin
            results.append({
            "Start Date": start_date,
            "End Date": end_date,

            "HODL Portfolio": hodl_portfolio['portfolio_value'].iloc[-1],
            "HODL Invested": investment,
            "HODL ROI": roi(hodl_portfolio['portfolio_value'].iloc[-1], investment),
            "HODL Max Loss": hodl_portfolio["max_loss"].min(),

            "DCA Portfolio": dca_portfolio['portfolio_value'].iloc[-1],
            "DCA Invested": dca_portfolio['total_invested'].iloc[-1],
            "DCA ROI": roi(dca_portfolio['portfolio_value'].iloc[-1], investment),
            "DCA Max Loss": dca_portfolio["max_loss"].min(),

            #"Rebalanced Portfolio": rebalancing_portfolio.iloc[-1],
            #"Rebalanced Invested": investment,
            #"Rebalanced ROI": compute_roi(rebalancing_portfolio.iloc[-1], investment),
            #"Rebalanced Max Loss": calculate_max_loss_vs_invested(rebalancing_portfolio, investment),

            "Improved DCA Portfolio" : improved_dca_portfolio['portfolio_value'].iloc[-1],
            "Improved DCA Invested": improved_dca_portfolio['total_invested'].iloc[-1],
            "Improved DCA ROI": roi(improved_dca_portfolio['portfolio_value'].iloc[-1], improved_dca_portfolio['total_invested'].iloc[-1]),
            "Improved DCA Max Loss": improved_dca_portfolio["max_loss"].min(),
            })
    return results
    

