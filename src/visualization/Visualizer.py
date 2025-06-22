import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Any
from pathlib import Path

from src.utils.constants import *


class Visualizer:

    def __init__(self):
        """Initializes the Visualizer's state."""
        self.running_balance_variance = None
        self.fig = None
        self.ax = None
        # Attributes to store calculated variances

    def plot_balance_distribution(self, statements_data: Dict[str, Dict[str, Any]]) -> None:
        """
        Calculates and plots the variance of running balances across all transactions in all statements.
        """
        if not statements_data:
            print("Warning: No statement data provided to visualize.")
            return

        ending_variances = {}

        for key, statement in statements_data.items():
            if not statement:
                print(f"WARNING: Empty statement_details for {key}, skipping")
                continue

            balance = abs(statement.get(STARTING_BALANCE, 0))
            transactions = statement.get(TRANSACTIONS, [])
            running_balance = [balance]

            for txn in transactions:
                direction = txn.get("direction", "").lower()
                amount = abs(txn.get("amount", 0))

                if direction == "debit":
                    balance -= amount
                elif direction == "credit":
                    balance += amount
                else:
                    print(f"! Unknown direction '{direction}' in {key}, skipping transaction.")
                    continue
                running_balance.append(balance)
            ending_variances[key] = np.var(running_balance)

        if not ending_variances:
            print("No running balances computed; cannot plot.")
            return

        # --- Graph Plotting ---
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        sns.set_theme(style="whitegrid")

        sns.lineplot(x=ending_variances.keys(),
                     y=ending_variances.values(),
                     ax=self.ax,
                     marker="o")

        self.ax.set_title('Distribution of Running Balances Across All Transactions', fontsize=16)
        self.ax.set_xlabel('Bank Statment', fontsize=12)
        self.ax.set_ylabel('Ending Balance Variance', fontsize=12)

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
