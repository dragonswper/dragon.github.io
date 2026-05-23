# 📈 TradeSim Pro — AI Trading Learning Simulator

A professional-grade trading simulator with a dark terminal UI, real market data,
a full news page, and three language/knowledge modes.

---

## 🚀 Quick Start

### Step 1 — Install dependencies
```
pip install -r requirements.txt
```

### Step 2 — Run the app
```
python -m streamlit run app.py
```

Opens at: http://localhost:8501

---

## 🗂️ Files

```
trading_simulator/
├── app.py              ← Full application (~950 lines)
├── requirements.txt    ← 7 free packages
└── README.md           ← This file
```

---

## 🎮 Features

| Feature | Detail |
|---------|--------|
| Dark Terminal UI | Styled like Tastytrade / Bloomberg Terminal |
| Real Market Data | Live prices via Yahoo Finance (yfinance) — no API key |
| ASX Full Access | Any ASX stock via TICKER.AX + 15 pre-loaded blue chips |
| US & Global | SPY, QQQ, NVDA, AAPL, gold/sector ETFs |
| Live Status Dot | Green = market open, Yellow = pre/after hours, Red = closed |
| 4 Indicators | RSI, SMA 20/50, Bollinger Bands, Volume |
| AI Trading Coach | Rule-based explanations after every trade |
| Prediction Engine | UP/DOWN/HOLD with confidence % |
| Market Movers | Live top 10 movers panel |
| News & Reports Tab | Apple News / NYT-style layout with real source links |
| Backtest Mode | SMA crossover strategy over 1–5 years |
| Stop-Loss | Auto-sell when position drops N% |
| Portfolio Tab | P&L, equity curve, pie chart |
| 3 Language Modes | Standard, Beginner, FPS Gamer |
| Learn Tab | RSI, ETFs, moving averages, glossary in all 3 modes |

---

## 🌐 Language Modes

Switch in the sidebar:

- **📊 Standard** — Professional trading terminology
- **🌱 Beginner** — Plain English, every term explained simply  
- **🎮 FPS Gamer** — Trading translated into shooter game language
  - RSI = Enemy HP Bar
  - Stop-loss = Respawn Insurance
  - ETF = Squad Bundle Pack
  - Golden Cross = Killstreak Activated

---

## 📰 News Page

The News & Reports tab features:
- Apple News / New York Times inspired layout
- Featured stories with full summary
- Category filters: Markets, ASX, Tech, Economy, World
- Sentiment badges (Bullish / Bearish / Neutral)
- Ticker tags linking news to stocks
- **Direct links to real sources** (Reuters, Bloomberg, AFR, CNBC, WSJ, FT, SMH)
- Data source footer with all attribution links

---

## ⚙️ Stack

- **Streamlit** — UI framework
- **yfinance** — Free real-time/delayed market data
- **Plotly** — Interactive candlestick + RSI + volume charts
- **pytz** — Market hours timezone detection
- **pandas / numpy** — Data processing

No paid APIs. No cloud required. Runs on any laptop.

---

## 🔧 Troubleshooting

**"streamlit not recognised"**
```
python -m streamlit run app.py
```

**"pip not recognised"**
```
python -m pip install -r requirements.txt
```

**Slow first load**
Data is cached 5 minutes — first fetch per ticker takes a few seconds.

**"No data for ticker"**
ASX stocks need `.AX` suffix: `BHP.AX` not `BHP`

---

## ⚠️ Disclaimer

All money is virtual. This is for educational purposes only.
Not financial advice. Past performance does not guarantee future results.
