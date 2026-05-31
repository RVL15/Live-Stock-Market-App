import tkinter as tk
from tkinter import ttk
import threading
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import time
from datetime import datetime, timedelta

TOP_100_STOCKS = [
    "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "HINDUNILVR.NS",
    "KOTAKBANK.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "AXISBANK.NS",
    "ASIANPAINT.NS", "MARUTI.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "SUNPHARMA.NS",
    "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS", "POWERGRID.NS", "NTPC.NS",
    "HCLTECH.NS", "ONGC.NS", "NESTLEIND.NS", "GRASIM.NS", "ADANIENT.NS",
    "ADANIPORTS.NS", "TATAMOTORS.NS", "JSWSTEEL.NS", "TECHM.NS", "TATASTEEL.NS",
    "COALINDIA.NS", "BRITANNIA.NS", "HDFCLIFE.NS", "INDUSINDBK.NS", "DRREDDY.NS",
    "CIPLA.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "BPCL.NS", "APOLLOHOSP.NS",
    "DIVISLAB.NS", "BAJAJ-AUTO.NS", "M&M.NS", "PIDILITIND.NS", "DABUR.NS",
    "HAVELLS.NS", "ICICIPRULI.NS", "GODREJCP.NS", "HINDZINC.NS", "TORNTPHARM.NS",
    "COLPAL.NS", "BEL.NS", "BOSCHLTD.NS", "GLAND.NS", "ABB.NS",
    "BERGEPAINT.NS", "ESCORTS.NS", "LUPIN.NS", "MPHASIS.NS", "SRF.NS",
    "AUROPHARMA.NS", "ZYDUSLIFE.NS", "BANDHANBNK.NS", "TATACHEM.NS", "OBEROIRLTY.NS",
    "DLF.NS", "BIOCON.NS", "SUNTV.NS", "MFSL.NS", "LICHSGFIN.NS",
    "IDFCFIRSTB.NS", "PNB.NS", "INDIGO.NS", "TVSMOTOR.NS", "ASHOKLEY.NS",
    "CANBK.NS", "GAIL.NS", "NMDC.NS", "IGL.NS", "CHOLAFIN.NS",
    "HINDPETRO.NS", "TATAPOWER.NS", "TRENT.NS", "VEDL.NS", "PAGEIND.NS",
    "BALKRISIND.NS"
]

class LiveStockApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📈 Live Stock Market App")
        self.root.geometry("1600x900")
        self.root.configure(bg="#F8F9FA")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#F8F9FA")
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 12))
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.stock_tab = ttk.Frame(self.notebook)
        self.chart_tab = ttk.Frame(self.notebook)
        self.fundamental_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stock_tab, text="📃 Stock List")
        self.notebook.add(self.chart_tab, text="📊 Stock Chart")
        self.notebook.add(self.fundamental_tab, text="🔍 Fundamentals")

        self.create_filter_ui()
        self.create_stock_table()

        self.chart_frame = tk.Frame(self.chart_tab, bg="#F8F9FA")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.fundamental_frame = tk.Frame(self.fundamental_tab, bg="#F8F9FA")
        self.fundamental_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        self.progress = ttk.Progressbar(self.stock_tab, mode="indeterminate", length=300)
        self.progress.pack(pady=10)

        # Simple in-memory cache for yfinance calls (symbol -> (timestamp, data))
        self._cache = {
            'info': {},
            'history': {}
        }

        self.root.after(100, self.fetch_stock_data_threaded)
        self.root.mainloop()

    def create_filter_ui(self):
        self.filter_frame = tk.Frame(self.stock_tab, bg="#F8F9FA")
        self.filter_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(self.filter_frame, text="Min Price (INR):", bg="#F8F9FA", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5, pady=5)
        self.min_price_entry = tk.Entry(self.filter_frame, width=10)
        self.min_price_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.filter_frame, text="Max Price (INR):", bg="#F8F9FA", font=("Segoe UI", 11)).grid(row=0, column=2, padx=5)
        self.max_price_entry = tk.Entry(self.filter_frame, width=10)
        self.max_price_entry.grid(row=0, column=3, padx=5)

        tk.Label(self.filter_frame, text="Min Market Cap (Cr):", bg="#F8F9FA", font=("Segoe UI", 11)).grid(row=0, column=4, padx=5)
        self.min_marketcap_entry = tk.Entry(self.filter_frame, width=10)
        self.min_marketcap_entry.grid(row=0, column=5, padx=5)

        self.profit_filter = tk.StringVar()
        self.profit_filter.set("All")
        tk.Label(self.filter_frame, text="Profit/Loss:", bg="#F8F9FA", font=("Segoe UI", 11)).grid(row=0, column=6, padx=5)
        ttk.Combobox(self.filter_frame, textvariable=self.profit_filter, values=["All", "Profit", "Loss"], width=10).grid(row=0, column=7, padx=5)

        filter_button = tk.Button(self.filter_frame, text="Apply Filters", font=("Segoe UI", 10, "bold"),
                                  command=self.fetch_stock_data_threaded, bg="#007BFF", fg="white")
        filter_button.grid(row=0, column=8, padx=10)

    def create_stock_table(self):
        self.tree_frame = tk.Frame(self.stock_tab, bg="#F8F9FA")
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("S.No", "Stock", "Price"), show='headings')
        self.tree.heading("S.No", text="#")
        self.tree.heading("Stock", text="Stock Symbol")
        self.tree.heading("Price", text="Current Price (INR)")
        self.tree.column("S.No", width=60, anchor="center")
        self.tree.column("Stock", width=200)
        self.tree.column("Price", width=160)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_stock_select)

    def fetch_stock_data_threaded(self):
        threading.Thread(target=self.fetch_stock_data, daemon=True).start()

    def fetch_stock_data(self):
        self.progress.start()
        self.tree.delete(*self.tree.get_children())
        try:
            min_price = float(self.min_price_entry.get()) if self.min_price_entry.get() else 0
        except:
            min_price = 0
        try:
            max_price = float(self.max_price_entry.get()) if self.max_price_entry.get() else float('inf')
        except:
            max_price = float('inf')
        try:
            min_marketcap = float(self.min_marketcap_entry.get()) * 1e7 if self.min_marketcap_entry.get() else 0
        except:
            min_marketcap = 0
        profit_choice = self.profit_filter.get()

        for index, stock in enumerate(TOP_100_STOCKS, start=1):
            try:
                # Use cached history and info to reduce repeated network calls
                price_data = self.get_history_cached(stock, period='1d')
                if price_data is None or price_data.empty:
                    continue
                price = price_data['Close'].iloc[-1]
                open_price = price_data['Open'].iloc[0]
                info = self.get_info_cached(stock)
                market_cap = info.get("marketCap", 0) if isinstance(info, dict) else 0

                if not (min_price <= price <= max_price):
                    continue
                if market_cap < min_marketcap:
                    continue
                if profit_choice == "Profit" and price < open_price:
                    continue
                if profit_choice == "Loss" and price > open_price:
                    continue

                self.tree.insert("", tk.END, values=(index, stock, f"{price:.2f}"))
            except Exception as e:
                print(f"Error fetching {stock}: {e}")
        self.progress.stop()

    def _with_retries(self, func, *args, retries=3, backoff=1, **kwargs):
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exc = e
                time.sleep(backoff * attempt)
        raise last_exc

    def get_history_cached(self, symbol, period='1d', interval=None, ttl_seconds=60):
        key = f"{symbol}|{period}|{interval}"
        entry = self._cache['history'].get(key)
        now = datetime.utcnow()
        if entry:
            ts, data = entry
            if now - ts < timedelta(seconds=ttl_seconds):
                return data
        def _fetch():
            ticker = yf.Ticker(symbol)
            # prefer interval when provided
            if interval:
                return ticker.history(period=period, interval=interval)
            return ticker.history(period=period)

        data = self._with_retries(_fetch)
        self._cache['history'][key] = (now, data)
        return data

    def get_info_cached(self, symbol, ttl_seconds=60):
        entry = self._cache['info'].get(symbol)
        now = datetime.utcnow()
        if entry:
            ts, data = entry
            if now - ts < timedelta(seconds=ttl_seconds):
                return data
        def _fetch():
            ticker = yf.Ticker(symbol)
            return ticker.info or {}

        info = self._with_retries(_fetch)
        # ensure a dict
        info = info if isinstance(info, dict) else {}
        self._cache['info'][symbol] = (now, info)
        return info

    def on_stock_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        stock_symbol = self.tree.item(selected_item[0], 'values')[1]
        self.show_stock_chart(stock_symbol)
        self.show_fundamentals(stock_symbol)

    def show_stock_chart(self, stock_symbol):
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period='1d', interval='15m')
        if data.empty:
            return
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(data.index, data['Close'], label=f'{stock_symbol} Price', color='blue')
        ax.set_title(f'{stock_symbol} Intraday Chart (15 min)', fontsize=14)
        ax.set_xlabel('Time')
        ax.set_ylabel('Price (INR)')
        ax.legend()
        ax.grid(True)

        latest_time = data.index[-1].strftime('%d-%b-%Y %H:%M')
        ax.annotate(f"Last Updated: {latest_time}",
                    xy=(1, 1), xycoords='axes fraction',
                    ha='right', va='top', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray"))
        mplcursors.cursor(ax)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def show_fundamentals(self, stock_symbol):
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        fundamentals = {
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "ROCE": info.get("returnOnEquity", "N/A"),
            "Debt/Equity Ratio": info.get("debtToEquity", "N/A"),
            "Market Cap": self.format_market_cap(info.get("marketCap", "N/A")),
            "52-Week High": f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}",
            "52-Week Low": f"₹{info.get('fiftyTwoWeekLow', 'N/A')}",
            "Dividend Yield": info.get("dividendYield", "N/A")
        }

        for widget in self.fundamental_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.fundamental_frame, text=f"Fundamentals of {stock_symbol}",
                         font=("Segoe UI", 18, "bold"), fg="black", bg="#F8F9FA", pady=10)
        title.pack()

        fundamentals_frame = tk.Frame(self.fundamental_frame, bg="#F8F9FA")
        fundamentals_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for i, (key, value) in enumerate(fundamentals.items()):
            label_key = tk.Label(fundamentals_frame, text=f"{key}:", font=("Segoe UI", 14, "bold"),
                                 fg="black", bg="#F8F9FA", anchor="w")
            label_key.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            label_value = tk.Label(fundamentals_frame, text=value, font=("Segoe UI", 14),
                                   fg="black", bg="#F8F9FA", anchor="w")
            label_value.grid(row=i, column=1, sticky="w", padx=10, pady=5)

    def format_market_cap(self, value):
        if not isinstance(value, (int, float)):
            return "N/A"
        if value >= 1e12:
            return f"₹{value / 1e12:.2f} Lakh Cr"
        elif value >= 1e7:
            return f"₹{value / 1e7:.2f} Cr"
        elif value >= 1e5:
            return f"₹{value / 1e5:.2f} Lakh"
        elif value >= 1e3:
            return f"₹{value / 1e3:.2f} Thousand"
        else:
            return f"₹{value:.2f}"

if __name__ == "__main__":
    LiveStockApp()