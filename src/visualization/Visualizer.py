import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Any
from pathlib import Path

from numpy.distutils.lib2def import output_def


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
        Calculates variance and creates a histogram of ending balances.
        """
        if not statements_data:
            print("Warning: No statement data provided to visualize.")
            return

        # --- Data Extraction for Variance Analysis ---
        starting_balances = []
        ending_balances = []
        transaction_volumes = []

        for statement_details in statements_data.values():
            starting_balances.append(statement_details.get('starting_balance', 0))
            ending_balances.append(statement_details.get('ending_balance', 0))
            transaction_volumes.append(len(statement_details.get('transactions', [])))

        # --- Variance Calculation ---
        self.starting_balance_variance = np.var(starting_balances) if starting_balances else 0
        self.ending_balance_variance = np.var(ending_balances) if ending_balances else 0
        self.transaction_volume_variance = np.var(transaction_volumes) if transaction_volumes else 0

        # --- Graph Plotting ---
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        sns.set_theme(style="whitegrid")

        # Create a histogram to show the number of statements per ending balance category
        sns.histplot(data=ending_balances, kde=True, ax=self.ax, bins=10)

        self.ax.set_title('Distribution of Ending Balances Across Bank Statements', fontsize=16)
        self.ax.set_xlabel('Ending Balance Value', fontsize=12)
        self.ax.set_ylabel('Number of Bank Statements', fontsize=12)

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


# --- Example Usage ---
if __name__ == '__main__':
    # Sample data matching the expected input format

    # 1. Instantiate the visualizer
    visualizer = Visualizer()

    # 2. Generate the plot and calculate variances
    visualizer.plot_balance_distribution(sample_data)

    # 3. Save the plot to a file
    visualizer.save_plot("output/balance_distribution.png")

    # 4. (Optional) Access and print the calculated variances
    print("\n--- Calculated Variances ---")
    print(f"Ending Balance Variance: {visualizer.ending_balance_variance:.2f}")
    print(f"Starting Balance Variance: {visualizer.starting_balance_variance:.2f}")
    print(f"Transaction Volume Variance: {visualizer.transaction_volume_variance:.2f}")
