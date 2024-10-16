import requests
import tkinter as tk
from tkinter import ttk


def cleanInput(text):
    """Converts full currency text and returns the currency code.
    cleanInput('US Dollar (USD)') = 'USD'

    Args:
      text: The full currency text.

    Returns:
      The currency code.
    """

    return text[text.find("(") + 1 : text.find(")")]


def updateOutput():
    """Converts the currency and updates the result label."""

    try:
        currency1 = cleanInput(currency1_var.get())
        currency2 = cleanInput(currency2_var.get())
        currency_value = float(currency_value_entry.get())

        result = convertCurrency(currency1, currency2, currency_value)
        result_label.config(
            text=f"{currency_value:.2f} {currency1.upper()} is equal to {result:.2f} {currency2.upper()}"
        )
    except ValueError as e:
        result_label.config(text=str(e))


def convertCurrency(currency1, currency2, currency_value):
    """Converts a currency value from one currency to another.

    Args:
      currency1: The source currency code.
      currency2: The target currency code.
      currency_value: The value to be converted.

    Returns:
      The converted value.
    """

    apiKey = "fxr_live_c408a6dd85fcdb3059c567c20e982ecdb809"
    url = f"https://api.fxratesapi.com/convert?api_key={apiKey}&from={currency1}&to={currency2}&amount={currency_value}"
    response = requests.get(url)
    data = response.json()

    if data["success"] != True:
        raise ValueError(f"ERROR: Invalid currency")

    return data["result"]


def currencyCodes():
    """Retrieves a list of currency codes.

    Returns:
      A sorted list of currency codes.
    """

    url = "https://api.fxratesapi.com/currencies"
    response = requests.get(url)
    data = response.json()

    # Create a list of formatted currency names
    formatted_currencies = [
        f"{currency['name']} ({currency['code']})" for currency in data.values()
    ]

    # Sort the list alphabetically
    # ['Afghan Afghani (AFN)', 'Albanian Lek (ALL)', etc.]
    return sorted(formatted_currencies)


# Create the main window
root = tk.Tk()
root.title("Currency Converter")

# Currency codes from 'https://api.fxratesapi.com/currencies'
currency_codes = currencyCodes()

# Currency 1 Dropdown
currency1_var = tk.StringVar(value="Currency Code 1")
currency1_label = tk.Label(root, text="From:")
currency1_label.grid(row=0, column=0, padx=20, pady=10)
currency1_dropdown = ttk.Combobox(
    root, textvariable=currency1_var, values=currency_codes, width=35
)
currency1_dropdown.grid(row=0, column=1, padx=20, pady=10)

# Currency 2 Dropdown
currency2_var = tk.StringVar(value="Currency Code 2")
currency2_label = tk.Label(root, text="To:")
currency2_label.grid(row=1, column=0, padx=20, pady=10)
currency2_dropdown = ttk.Combobox(
    root, textvariable=currency2_var, values=currency_codes, width=35
)
currency2_dropdown.grid(row=1, column=1, padx=20, pady=10)

# Currency Value Input
currency_value_label = tk.Label(root, text="Amount:")
currency_value_label.grid(row=2, column=0, padx=20, pady=10)
currency_value_entry = tk.Entry(root, width=38)
currency_value_entry.grid(row=2, column=1, padx=20, pady=10)

# Convert Button
convert_button = tk.Button(root, text="Convert", command=updateOutput)
convert_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

# Result Label
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

root.mainloop()
