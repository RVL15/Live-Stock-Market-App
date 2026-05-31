# 📈 Live Stock Market App

A powerful Python-based desktop application that displays **live Indian stock market data**, charts, and fundamentals using a clean GUI.

---

## 🚀 Features

* 📃 Top 100 Indian Stocks (NSE)
* 📊 Intraday Stock Charts (15-minute interval)
* 🔍 Fundamental Analysis:

  * P/E Ratio
  * ROCE
  * Debt/Equity
  * Market Cap
  * 52 Week High/Low
* 🎯 Filters:

  * Price Range
  * Market Cap
  * Profit / Loss
* ⚡ Fast & Interactive UI
* 📌 Double-click stock → View chart + fundamentals

---

## 🛠 Tech Stack

* Python 🐍
* Tkinter (GUI)
* yfinance (Stock Data API)
* matplotlib (Charts)
* mplcursors (Interactive cursor)

---

## 📦 Installation

Clone the repository:

```
git clone https://github.com/RVL15/Live-Stock-Market-App.git
cd Live-Stock-Market-App
```

Install dependencies:

```
pip install -r requirements.txt
```

Note: `tkinter` is part of the standard Python distribution on Windows and is not listed in `requirements.txt`.
Make sure you have Python 3.8+ installed (Tkinter comes bundled with standard installers).

Quick run (Windows)

You can use the helper scripts to create a virtual environment, install dependencies, and run the app.

PowerShell:

```
.\run_app.ps1
```

Command Prompt:

```
run_app.bat
```

Logs are written to `run.log` in the project root when using the helper scripts.

---

## 🧭 Manual Run (Step-by-step)

These steps work on Windows, macOS, and Linux with minor differences in the activation step.

1. Ensure you have Python 3.8+ installed. On Windows, the official installer includes `tkinter`.

2. From the project root create and activate a virtual environment:

PowerShell (Windows):

```
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

Command Prompt (Windows):

```
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (pinned versions are recommended):

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Run the app:

```
python stock_app.py
```

Alternatively on Windows you can use the included helpers:

```
.\run_app.ps1   # PowerShell helper
run_app.bat     # Command Prompt helper
```

Helpers create a `.venv`, install dependencies, run the app and write stdout/stderr to `run.log`.

---

## 🛠 What changed in the code

- Added a simple in-memory cache for `yfinance` `history` and `info` calls to reduce repeated requests during a single run.
- Added a retry wrapper for network calls (3 attempts with backoff) to improve robustness against transient errors.
- Added `run_app.ps1` and `run_app.bat` helpers and added `run.log` usage in README.

---

## 🐞 Troubleshooting

- If the GUI does not appear or the process exits immediately, check `run.log` for tracebacks. If empty, run the program directly in a terminal to see errors:

```
python stock_app.py
```

- Common issues:
  - `tkinter` not found: install the standard Python distribution from python.org or use your OS package manager to install the `tk`/`python3-tk` package.
  - Network errors / rate limits from Yahoo Finance: wait a few minutes or reduce the number of stocks being fetched; consider running the app again.
  - Missing dependencies: ensure the virtual environment is activated and `pip install -r requirements.txt` completed successfully.

---

If you run into any errors, paste the full traceback or the `run.log` contents here and I'll help fix them.

---

## ▶️ Run the App

```
python stock_app.py
```

---

## 📂 Project Structure

```
Live-Stock-Market-App/
│── stock_app.py
│── requirements.txt
│── README.md
```

---

## ⚠️ Notes

* Uses Yahoo Finance API → may occasionally fail due to rate limits
* Internet connection required

---

## 🔥 Future Improvements

* 💼 Portfolio Management (Buy/Sell system)
* 📉 Technical Indicators (RSI, SMA)
* 🌐 Web Version (Flask/React)
* ⚡ Real-time streaming data

---

## 👨‍💻 Author

**Rishabh Lokhande**

GitHub: https://github.com/RVL15

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 💡 Contribute

---
