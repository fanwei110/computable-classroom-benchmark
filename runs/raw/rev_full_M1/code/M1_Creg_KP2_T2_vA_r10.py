import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_and_plot_sml(risk_free_rate, market_return):
    # Calculate SML slope (market risk premium)
    sml_slope = market_return - risk_free_rate

    # Calculate expected return at beta=1.27
    er_at_beta_127 = risk_free_rate + 1.27 * sml_slope

    # Create beta range for SML line
    beta_range = np.linspace(0, 2, 100)
    expected_returns = risk_free_rate + beta_range * sml_slope

    # Create figure
    plt.figure(figsize=(10, 6))

    # Plot SML line
    plt.plot(beta_range, expected_returns, label='Security Market Line', color='blue')

    # Plot stocks with annotations
    stocks = {
        'X': {'beta': 0.62, 'return': 8.1},
        'Y': {'beta': 1.18, 'return': 13.1},
        'Z': {'beta': 1.51, 'return': 9.9}
    }

    for name, data in stocks.items():
        plt.scatter(data['beta'], data['return'], label=f'Stock {name}')
        plt.annotate(f'{name} ({data["beta"]}, {data["return"]}%)',
                     (data['beta'], data['return']),
                     textcoords="offset points",
                     xytext=(10,5),
                     ha='center')

    # Plot risk-free rate point
    plt.scatter(0, risk_free_rate, color='green', label='Risk-free Rate')
    plt.annotate(f'RF ({risk_free_rate}%)',
                 (0, risk_free_rate),
                 textcoords="offset points",
                 xytext=(10,5),
                 ha='center')

    # Plot market portfolio point
    plt.scatter(1, market_return, color='red', label='Market Portfolio')
    plt.annotate(f'M (1, {market_return}%)',
                 (1, market_return),
                 textcoords="offset points",
                 xytext=(10,5),
                 ha='center')

    # Add labels and title
    plt.title('Security Market Line with Sample Stocks')
    plt.xlabel('Beta (Systematic Risk)')
    plt.ylabel('Expected Return (%)')
    plt.legend()
    plt.grid(True)

    # Save figure
    figure_path = 'security_market_line.png'
    plt.savefig(figure_path)
    plt.close()

    # Prepare results
    result = {
        'sml_slope': sml_slope,
        'er_at_beta_127': er_at_beta_127,
        'figure_path': os.path.abspath(figure_path)
    }

    return result

# Main execution
if __name__ == "__main__":
    # Given parameters
    risk_free_rate = 2.3  # %
    market_return = 9.4   # %

    # Calculate and plot
    result = calculate_and_plot_sml(risk_free_rate, market_return)

    # Print results (as per output contract)
    print("result = {")
    print(f"    'sml_slope': {result['sml_slope']},")
    print(f"    'er_at_beta_127': {result['er_at_beta_127']},")
    print(f"    'figure_path': '{result['figure_path']}'")
    print("}")
