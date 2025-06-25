"""
	@file save_results.py
	@author Matěj Říčný
	@brief Saves the backtest results
	@details Takes a list of results from the backtest
            and saves it into structured JSON file.

	IMPROVING PREDICTION OF AUTOMATED TRADING STRATEGIES
    BASED ON DISPARATEEXTERNAL SOURCES
	Bachelor's thesis project at VUT Brno, Faculty of Information Technology
	Department of Intelligent Systems

	Supervisor: Ing. IVAN HOMOLIAK, Ph.D.
	2025
"""
import json
import numpy as np

def save_results(results):
    try:
        with open("results/final.json", "w") as f:
            json.dump(results, f, indent=4)
    except Exception as e:
        print("Error saving results: ",e)