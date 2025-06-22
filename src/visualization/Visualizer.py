import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Any
from pathlib import Path

from src.utils.constants import *


class Visualizer:

    def __init__(self):
        """Initializes the Visualizer's state."""
        self.fig = None
        self.ax = None
        # Attributes to store calculated variances
        self.starting_balance_variance: float = 0.0
        self.ending_balance_variance: float = 0.0
        self.transaction_volume_variance: float = 0.0

    def plot_balance_distribution(self, statements_data: Dict[str, Dict[str, Any]]) -> None:
        """
        Calculates and plots the variance of running balances across all transactions in all statements.
        """
        if not statements_data:
            print("Warning: No statement data provided to visualize.")
            return

        running_balances = []

        for key, statement in statements_data.items():
            if not statement:
                print(f"WARNING: Empty statement_details for {key}, skipping")
                continue

            balance = statement.get(STARTING_BALANCE, 0)
            transactions = statement.get(TRANSACTIONS, [])

            for txn in transactions:
                direction = txn.get("direction", "").lower()
                amount = txn.get("amount", 0)

                if direction == "debit":
                    balance -= amount
                elif direction == "credit":
                    balance += amount
                else:
                    print(f"! Unknown direction '{direction}' in {key}, skipping transaction.")
                    continue

                running_balances.append(balance)

        if not running_balances:
            print("No running balances computed; cannot plot.")
            return

        # --- Variance Calculation ---
        self.running_balance_variance = np.var(running_balances)

        # --- Graph Plotting ---
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        sns.set_theme(style="whitegrid")

        sns.histplot(data=running_balances, kde=True, ax=self.ax, bins=10)

        self.ax.set_title('Distribution of Running Balances Across All Transactions', fontsize=16)
        self.ax.set_xlabel('Running Balance Value', fontsize=12)
        self.ax.set_ylabel('Frequency', fontsize=12)

    def save_plot(self, config: Dict) -> None:
        output_path = config["plots_output_dir"]
        if self.fig is None:
            raise RuntimeError('A plot must be created with plot_balance_distribution() before it can be saved.')
        output_path = output_path + "/balance_distribution.png"
        # Ensure the output directory exists before saving[2]
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        # Save the figure with high resolution and tight layout
        self.fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(self.fig)
        print(f"Visualization saved successfully to: {output_path}")
