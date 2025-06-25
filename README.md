## How to Run

python3 main.py

## Configuration

Configure parametres in `main.py`:

-  `file` Path to the CSV file with historical price data

-  `assets` List of asset to include in the simulation
  
-  `weights` Dictionary assigning a portfolio weight to each asset
  
-  `start_dates` List of start dates for each investment period

-  `end_dates` List of end dates for each investment period

-  `investment` Total capital ($) to be distributed across the investment periods
## Output

- Simulation results are saved in JSON format.
- The output file path can be configured in `save_results.py` by `file` parameter.
## Plotting

- Use `plot_basic_results.py` or `plot_dca_vs_improved.py` to generate plots.
- Require `file` parameter that specifies where the JSON results are saved.
## Folder Structure

- `strategies/`  Implementation of investment strategies  
- `img/` Generated plots  
- `results/`  Performance of strategies in JSON format