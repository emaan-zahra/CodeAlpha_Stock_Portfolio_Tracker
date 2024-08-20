import yfinance as yf
import pandas as pd

class Portfolio:
    def __init__(self):
        self.stocks = {}  # Dictionary to store stock symbols and quantities

    def add_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] += quantity
        else:
            self.stocks[symbol] = quantity
        print(f"Added {quantity} shares of {symbol} to your portfolio.")

    def remove_stock(self, symbol, quantity):
        if symbol in self.stocks:
            if self.stocks[symbol] >= quantity:
                self.stocks[symbol] -= quantity
                if self.stocks[symbol] == 0:
                    del self.stocks[symbol]
                print(f"Removed {quantity} shares of {symbol} from your portfolio.")
            else:
                print(f"Not enough shares of {symbol} in your portfolio.")
        else:
            print(f"{symbol} is not in your portfolio.")

    def get_stock_data(self, symbol, period="1d", interval="1d"):
        try:
            data = yf.download(symbol, period=period, interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def get_portfolio_value(self, date=None):
        total_value = 0
        for symbol, quantity in self.stocks.items():
            data = self.get_stock_data(symbol)
            if data is not None:
                if date is None:
                    price = data["Close"][-1]  # Get the latest closing price
                else:
                    try:
                        price = data["Close"].loc[date]
                    except KeyError:
                        print(f"No data available for {symbol} on {date}")
                        price = 0
                total_value += price * quantity
        return total_value

    def get_historical_data(self, start_date, end_date):
        historical_data = {}
        for symbol, quantity in self.stocks.items():
            data = self.get_stock_data(symbol, period="max", interval="1d")
            if data is not None:
                historical_data[symbol] = data["Close"][start_date:end_date]
        return historical_data

    def display_portfolio_value(self):
        value = self.get_portfolio_value()
        print(f"Your portfolio value is: ${value:.2f}")

    def display_historical_performance(self, start_date, end_date):
        historical_data = self.get_historical_data(start_date, end_date)

        if historical_data:
            df = pd.DataFrame(historical_data)
            print(df)
        else:
            print("No historical data found for the specified period.")

def main():
    portfolio = Portfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio Value")
        print("4. View Historical Performance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            quantity = int(input("Enter quantity: "))
            portfolio.add_stock(symbol, quantity)

        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            quantity = int(input("Enter quantity to remove: "))
            portfolio.remove_stock(symbol, quantity)

        elif choice == "3":
            portfolio.display_portfolio_value()

        elif choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            portfolio.display_historical_performance(start_date, end_date)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
