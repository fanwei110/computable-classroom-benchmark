import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_and_plot_sml(risk_free_rate, market_return):
    # Calculate SML slope (market risk premium)
    sml_slope = market_return - risk_free_rate

    # Calculate expected return at beta=1.27
    beta_127 = 1.27
    er_at_beta_127 = risk_free_rate + beta_127 * sml_slope

    # Generate beta values from 0 to 2
    betas = np.linspace(0, 2, 100)
    expected_returns = risk_free_rate + betas * sml_slope

    # Create figure
    plt.figure(figsize=(10, 6))
    plt.plot(betas, expected_returns, label='Security Market Line', color='blue')

    # Plot stocks with annotations
    stocks = {
        'X': {'beta': 0.62, 'return': 8.1},
        'Y': {'beta': 1.18, 'return': 13.1},
        'Z': {'beta': 1.51, 'return': 9.9}
    }

    for name, data in stocks.items():
        plt.scatter(data['beta'], data['return'], color='red', zorder=5)
        plt.annotate(name,
                     (data['beta'], data['return']),
                     textcoords="offset points",
                     xytext=(10,5),
                     ha='center')

    # Add labels and title
    plt.title('Security Market Line with Stocks X, Y, Z')
    plt.xlabel('Beta (β)')
    plt.ylabel('Expected Return (%)')
    plt.grid(True)
    plt.legend()

    # Save figure
    figure_path = 'sml_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # Prepare result dictionary
    result = {
        'sml_slope': sml_slope,
        'er_at_beta_127': er_at_beta_127,
        'figure_path': os.path.abspath(figure_path)
    }

    return result

# Given parameters
risk_free_rate = 2.3  # %
market_return = 9.4   # %

# Calculate and plot
result = calculate_and_plot_sml(risk_free_rate, market_return)

# Print results for verification
print("Results:")
print(f"SML Slope: {result['sml_slope']:.4f}")
print(f"Expected Return at β=1.27: {result['er_at_beta_127']:.4f}%")
print(f"Figure saved to: {result['figure_path']}")
