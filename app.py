"""
AI Trading Learning Simulator — Pro Terminal Edition
Dark trading terminal UI. Real data. News page. Language modes.
Styled after professional trading platforms (Tastytrade / Bloomberg).
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timezone
import pytz
import random
import json
import os
from pathlib import Path

# ─────────────────────────────────────────────
st.set_page_config(page_title="TradeSim Pro", page_icon="📈",
                   layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────
# GLOBAL CSS — Professional dark terminal
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,500&display=swap');

:root {
  --bg:#0b0e11; --bg2:#111519; --bg3:#161b21; --bg4:#1a2028;
  --border:#1e2530; --border2:#252d38; --border3:#2d3748;
  --text:#d1d5db; --text2:#8892a4; --text3:#4b5563;
  --accent:#3b82f6; --green:#22c55e; --red:#ef4444;
  --yellow:#f59e0b; --cyan:#06b6d4; --purple:#8b5cf6;
  --mono:'IBM Plex Mono',monospace; --sans:'IBM Plex Sans',sans-serif;
}
html,body,[class*="css"],.stApp{background:var(--bg)!important;color:var(--text)!important;font-family:var(--sans)!important;}
#MainMenu,footer,header,.stDeployButton{display:none!important;}
.main .block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]>div:first-child{padding-top:0!important;}
div[data-testid="stSidebar"]{background:var(--bg2)!important;border-right:1px solid var(--border)!important;min-width:210px!important;max-width:210px!important;}
div[data-testid="stSidebar"] .block-container{padding:0!important;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:var(--bg2)!important;border-bottom:1px solid var(--border)!important;padding:0 0.5rem!important;gap:0!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--text2)!important;font-family:var(--mono)!important;font-size:0.75rem!important;font-weight:500!important;padding:0.6rem 0.9rem!important;border:none!important;border-bottom:2px solid transparent!important;border-radius:0!important;letter-spacing:0.03em!important;}
.stTabs [aria-selected="true"]{color:var(--text)!important;border-bottom:2px solid var(--accent)!important;}
.stTabs [data-baseweb="tab-panel"]{padding:0!important;background:var(--bg)!important;}

/* Metrics */
[data-testid="metric-container"]{background:var(--bg2)!important;border:1px solid var(--border)!important;border-radius:3px!important;padding:0.55rem 0.75rem!important;}
[data-testid="metric-container"] label{font-family:var(--mono)!important;font-size:0.62rem!important;color:var(--text2)!important;text-transform:uppercase!important;letter-spacing:0.08em!important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{font-family:var(--mono)!important;font-size:1rem!important;color:var(--text)!important;}
[data-testid="stMetricDelta"]{font-family:var(--mono)!important;font-size:0.72rem!important;}

/* Form elements */
.stSelectbox>div>div,.stTextInput>div>div>input,.stNumberInput>div>div>input{background:var(--bg3)!important;border:1px solid var(--border2)!important;border-radius:3px!important;color:var(--text)!important;font-family:var(--mono)!important;font-size:0.78rem!important;}
.stSelectbox label,.stTextInput label,.stNumberInput label,.stSlider label,.stRadio label{color:var(--text2)!important;font-size:0.65rem!important;font-family:var(--mono)!important;text-transform:uppercase!important;letter-spacing:0.07em!important;}

/* Buttons */
.stButton>button{background:var(--bg3)!important;border:1px solid var(--border2)!important;border-radius:3px!important;color:var(--text)!important;font-family:var(--mono)!important;font-size:0.75rem!important;font-weight:500!important;padding:0.38rem 0.75rem!important;transition:all 0.12s!important;}
.stButton>button:hover{background:var(--border2)!important;border-color:var(--accent)!important;color:#fff!important;}
.stButton>button[kind="primary"]{background:var(--accent)!important;border-color:var(--accent)!important;color:#fff!important;}
.buy-btn .stButton>button{background:rgba(34,197,94,0.1)!important;border-color:var(--green)!important;color:var(--green)!important;font-weight:700!important;}
.buy-btn .stButton>button:hover{background:var(--green)!important;color:#000!important;}
.sell-btn .stButton>button{background:rgba(239,68,68,0.1)!important;border-color:var(--red)!important;color:var(--red)!important;font-weight:700!important;}
.sell-btn .stButton>button:hover{background:var(--red)!important;color:#fff!important;}

/* DataFrames */
.stDataFrame{border:1px solid var(--border)!important;border-radius:3px!important;}
.stDataFrame th{background:var(--bg2)!important;font-family:var(--mono)!important;font-size:0.65rem!important;text-transform:uppercase!important;letter-spacing:0.06em!important;color:var(--text2)!important;}
.stDataFrame td{font-family:var(--mono)!important;font-size:0.75rem!important;background:var(--bg)!important;}
.stExpander{border:1px solid var(--border)!important;border-radius:3px!important;}
.stExpander summary{font-family:var(--mono)!important;font-size:0.78rem!important;color:var(--text)!important;}
hr{border-color:var(--border)!important;margin:0.4rem 0!important;}

/* Live dot */
.ldot{display:inline-block;width:6px;height:6px;border-radius:50%;vertical-align:middle;margin-right:4px;}
.ldot.green{background:var(--green);animation:pulse 1.5s infinite;}
.ldot.red{background:var(--red);}
.ldot.yellow{background:var(--yellow);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.25;}}

/* Panel */
.panel{background:var(--bg2);border:1px solid var(--border);border-radius:3px;overflow:hidden;margin-bottom:0.5rem;}
.ph{background:var(--bg3);border-bottom:1px solid var(--border);padding:0.38rem 0.75rem;font-family:var(--mono);font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--text2);}
.ob-row{display:flex;justify-content:space-between;padding:0.22rem 0.75rem;font-family:var(--mono);font-size:0.72rem;}
.ob-row.hd{color:var(--text2);font-size:0.6rem;text-transform:uppercase;letter-spacing:0.06em;border-bottom:1px solid var(--border);}
.mrow{display:flex;justify-content:space-between;align-items:center;padding:0.28rem 0.75rem;border-bottom:1px solid var(--border);font-family:var(--mono);font-size:0.72rem;}
.mrow:hover{background:var(--bg3);}
.mrow:last-child{border-bottom:none;}

/* Prediction */
.pred{border-radius:3px;padding:0.6rem 0.75rem;text-align:center;font-family:var(--mono);}
.pred.up{background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25);}
.pred.dn{background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);}
.pred.hl{background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);}

/* AI box */
.aibox{border-radius:3px;padding:0.75rem 1rem;font-family:var(--sans);font-size:0.8rem;line-height:1.6;color:var(--text);margin:0.5rem 0;}
.aibox.std{background:#0d1420;border:1px solid #1e3a5f;border-left:3px solid var(--accent);}
.aibox.beg{background:#071a0d;border:1px solid #14532d;border-left:3px solid var(--green);}
.aibox.fps{background:#140a00;border:1px solid #7c2d0a;border-left:3px solid var(--yellow);}
.aitag{font-family:var(--mono);font-size:0.6rem;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.5rem;}
.aitag.std{color:var(--accent);}
.aitag.beg{color:var(--green);}
.aitag.fps{color:var(--yellow);}

/* News styles */
.masthead{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;color:var(--text);letter-spacing:-0.02em;border-bottom:3px double var(--border2);padding-bottom:0.5rem;margin-bottom:0.8rem;}
.datebar{font-family:var(--mono);font-size:0.65rem;color:var(--text2);text-transform:uppercase;letter-spacing:0.1em;border-bottom:1px solid var(--border);padding-bottom:0.35rem;margin-bottom:0.8rem;}
.ncard{background:var(--bg2);border:1px solid var(--border);border-radius:3px;overflow:hidden;margin-bottom:0.8rem;transition:border-color 0.2s;}
.ncard:hover{border-color:var(--border3);}
.nbody{padding:0.85rem;}
.ncat{font-family:var(--mono);font-size:0.6rem;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.35rem;}
.cat-markets{color:var(--accent);}
.cat-asx{color:var(--yellow);}
.cat-economy{color:var(--green);}
.cat-tech{color:var(--cyan);}
.cat-world{color:var(--purple);}
.nhl-lg{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:var(--text);line-height:1.35;margin-bottom:0.45rem;cursor:pointer;}
.nhl-lg:hover{color:var(--accent);}
.nhl-sm{font-family:'Playfair Display',serif;font-size:0.9rem;font-weight:700;color:var(--text);line-height:1.35;margin-bottom:0.3rem;cursor:pointer;}
.nhl-sm:hover{color:var(--accent);}
.nsumm{font-family:var(--sans);font-size:0.78rem;color:var(--text2);line-height:1.55;margin-bottom:0.45rem;}
.nmeta{display:flex;gap:0.7rem;align-items:center;font-family:var(--mono);font-size:0.6rem;color:var(--text3);flex-wrap:wrap;}
.nsrc{color:var(--accent);}
.nlink{color:var(--accent);text-decoration:none;font-family:var(--mono);font-size:0.6rem;}
.nlink:hover{text-decoration:underline;}
.sbadge{display:inline-block;padding:1px 6px;border-radius:2px;font-family:var(--mono);font-size:0.58rem;text-transform:uppercase;letter-spacing:0.06em;}
.sb-bull{background:rgba(34,197,94,0.12);color:var(--green);}
.sb-bear{background:rgba(239,68,68,0.12);color:var(--red);}
.sb-neut{background:rgba(245,158,11,0.12);color:var(--yellow);}
.tc{font-family:var(--mono);font-size:0.58rem;background:var(--bg3);padding:1px 5px;border-radius:2px;color:var(--accent);}

/* sidebar nav */
.ns{font-family:var(--mono);font-size:0.58rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--text3);padding:0.7rem 1rem 0.25rem;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LANGUAGE MODES
# ─────────────────────────────────────────────
LANG_MODES = {
    "📊 Standard":               "standard",
    "🌱 Beginner (Plain English)":"beginner",
    "🎮 FPS Gamer Mode":         "fps",
}
def lm(): return st.session_state.get("lang_mode","standard")
def lt(s,b,f): return {"standard":s,"beginner":b,"fps":f}[lm()]

# ─────────────────────────────────────────────
# STOCK UNIVERSE
# ─────────────────────────────────────────────
FEATURED = {
    "🇺🇸 US ETFs":   {"SPY":"S&P 500","QQQ":"NASDAQ 100","DIA":"Dow Jones","IWM":"Russell 2000","VTI":"Total Mkt"},
    "🇦🇺 ASX ETFs":  {"VAS.AX":"Vanguard ASX300","STW.AX":"SPDR ASX200","IOZ.AX":"iShares ASX200","NDQ.AX":"BetaShares NDQ","A200.AX":"BetaShares A200"},
    "🇦🇺 ASX Stocks":{"BHP.AX":"BHP Group","CBA.AX":"Commonwealth Bank","CSL.AX":"CSL Ltd","WBC.AX":"Westpac","NAB.AX":"NAB","ANZ.AX":"ANZ","WES.AX":"Wesfarmers","WOW.AX":"Woolworths","MQG.AX":"Macquarie","RIO.AX":"Rio Tinto","FMG.AX":"Fortescue","TLS.AX":"Telstra","REA.AX":"REA Group","ALL.AX":"Aristocrat"},
    "🌐 Tech Giants":{"AAPL":"Apple","MSFT":"Microsoft","NVDA":"NVIDIA","GOOGL":"Alphabet","AMZN":"Amazon","META":"Meta","TSLA":"Tesla"},
    "⚡ Sectors":    {"XLK":"Tech","XLF":"Finance","XLE":"Energy","XLV":"Health","GLD":"Gold ETF","SLV":"Silver ETF"},
}

# ─────────────────────────────────────────────
# MARKET STATUS
# ─────────────────────────────────────────────
def market_status(ticker):
    utc = datetime.now(timezone.utc)
    if ".AX" in ticker:
        tz  = pytz.timezone("Australia/Sydney")
        loc = utc.astimezone(tz)
        wd  = loc.weekday(); h = loc.hour + loc.minute/60
        if wd>=5: return {"s":"closed","label":"ASX CLOSED — Weekend","dot":"red","tz":"AEST"}
        if 10<=h<16: return {"s":"open","label":"ASX OPEN","dot":"green","tz":"AEST"}
        if 9.5<=h<10: return {"s":"pre","label":"ASX PRE-OPEN","dot":"yellow","tz":"AEST"}
        return {"s":"closed","label":"ASX CLOSED","dot":"red","tz":"AEST"}
    else:
        tz  = pytz.timezone("America/New_York")
        loc = utc.astimezone(tz)
        wd  = loc.weekday(); h = loc.hour + loc.minute/60
        if wd>=5: return {"s":"closed","label":"NYSE CLOSED — Weekend","dot":"red","tz":"ET"}
        if 9.5<=h<16: return {"s":"open","label":"NYSE OPEN","dot":"green","tz":"ET"}
        if 4<=h<9.5:  return {"s":"pre","label":"PRE-MARKET","dot":"yellow","tz":"ET"}
        if 16<=h<20:  return {"s":"pre","label":"AFTER-HOURS","dot":"yellow","tz":"ET"}
        return {"s":"closed","label":"NYSE CLOSED","dot":"red","tz":"ET"}

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch(ticker,period="6mo"):
    try:
        df = yf.download(ticker,period=period,auto_adjust=True,progress=False)
        if df.empty: return pd.DataFrame()
        df.index = pd.to_datetime(df.index)
        if isinstance(df.columns,pd.MultiIndex): df.columns=df.columns.get_level_values(0)
        return df
    except: return pd.DataFrame()

@st.cache_data(ttl=120)
def price(ticker):
    try:
        h = yf.Ticker(ticker).history(period="2d")
        return float(h["Close"].iloc[-1]) if not h.empty else 0.0
    except: return 0.0

@st.cache_data(ttl=600)
def info(ticker):
    try:
        i = yf.Ticker(ticker).info
        return {"name":i.get("longName",ticker),"sector":i.get("sector","—"),
                "52h":i.get("fiftyTwoWeekHigh"),"52l":i.get("fiftyTwoWeekLow"),
                "pe":i.get("trailingPE"),"mc":i.get("marketCap",0),
                "cur":i.get("currency","USD"),"avol":i.get("averageVolume",0)}
    except: return {"name":ticker,"sector":"—","cur":"USD"}

@st.cache_data(ttl=300)
def movers():
    tks=["SPY","QQQ","AAPL","NVDA","TSLA","BHP.AX","CBA.AX","VAS.AX","GLD","META"]
    rows=[]
    for t in tks:
        try:
            h=yf.Ticker(t).history(period="2d")
            if len(h)>=2:
                p=float(h["Close"].iloc[-2]); l=float(h["Close"].iloc[-1])
                rows.append({"t":t,"l":l,"c":l-p,"p":(l-p)/p*100})
        except: pass
    return sorted(rows,key=lambda x:abs(x["p"]),reverse=True)

# ─────────────────────────────────────────────
# INDICATORS
# ─────────────────────────────────────────────
def rsi_calc(s,n=14):
    d=s.diff(); g=d.clip(lower=0).rolling(n).mean(); l=(-d.clip(upper=0)).rolling(n).mean()
    return 100-(100/(1+g/l.replace(0,np.nan)))

def indicators(df):
    if df.empty or len(df)<20: return df
    df=df.copy(); c=df["Close"].squeeze()
    df["S20"]=c.rolling(20).mean(); df["S50"]=c.rolling(50).mean()
    df["RSI"]=rsi_calc(c)
    vm=df["Volume"].squeeze().rolling(20).mean()
    df["VMA"]=vm; df["VR"]=df["Volume"].squeeze()/vm
    df["BBm"]=c.rolling(20).mean(); std=c.rolling(20).std()
    df["BBu"]=df["BBm"]+2*std; df["BBl"]=df["BBm"]-2*std
    return df

# ─────────────────────────────────────────────
# LOCAL PERSISTENCE — saves to ~/tradesim_data/
# ─────────────────────────────────────────────
DATA_DIR  = Path.home() / "tradesim_data"
SAVE_FILE = DATA_DIR / "portfolio.json"
LOG_FILE  = DATA_DIR / "trade_log.json"
SETTINGS_FILE = DATA_DIR / "settings.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_PORTFOLIO = {
    "cash":        10000.0,
    "portfolio":   {},
    "trades":      [],
    "daily":       0,
    "last_date":   None,
    "created_at":  datetime.now().isoformat(),
    "last_saved":  None,
}

DEFAULT_SETTINGS = {
    "lang_mode": "standard",
    "period":    "6mo",
    "sl":        5.0,
    "ticker":    "SPY",
    "news_cat":  "All",
}

def load_portfolio() -> dict:
    """Load portfolio from local JSON file. Returns defaults if not found."""
    try:
        if SAVE_FILE.exists():
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            # Ensure all keys present (handles upgrades)
            for k, v in DEFAULT_PORTFOLIO.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception as e:
        pass  # Fall through to defaults
    return DEFAULT_PORTFOLIO.copy()

def save_portfolio():
    """Persist current portfolio + trade history to disk."""
    try:
        data = {
            "cash":       st.session_state.cash,
            "portfolio":  st.session_state.portfolio,
            "trades":     st.session_state.trades,
            "daily":      st.session_state.daily,
            "last_date":  st.session_state.last_date,
            "created_at": st.session_state.get("created_at", datetime.now().isoformat()),
            "last_saved": datetime.now().isoformat(),
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        # Also write a full trade log CSV for easy export
        if st.session_state.trades:
            pd.DataFrame(st.session_state.trades).to_csv(
                DATA_DIR / "trade_log.csv", index=False
            )
    except Exception as e:
        st.warning(f"⚠️ Could not save data: {e}")

def load_settings() -> dict:
    """Load user preferences from disk."""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r") as f:
                s = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                if k not in s: s[k] = v
            return s
    except:
        pass
    return DEFAULT_SETTINGS.copy()

def save_settings():
    """Persist sidebar preferences to disk."""
    try:
        s = {
            "lang_mode": st.session_state.lang_mode,
            "period":    st.session_state.period,
            "sl":        st.session_state.sl,
            "ticker":    st.session_state.ticker,
            "news_cat":  st.session_state.news_cat,
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(s, f, indent=2)
    except:
        pass

def get_save_info() -> dict:
    """Return metadata about last save for display."""
    try:
        if SAVE_FILE.exists():
            stat = SAVE_FILE.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            size_kb = stat.st_size / 1024
            return {
                "exists": True,
                "path": str(SAVE_FILE),
                "last_saved": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                "size_kb": round(size_kb, 1),
            }
    except:
        pass
    return {"exists": False, "path": str(SAVE_FILE)}

# ─────────────────────────────────────────────
# SESSION STATE  (loads from disk on first run)
# ─────────────────────────────────────────────
def init():
    # Only load from disk once per browser session
    if "loaded_from_disk" not in st.session_state:
        saved   = load_portfolio()
        prefs   = load_settings()

        st.session_state.cash       = float(saved["cash"])
        st.session_state.portfolio  = saved["portfolio"]
        st.session_state.trades     = saved["trades"]
        st.session_state.daily      = int(saved.get("daily", 0))
        st.session_state.last_date  = saved.get("last_date")
        st.session_state.created_at = saved.get("created_at", datetime.now().isoformat())

        st.session_state.lang_mode  = prefs["lang_mode"]
        st.session_state.period     = prefs["period"]
        st.session_state.sl         = float(prefs["sl"])
        st.session_state.ticker     = prefs["ticker"]
        st.session_state.news_cat   = prefs["news_cat"]

        st.session_state.ai_exp         = ""
        st.session_state.loaded_from_disk = True

    # Non-persisted keys (safe defaults every refresh)
    for k, v in {"ai_exp": "", "news_cat": "All"}.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def pval():
    v=st.session_state.cash
    for t,p in st.session_state.portfolio.items(): v+=p["s"]*price(t)
    return v

def ppnl(ticker):
    if ticker not in st.session_state.portfolio: return 0.0,0.0
    p=st.session_state.portfolio[ticker]; pr=price(ticker)
    cost=p["s"]*p["a"]; val=p["s"]*pr; pnl=val-cost
    return pnl,(pnl/cost*100) if cost else 0

def check_sl():
    alerts=[]
    for t,pos in list(st.session_state.portfolio.items()):
        pr=price(t)
        if not pr: continue
        lp=(pr-pos["a"])/pos["a"]*100
        if lp<=-st.session_state.sl:
            proc=pos["s"]*pr; pnl=proc-pos["s"]*pos["a"]
            st.session_state.cash+=proc
            st.session_state.trades.append({"time":datetime.now().strftime("%H:%M"),"action":"STOP-LOSS","ticker":t,"shares":pos["s"],"price":pr,"pnl":pnl})
            del st.session_state.portfolio[t]
            alerts.append(lt(f"⛔ Stop-loss: {t} sold at ${pr:.2f} ({lp:.1f}%)",
                             f"🛑 Auto-sold {t}! Dropped {abs(lp):.1f}% below your buy price.",
                             f"💀 EXTRACT TRIGGERED — {t} eliminated at ${pr:.2f} ({lp:.1f}%)"))
    return alerts

# ─────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────
def predict(df):
    if df.empty or len(df)<20: return {"d":"HOLD","c":50,"r":[]}
    def sc(col): return float(df[col].iloc[-1]) if col in df.columns else None
    try:
        close=float(df["Close"].iloc[-1]); rsi=sc("RSI") or 50
        s20=sc("S20") or close; s50=sc("S50") or close
    except: return {"d":"HOLD","c":50,"r":[]}
    sigs=[]; reas=[]
    if rsi<35:
        sigs.append(1); reas.append(lt(f"RSI {rsi:.0f} — oversold (bullish)",f"RSI {rsi:.0f} — sold too much, may bounce up 🔁",f"RSI {rsi:.0f} — LOW HP, push opportunity 🩸"))
    elif rsi>65:
        sigs.append(-1); reas.append(lt(f"RSI {rsi:.0f} — overbought (bearish)",f"RSI {rsi:.0f} — bought too much, may drop ⚠️",f"RSI {rsi:.0f} — overextended, pullback likely 💥"))
    else:
        sigs.append(0); reas.append(lt(f"RSI {rsi:.0f} — neutral",f"RSI {rsi:.0f} — normal range",f"RSI {rsi:.0f} — even fight zone"))
    if close>s20>s50:
        sigs.append(1); reas.append(lt("Above SMA20 & SMA50 — uptrend","Price above both averages 📈","HIGH GROUND secured ⬆️"))
    elif close<s20<s50:
        sigs.append(-1); reas.append(lt("Below SMA20 & SMA50 — downtrend","Price below both averages 📉","LOW GROUND — bears dominate ⬇️"))
    else:
        sigs.append(0); reas.append(lt("Mixed MA signals","Averages are mixed","Contested zone — no clear angle"))
    if len(df)>=5:
        cs=df["Close"].squeeze(); mom=float(cs.iloc[-1])/float(cs.iloc[-5])-1
        if mom>0.02: sigs.append(1); reas.append(lt(f"+{mom*100:.1f}% momentum",f"Up {mom*100:.1f}% this week 🚀",f"KILLSTREAK +{mom*100:.1f}% 🔥"))
        elif mom<-0.02: sigs.append(-1); reas.append(lt(f"{mom*100:.1f}% momentum",f"Down {abs(mom*100):.1f}% this week 😬",f"TILTED {mom*100:.1f}% 💀"))
        else: sigs.append(0); reas.append(lt(f"Flat {mom*100:.1f}%",f"Barely moved ({mom*100:.1f}%)",f"Ghost lobby ({mom*100:.1f}%)"))
    score=sum(sigs); d="UP" if score>0 else ("DOWN" if score<0 else "HOLD")
    return {"d":d,"c":min(90,55+abs(score)*12) if score else 50,"r":reas}

# ─────────────────────────────────────────────
# AI EXPLANATION
# ─────────────────────────────────────────────
def explain(ticker,action,shares,cp,df,pnl=0.0):
    m=lm(); cur="AUD" if ".AX" in ticker else "USD"; val=shares*cp; parts=[]
    if m=="standard": parts.append(f"**Trade:** {'Bought' if action=='BUY' else 'Sold'} {shares:.2f} × {ticker} @ ${cp:.2f} {cur} = ${val:.2f}")
    elif m=="beginner": parts.append(f"**What you did:** You {'bought' if action=='BUY' else 'sold'} {shares:.2f} shares of **{ticker}** for ${cp:.2f} each. Total: **${val:.2f}**. Each share is like one pizza slice 🍕 — you just {'added' if action=='BUY' else 'sold'} {shares:.2f} slices.")
    else: parts.append(f"**ENGAGEMENT LOG:** {action} {shares:.2f}× {ticker} @ ${cp:.2f} — Ammo deployed: **${val:.2f}**")
    if df.empty or len(df)<20: return "\n\n".join(parts)
    def sc(col): return float(df[col].iloc[-1]) if col in df.columns else None
    rsi=sc("RSI"); s20=sc("S20"); s50=sc("S50"); vr=sc("VR"); close=float(df["Close"].iloc[-1])
    if rsi:
        if m=="standard":
            if rsi<30: parts.append(f"**RSI {rsi:.0f}** — oversold territory. Like a rubber band stretched down — often bounces. Buying here can be smart.")
            elif rsi>70: parts.append(f"**RSI {rsi:.0f}** — overbought. Pullback risk is elevated. Selling or waiting may be safer.")
            else: parts.append(f"**RSI {rsi:.0f}** — neutral zone (30–70). No extreme signal. Normal conditions.")
        elif m=="beginner":
            if rsi<30: parts.append(f"🌡️ **RSI is {rsi:.0f} — very LOW.** Like a trampoline pushed way down — it often springs back up. Could be a good time to buy!")
            elif rsi>70: parts.append(f"🌡️ **RSI is {rsi:.0f} — very HIGH.** Like a balloon blown up too much. Risky to buy right now — it might come back down.")
            else: parts.append(f"🌡️ **RSI is {rsi:.0f} — normal range.** Nothing extreme. The stock is just doing its usual thing.")
        else:
            if rsi<30: parts.append(f"🩸 **RSI {rsi:.0f} — ENEMY AT LOW HP.** Prime push window. High kill potential.")
            elif rsi>70: parts.append(f"⚡ **RSI {rsi:.0f} — TARGET OVERPOWERED.** Don't chase. Wait for the pullback then re-engage.")
            else: parts.append(f"🎯 **RSI {rsi:.0f} — EVEN MATCH.** No HP advantage. Read the map first.")
    if s20 and s50:
        if m=="standard":
            if close>s20>s50: parts.append("**Trend:** Bullish — price above SMA20 & SMA50. Uptrend confirmed.")
            elif close<s20<s50: parts.append("**Trend:** Bearish — price below both moving averages. Downtrend active.")
            else: parts.append("**Trend:** Mixed — no clear directional bias from moving averages.")
        elif m=="beginner":
            if close>s20>s50: parts.append(f"📈 **Trend is UP!** Price (${close:.2f}) is above both averages. Like swimming with the current — easier to make money buying.")
            elif close<s20<s50: parts.append(f"📉 **Trend is DOWN.** Price (${close:.2f}) is below both averages. Swimming against the current — harder to make money buying right now.")
            else: parts.append("🤔 **Trend is MIXED.** Averages are conflicting — wait for a clearer signal.")
        else:
            if close>s20>s50: parts.append(f"🏔️ **HIGH GROUND SECURED.** Price ${close:.2f} above both lines. Bulls own the map. Push the objective.")
            elif close<s20<s50: parts.append(f"💀 **LOSING POSITION.** Price ${close:.2f} below both defense lines. Bears in control. Consider extracting.")
            else: parts.append(f"⚔️ **CONTESTED ZONE.** Price fighting between SMA20 (${s20:.2f}) and SMA50 (${s50:.2f}). Wait for a side to break.")
    if vr:
        if vr>1.5: parts.append(lt(f"**Volume {vr:.1f}×** — strong participation, move is confirmed",f"📊 **{vr:.1f}× normal trading volume!** More people trading = more trustworthy move.",f"👥 **FULL SQUAD — {vr:.1f}× volume.** High-pop lobby. This move is real."))
        elif vr<0.6: parts.append(lt(f"**Volume {vr:.1f}×** — low participation, treat with caution",f"😴 **Low volume ({vr:.1f}× normal).** Not many people trading — move might be a fake-out.",f"👻 **GHOST LOBBY — {vr:.1f}× volume.** Don't over-commit on low-pop plays."))
    if action=="SELL" and pnl!=0:
        if m=="standard": parts.append(f"**P&L: {'+'if pnl>=0 else ''}${pnl:.2f}** — {'profit secured ✅' if pnl>0 else 'loss absorbed — stop-losses exist for this 📉'}")
        elif m=="beginner":
            if pnl>0: parts.append(f"🎉 **You made ${pnl:.2f} profit!** You sold for more than you paid. That's exactly what trading is about!")
            else: parts.append(f"😓 **You lost ${abs(pnl):.2f}.** That's okay — every trader has losses. Key is keeping them small and learning why.")
        else:
            if pnl>0: parts.append(f"💰 **+${pnl:.2f} BOUNTY COLLECTED.** Bag secured. GG EZ.")
            else: parts.append(f"💀 **-${abs(pnl):.2f} ELIMINATED.** Review kill cam. Respawn ready.")
    tips={"standard":["💡 Never invest what you can't afford to lose","💡 Diversify — don't all-in one ticker","💡 Trade with the trend, not against it","💡 High volume confirms price moves","💡 Stop-losses protect capital — always set one"],
          "beginner":["🌱 Only use money you're okay losing. Learn here first!","🌱 Think of your portfolio like a garden — plant in different spots!","🌱 Buy low, sell high — simple idea, takes lots of practice","🌱 A stop-loss is your safety net — set it to protect yourself","🌱 The S&P 500 (SPY) has averaged ~10%/year over 100 years. Patience wins!"],
          "fps":["🎮 Don't YOLO your full bankroll on one play — noob move","🎮 Stop-loss = respawn insurance. No stop = permadeath mode","🎮 Follow the meta (trend). Fight the meta = hard mode","🎮 Even pros only win 55-60% of trades. Win rate > 50% = profit","🎮 ETFs = squad bundles. Less risky than solo-queuing single stocks"]}
    parts.append(random.choice(tips[lm()]))
    return "\n\n".join(parts)

# ─────────────────────────────────────────────
# NEWS ARTICLES  (curated with real source URLs)
# ─────────────────────────────────────────────
ARTICLES = [
    {"id":1,"cat":"Markets","cls":"cat-markets","hl":"S&P 500 Extends Rally as Fed Signals Rate Path Clarity",
     "summ":"US equity markets climbed for a fourth consecutive session Thursday, with the S&P 500 touching a fresh six-week high as Federal Reserve officials signalled growing confidence that inflation is trending toward the 2% target, reducing urgency of further rate hikes.",
     "src":"Reuters","url":"https://www.reuters.com/markets/","time":"2h ago","sent":"bull","tks":["SPY","QQQ"],"feat":True},
    {"id":2,"cat":"ASX","cls":"cat-asx","hl":"BHP and Rio Tinto Surge as Iron Ore Recovers on China Stimulus Bets",
     "summ":"Australian mining giants BHP Group and Rio Tinto both gained more than 2% as iron ore futures in Singapore rose above US$110/tonne, driven by speculation that Beijing will announce additional infrastructure stimulus before year end.",
     "src":"AFR","url":"https://www.afr.com/markets","time":"1h ago","sent":"bull","tks":["BHP.AX","RIO.AX","VAS.AX"],"feat":True},
    {"id":3,"cat":"Tech","cls":"cat-tech","hl":"NVIDIA Smashes Estimates — Data Centre Revenue Triples Year-on-Year",
     "summ":"NVIDIA reported quarterly data centre revenue of $22.6 billion, nearly tripling the year-ago figure. CEO Jensen Huang said demand for Blackwell AI chips remains significantly ahead of supply, with the order backlog stretching into next year.",
     "src":"CNBC","url":"https://www.cnbc.com/technology/","time":"3h ago","sent":"bull","tks":["NVDA","QQQ","XLK"],"feat":True},
    {"id":4,"cat":"Markets","cls":"cat-markets","hl":"Treasury Yields Edge Lower as Inflation Data Comes In Mixed",
     "summ":"The 10-year Treasury yield fell three basis points after the latest CPI reading showed headline inflation declining while core services remained sticky, leaving markets uncertain about the timing of rate cuts.",
     "src":"Bloomberg","url":"https://www.bloomberg.com/markets","time":"4h ago","sent":"neut","tks":["SPY","GLD"],"feat":False},
    {"id":5,"cat":"ASX","cls":"cat-asx","hl":"RBA Holds Cash Rate at 4.35% — Markets Bet on Mid-Year Cut",
     "summ":"The Reserve Bank of Australia left its benchmark cash rate unchanged. Governor Michele Bullock reiterated vigilance on inflation, though swap markets are now pricing a 70% probability of a cut by June.",
     "src":"SMH","url":"https://www.smh.com.au/business/markets","time":"Yesterday","sent":"neut","tks":["VAS.AX","CBA.AX","STW.AX"],"feat":False},
    {"id":6,"cat":"Tech","cls":"cat-tech","hl":"Apple Unveils AI-Powered Mac Lineup Ahead of Holiday Season",
     "summ":"Apple introduced updated MacBook Pro and Mac Mini models powered by the new M4 chip family, delivering up to 3× faster neural engine performance for on-device AI tasks. Analysts expect a strong upgrade cycle heading into the festive quarter.",
     "src":"The Verge","url":"https://www.theverge.com/apple","time":"5h ago","sent":"bull","tks":["AAPL","QQQ"],"feat":False},
    {"id":7,"cat":"Economy","cls":"cat-economy","hl":"US Jobs Report Shows Labour Market Cooling But Remaining Resilient",
     "summ":"Non-farm payrolls rose 187,000 in October, below the 200,000 consensus. Unemployment ticked to 3.9%. Wage growth eased to 4.1% year-on-year — data the Federal Reserve will view as progress without triggering recession fears.",
     "src":"WSJ","url":"https://www.wsj.com/economy","time":"6h ago","sent":"neut","tks":["SPY","DIA","XLF"],"feat":False},
    {"id":8,"cat":"Economy","cls":"cat-economy","hl":"Australian CPI Falls to 3.4% — Lowest Since Late 2021",
     "summ":"Australia's headline CPI slowed to 3.4% in the September quarter, giving the RBA greater comfort to hold and eventually cut interest rates. Housing and energy remain the key upside risks.",
     "src":"ABC Business","url":"https://www.abc.net.au/news/business","time":"Yesterday","sent":"bull","tks":["VAS.AX","A200.AX","CBA.AX"],"feat":False},
    {"id":9,"cat":"Markets","cls":"cat-markets","hl":"Gold Hits $2,400 as Dollar Weakens and Geopolitical Risk Rises",
     "summ":"Spot gold surged to $2,400/troy oz as the US dollar index fell to its lowest since August and investors sought safe-haven assets amid escalating Middle East tensions and US election uncertainty.",
     "src":"FT","url":"https://www.ft.com/markets","time":"30m ago","sent":"bull","tks":["GLD","SLV"],"feat":False},
    {"id":10,"cat":"World","cls":"cat-world","hl":"China Manufacturing PMI Returns to Expansion — Asia Stocks Rally",
     "summ":"China's official manufacturing PMI rose to 50.1 in October, the first expansion reading in six months, fuelling gains across Asian markets. The ASX 200 added 0.8%, led by materials and energy stocks.",
     "src":"Reuters","url":"https://www.reuters.com/world/china/","time":"8h ago","sent":"bull","tks":["BHP.AX","FMG.AX","VAS.AX"],"feat":False},
    {"id":11,"cat":"Tech","cls":"cat-tech","hl":"Tesla Deliveries Miss Wall Street Targets — Stock Falls 6% After-Hours",
     "summ":"Tesla delivered 462,890 vehicles in Q3 2024, short of the 469,000 consensus estimate. CEO Elon Musk said the company will detail cost reduction and new models on the upcoming earnings call.",
     "src":"CNBC","url":"https://www.cnbc.com/tesla/","time":"Yesterday","sent":"bear","tks":["TSLA","QQQ"],"feat":False},
    {"id":12,"cat":"ASX","cls":"cat-asx","hl":"Commonwealth Bank FY24 Cash Profit +3% — Special Dividend Announced",
     "summ":"CBA reported full-year cash profit of $10.2 billion, up 3%, and announced a special dividend of 60 cents per share. Strong mortgage growth and disciplined cost management were cited as key drivers.",
     "src":"AFR","url":"https://www.afr.com/companies/financial-services","time":"2 days ago","sent":"bull","tks":["CBA.AX","VAS.AX"],"feat":False},
]

def get_news(ticker):
    is_asx=".AX" in ticker
    if is_asx:
        pri=[a for a in ARTICLES if any(t.endswith(".AX") for t in a["tks"])]
        rest=[a for a in ARTICLES if a not in pri]
        return pri+rest
    if ticker in ["SPY","QQQ","DIA","IWM","VTI"]: return ARTICLES
    filt=[a for a in ARTICLES if ticker in a["tks"]]+[a for a in ARTICLES if ticker not in a["tks"]]
    return filt

# ─────────────────────────────────────────────
# BACKTEST
# ─────────────────────────────────────────────
def backtest(ticker,years=2):
    df=fetch(ticker,f"{years}y")
    if df.empty or len(df)<60: return {}
    df=indicators(df); df=df.dropna(subset=["S20","S50"])
    cash=10000.0; shares=avg=0.0; equity=[]; trades=[]
    cl=df["Close"].squeeze(); s20=df["S20"].squeeze(); s50=df["S50"].squeeze()
    for i in range(1,len(df)):
        p=float(cl.iloc[i]); ps20=float(s20.iloc[i-1]); ps50=float(s50.iloc[i-1])
        cs20=float(s20.iloc[i]); cs50=float(s50.iloc[i])
        if ps20<=ps50 and cs20>cs50 and shares==0 and cash>p:
            shares=cash/p; avg=p; cash=0; trades.append({"type":"BUY","price":p,"date":str(df.index[i].date())})
        elif ps20>=ps50 and cs20<cs50 and shares>0:
            pnl=shares*(p-avg); cash=shares*p; trades.append({"type":"SELL","price":p,"date":str(df.index[i].date()),"pnl":pnl}); shares=avg=0
        equity.append({"date":str(df.index[i].date()),"value":round(cash+shares*p,2)})
    if shares>0: cash=shares*float(cl.iloc[-1])
    sells=[t for t in trades if t["type"]=="SELL"]; wins=[t for t in sells if t.get("pnl",0)>0]
    return {"eq":equity,"trades":trades,"wr":round(len(wins)/len(sells)*100,1) if sells else 0,
            "ret":round((cash-10000)/10000*100,1),"nt":len(sells),
            "best":max([t.get("pnl",0) for t in trades],default=0),
            "worst":min([t.get("pnl",0) for t in trades],default=0),"fv":round(cash,2)}

# ─────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────
def chart_price(df,ticker):
    if df.empty: return go.Figure()
    c=df["Close"].squeeze(); fig=go.Figure()
    if all(x in df.columns for x in ["Open","High","Low"]):
        fig.add_trace(go.Candlestick(x=df.index,open=df["Open"].squeeze(),high=df["High"].squeeze(),
            low=df["Low"].squeeze(),close=c,name=ticker,
            increasing=dict(line=dict(color="#22c55e",width=1),fillcolor="#22c55e"),
            decreasing=dict(line=dict(color="#ef4444",width=1),fillcolor="#ef4444")))
    else:
        fig.add_trace(go.Scatter(x=df.index,y=c,line=dict(color="#3b82f6",width=1.5),name=ticker))
    if "S20" in df.columns: fig.add_trace(go.Scatter(x=df.index,y=df["S20"].squeeze(),name="SMA20",line=dict(color="#f59e0b",width=1,dash="dot"),opacity=0.8))
    if "S50" in df.columns: fig.add_trace(go.Scatter(x=df.index,y=df["S50"].squeeze(),name="SMA50",line=dict(color="#8b5cf6",width=1,dash="dot"),opacity=0.8))
    if "BBu" in df.columns:
        fig.add_trace(go.Scatter(x=df.index,y=df["BBu"].squeeze(),line=dict(color="#374151",width=0.8),showlegend=False,name="BB"))
        fig.add_trace(go.Scatter(x=df.index,y=df["BBl"].squeeze(),line=dict(color="#374151",width=0.8),fill="tonexty",fillcolor="rgba(55,65,81,0.08)",showlegend=False,name="BB"))
    fig.update_layout(template="plotly_dark",paper_bgcolor="#111519",plot_bgcolor="#0b0e11",
        margin=dict(l=6,r=6,t=6,b=6),height=320,
        xaxis=dict(gridcolor="#1e2530",rangeslider_visible=False,tickfont=dict(family="IBM Plex Mono",size=9,color="#8892a4")),
        yaxis=dict(gridcolor="#1e2530",side="right",tickfont=dict(family="IBM Plex Mono",size=9,color="#8892a4")),
        legend=dict(orientation="h",yanchor="bottom",y=1.01,bgcolor="rgba(0,0,0,0)",font=dict(family="IBM Plex Mono",size=9,color="#8892a4")),
        xaxis_rangeslider_visible=False)
    return fig

def chart_rsi(df):
    if "RSI" not in df.columns: return go.Figure()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df.index,y=df["RSI"].squeeze(),line=dict(color="#06b6d4",width=1.5),name="RSI"))
    fig.add_hrect(y0=70,y1=100,fillcolor="rgba(239,68,68,0.04)",line_width=0)
    fig.add_hrect(y0=0,y1=30,fillcolor="rgba(34,197,94,0.04)",line_width=0)
    fig.add_hline(y=70,line_color="#ef4444",line_width=0.7,line_dash="dash")
    fig.add_hline(y=30,line_color="#22c55e",line_width=0.7,line_dash="dash")
    fig.update_layout(template="plotly_dark",paper_bgcolor="#111519",plot_bgcolor="#0b0e11",
        height=100,margin=dict(l=6,r=6,t=4,b=4),showlegend=False,
        yaxis=dict(range=[0,100],gridcolor="#1e2530",side="right",tickfont=dict(family="IBM Plex Mono",size=8,color="#8892a4")),
        xaxis=dict(gridcolor="#1e2530",showticklabels=False))
    return fig

def chart_vol(df):
    if "Volume" not in df.columns: return go.Figure()
    vol=df["Volume"].squeeze(); cl=df["Close"].squeeze()
    cols=["#22c55e" if float(cl.iloc[i])>=float(cl.iloc[i-1]) else "#ef4444" for i in range(len(cl))]
    fig=go.Figure()
    fig.add_trace(go.Bar(x=df.index,y=vol,marker_color=cols,name="Vol",opacity=0.65))
    if "VMA" in df.columns: fig.add_trace(go.Scatter(x=df.index,y=df["VMA"].squeeze(),line=dict(color="#f59e0b",width=1),name="Vol MA"))
    fig.update_layout(template="plotly_dark",paper_bgcolor="#111519",plot_bgcolor="#0b0e11",
        height=80,margin=dict(l=6,r=6,t=4,b=4),showlegend=False,bargap=0.1,
        yaxis=dict(gridcolor="#1e2530",side="right",tickfont=dict(family="IBM Plex Mono",size=8,color="#8892a4")),
        xaxis=dict(gridcolor="#1e2530",showticklabels=False))
    return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.85rem 1rem 0.6rem;border-bottom:1px solid #1e2530;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.95rem;font-weight:700;color:#fff;letter-spacing:0.04em;">
        <span style="color:#3b82f6;">▲</span> TradeSim
      </div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:#4b5563;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px;">Pro Terminal · v2.0</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="ns">Knowledge Mode</div>', unsafe_allow_html=True)
    lc = st.radio("lm", list(LANG_MODES.keys()),
                  index=list(LANG_MODES.values()).index(st.session_state.lang_mode),
                  label_visibility="collapsed")
    nm = LANG_MODES[lc]
    if nm != st.session_state.lang_mode:
        st.session_state.lang_mode = nm
        save_settings()
        st.rerun()

    st.markdown('<div class="ns" style="margin-top:0.6rem;">Market / Stock</div>', unsafe_allow_html=True)
    cat = st.selectbox("Cat", list(FEATURED.keys()), label_visibility="collapsed")
    stks = FEATURED[cat]; tks=list(stks.keys()); tlbls=[f"{t} — {n}" for t,n in stks.items()]
    si = st.selectbox("Stk", range(len(tks)), format_func=lambda i:tlbls[i], label_visibility="collapsed")
    sel = tks[si]; st.session_state.ticker = sel

    cust = st.text_input("", "", placeholder="Custom ticker (e.g. BHP.AX)", label_visibility="collapsed")
    if cust.strip(): sel=cust.strip().upper(); st.session_state.ticker=sel

    st.markdown('<div class="ns">Chart Period</div>', unsafe_allow_html=True)
    new_period = st.select_slider("P", ["1mo","3mo","6mo","1y","2y"],
                                  value=st.session_state.period, label_visibility="collapsed")
    if new_period != st.session_state.period:
        st.session_state.period = new_period
        save_settings()

    st.markdown('<div class="ns">Risk Settings</div>', unsafe_allow_html=True)
    new_sl = st.slider("SL", 2, 20, int(st.session_state.sl), label_visibility="collapsed")
    if new_sl != st.session_state.sl:
        st.session_state.sl = new_sl
        save_settings()
    st.caption(f"Stop-loss: {st.session_state.sl}% below entry")

    st.markdown('<div class="ns">Account</div>', unsafe_allow_html=True)
    pv=pval(); pnl_tot=pv-10000; pc="#22c55e" if pnl_tot>=0 else "#ef4444"
    st.markdown(f"""
    <div style="padding:0.55rem 1rem;font-family:'IBM Plex Mono',monospace;border-bottom:1px solid #1e2530;">
      <div style="color:#8892a4;font-size:0.58rem;text-transform:uppercase;letter-spacing:0.08em;">Portfolio</div>
      <div style="color:#fff;font-size:0.95rem;font-weight:700;margin:2px 0;">${pv:,.2f}</div>
      <div style="color:{pc};font-size:0.68rem;">{'▲' if pnl_tot>=0 else '▼'} ${abs(pnl_tot):,.2f} ({pnl_tot/100:+.1f}%)</div>
      <div style="color:#4b5563;font-size:0.62rem;margin-top:3px;">Cash: ${st.session_state.cash:,.2f}</div>
    </div>""", unsafe_allow_html=True)

    if st.button(lt("↺  Reset Game","↺  Start Fresh","💀 RESPAWN"), use_container_width=True):
        st.session_state.cash=10000.0; st.session_state.portfolio={}
        st.session_state.trades=[]; st.session_state.ai_exp=""
        st.session_state.daily=0; st.session_state.created_at=datetime.now().isoformat()
        save_portfolio()
        st.rerun()

    # ── Save status indicator ──────────────────
    si_info = get_save_info()
    if si_info["exists"]:
        st.markdown(f"""
        <div style="padding:0.4rem 1rem;font-family:'IBM Plex Mono',monospace;font-size:0.58rem;
                    color:#4b5563;border-top:1px solid #1e2530;line-height:1.7;">
          <span class="ldot green" style="width:5px;height:5px;"></span>
          <span style="color:#22c55e;">Saved locally</span><br>
          {si_info['last_saved']}<br>
          <span style="color:#374151;">{si_info['path']}</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="padding:0.4rem 1rem;font-family:'IBM Plex Mono',monospace;font-size:0.58rem;
                    color:#4b5563;border-top:1px solid #1e2530;">
          <span class="ldot yellow"></span> No save file yet<br>
          <span style="color:#374151;">Will save on first trade</span>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
m=lm()
TL={"standard":["📊  Trade","💼  Portfolio","📰  News & Reports","🔬  Backtest","📚  Learn"],
    "beginner": ["📊  Trade","💼  My Money","📰  News","🔬  Time Machine","📚  What's it Mean?"],
    "fps":      ["🔫  ENGAGE","🎒  LOADOUT","📡  SITREP","🎬  REPLAY","📖  FIELD MANUAL"]}
tabs=st.tabs(TL[m])

# ══════════════════════════════════════════════
# TAB 0 — TRADE
# ══════════════════════════════════════════════
with tabs[0]:
    ticker=st.session_state.ticker
    ms=market_status(ticker)
    dot_col={"open":"green","pre":"yellow","closed":"red"}[ms["s"]]
    status_col={"open":"#22c55e","pre":"#f59e0b","closed":"#ef4444"}[ms["s"]]

    # Terminal bar
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:1.2rem;padding:0.38rem 1rem;
                background:#111519;border-bottom:1px solid #1e2530;">
      <span style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;">
        <span class="ldot {dot_col}"></span>
        <span style="color:{status_col};">{ms['label']}</span>
        <span style="color:#4b5563;margin-left:6px;">{ms['tz']}</span>
      </span>
      <span style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;margin-left:auto;">
        <span class="ldot green"></span><span style="color:#22c55e;">LIVE</span>
        <span style="color:#4b5563;margin-left:4px;">Yahoo Finance</span>
      </span>
      <span style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:#4b5563;">
        {datetime.now().strftime("%H:%M:%S")}
      </span>
    </div>""", unsafe_allow_html=True)

    with st.spinner(f"Fetching {ticker}…"):
        df0=fetch(ticker, st.session_state.period)
        df=indicators(df0) if not df0.empty else df0

    if df.empty:
        st.error(lt(f"No data for {ticker}. Check ticker — ASX stocks need .AX suffix.",
                    f"Couldn't find {ticker}. Australian stocks need '.AX' at the end (e.g. BHP.AX).",
                    f"TARGET NOT FOUND: {ticker}. Bad callout — verify ticker."))
    else:
        nfo=info(ticker); cs=df["Close"].squeeze()
        cp=float(cs.iloc[-1]); pp=float(cs.iloc[-2]) if len(cs)>1 else cp
        chg=cp-pp; pct=chg/pp*100; cur="AUD" if ".AX" in ticker else "USD"
        cc="#22c55e" if chg>=0 else "#ef4444"; sym="▲" if chg>=0 else "▼"

        # Price strip
        st.markdown(f"""
        <div style="display:flex;align-items:baseline;gap:0.9rem;padding:0.5rem 1rem 0.35rem;
                    background:#111519;border-bottom:1px solid #1e2530;">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:#8892a4;font-weight:600;">{ticker}</span>
          <span style="font-family:'IBM Plex Mono',monospace;font-size:1.35rem;font-weight:700;color:#fff;">${cp:.2f}</span>
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.82rem;color:{cc};font-weight:600;">{sym} {abs(chg):.2f} ({pct:+.2f}%)</span>
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:#4b5563;margin-left:auto;">{cur} · {nfo.get('sector','—')}</span>
        </div>""", unsafe_allow_html=True)

        col_c, col_r = st.columns([3,1], gap="small")

        with col_c:
            st.plotly_chart(chart_price(df,ticker), use_container_width=True, config={"displayModeBar":False})
            st.plotly_chart(chart_rsi(df), use_container_width=True, config={"displayModeBar":False})
            st.plotly_chart(chart_vol(df), use_container_width=True, config={"displayModeBar":False})

        with col_r:
            # Stats
            def sc(col): return float(df[col].iloc[-1]) if col in df.columns else None
            rv=sc("RSI"); s2=sc("S20"); s5=sc("S50"); vr=sc("VR")
            rc="#22c55e" if (rv and rv<40) else ("#ef4444" if (rv and rv>60) else "#d1d5db")
            def row(l,v,c="#d1d5db"):
                return f'<div class="ob-row"><span style="color:#8892a4;">{l}</span><span style="color:{c};font-weight:600;">{v}</span></div>'
            st.markdown(f"""
            <div class="panel">
              <div class="ph">{lt("Stats","Key Numbers","INTEL STATS")}</div>
              {row("RSI(14)", f"{rv:.1f}" if rv else "—", rc)}
              {row("SMA20",  f"${s2:.2f}" if s2 else "—")}
              {row("SMA50",  f"${s5:.2f}" if s5 else "—")}
              {row("Vol×",   f"{vr:.2f}×" if vr else "—", "#f59e0b" if (vr and vr>1.5) else "#d1d5db")}
              {row("52W H",  f"${nfo['52h']:.2f}" if nfo.get('52h') else "—")}
              {row("52W L",  f"${nfo['52l']:.2f}" if nfo.get('52l') else "—")}
            </div>""", unsafe_allow_html=True)

            # Prediction
            pred=predict(df); d=pred["d"]
            pcls={"UP":"up","DOWN":"dn","HOLD":"hl"}[d]
            pcol={"UP":"#22c55e","DOWN":"#ef4444","HOLD":"#f59e0b"}[d]
            psym={"UP":"▲","DOWN":"▼","HOLD":"—"}[d]
            plbl=lt(d,{"UP":"GOING UP","DOWN":"GOING DOWN","HOLD":"UNSURE"}[d],{"UP":"ADVANCE","DOWN":"RETREAT","HOLD":"HOLD"}[d])
            st.markdown(f"""
            <div class="panel">
              <div class="ph">{lt("AI Prediction","Tomorrow?","INTEL REPORT")}</div>
              <div class="pred {pcls}">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:{pcol};">{psym} {plbl}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:#8892a4;margin-top:3px;">{lt("Confidence","How sure","ACCURACY")}: {pred['c']}%</div>
              </div>
              <div style="padding:0.3rem 0.5rem;">""", unsafe_allow_html=True)
            for r in pred["r"]:
                st.markdown(f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.6rem;color:#8892a4;padding:1px 0.25rem;">• {r}</div>', unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

            # Order entry
            st.markdown(f'<div class="panel"><div class="ph">{lt("Order Entry","Buy / Sell","DEPLOY CAPITAL")}</div><div style="padding:0.5rem;">', unsafe_allow_html=True)
            maxsh=st.session_state.cash/cp if cp else 0
            sh=st.number_input(lt(f"Shares (max {maxsh:.2f})",f"# shares (up to {maxsh:.2f})",f"Units (max {maxsh:.2f})"),
                               min_value=0.01,max_value=max(0.01,maxsh*2),value=min(1.0,maxsh),step=0.1,format="%.2f")
            tv=sh*cp; st.caption(f"Value: **${tv:.2f} {cur}**")
            cb,cs2=st.columns(2)
            with cb:
                st.markdown('<div class="buy-btn">',unsafe_allow_html=True)
                if st.button(lt("BUY","BUY ↑","ENGAGE"),use_container_width=True,disabled=tv>st.session_state.cash):
                    today=datetime.now().date().isoformat()
                    if st.session_state.last_date!=today: st.session_state.daily=0; st.session_state.last_date=today
                    if st.session_state.daily>=10: st.error("Daily trade limit (10) reached.")
                    else:
                        st.session_state.cash-=tv
                        pos=st.session_state.portfolio.get(ticker,{"s":0,"a":cp})
                        ts=pos["s"]+sh; tc=pos["s"]*pos["a"]+tv
                        st.session_state.portfolio[ticker]={"s":ts,"a":tc/ts}
                        st.session_state.daily+=1
                        st.session_state.trades.append({"time":datetime.now().strftime("%H:%M"),"action":"BUY","ticker":ticker,"shares":sh,"price":cp,"pnl":0})
                        st.session_state.ai_exp=explain(ticker,"BUY",sh,cp,df)
                        save_portfolio()
                        st.success(lt(f"Bought {sh:.2f} @ ${cp:.2f}",f"Done! Bought {sh:.2f} × {ticker}",f"ENGAGED — {sh:.2f} units locked"))
                        st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)
            with cs2:
                pos=st.session_state.portfolio.get(ticker,{}); avsh=pos.get("s",0)
                st.markdown('<div class="sell-btn">',unsafe_allow_html=True)
                if st.button(lt("SELL","SELL ↓","EXTRACT"),use_container_width=True,disabled=avsh==0 or sh>avsh):
                    act=min(sh,avsh); proc=act*cp; pnl_t=proc-act*pos["a"]
                    st.session_state.cash+=proc
                    if act>=avsh-0.001: del st.session_state.portfolio[ticker]
                    else: st.session_state.portfolio[ticker]["s"]-=act
                    st.session_state.daily+=1
                    st.session_state.trades.append({"time":datetime.now().strftime("%H:%M"),"action":"SELL","ticker":ticker,"shares":act,"price":cp,"pnl":pnl_t})
                    st.session_state.ai_exp=explain(ticker,"SELL",act,cp,df,pnl_t)
                    ps=f"+${pnl_t:.2f}" if pnl_t>=0 else f"-${abs(pnl_t):.2f}"
                    save_portfolio()
                    st.success(lt(f"Sold {act:.2f} @ ${cp:.2f} | {ps}",f"Sold! P&L: {ps}",f"EXTRACTED | BOUNTY: {ps}"))
                    st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)
            if avsh>0:
                ppnl_v,ppct=ppnl(ticker); pc2="#22c55e" if ppnl_v>=0 else "#ef4444"
                st.markdown(f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.62rem;color:#8892a4;padding:0.35rem;background:#0b0e11;border-radius:2px;margin-top:4px;">POS: {avsh:.2f} sh · Avg ${pos["a"]:.2f}<span style="color:{pc2};"> | P&L: {"+"if ppnl_v>=0 else ""}${ppnl_v:.2f} ({ppct:+.1f}%)</span></div>', unsafe_allow_html=True)
            st.markdown("</div></div>",unsafe_allow_html=True)

        # Stop-loss alerts
        sl_alerts = check_sl()
        if sl_alerts:
            save_portfolio()
        for a in sl_alerts: st.warning(a)

        # AI explanation
        if st.session_state.ai_exp:
            ac={"standard":"aibox std","beginner":"aibox beg","fps":"aibox fps"}[m]
            at={"standard":"🤖 AI TRADING COACH","beginner":"🤖 YOUR HELPER EXPLAINS","fps":"🎮 KILL CAM — TRADE REVIEW"}[m]
            atc={"standard":"aitag std","beginner":"aitag beg","fps":"aitag fps"}[m]
            exp_html=st.session_state.ai_exp.replace("\n","<br>")
            st.markdown(f'<div class="{ac}"><div class="{atc}">{at}</div>{exp_html}</div>',unsafe_allow_html=True)

        # Market movers
        st.markdown(f'<div class="panel" style="margin-top:0.5rem;"><div class="ph">{lt("Market Movers","Top Movers Today","LEADERBOARD")}</div><div class="ob-row hd"><span>Symbol</span><span>Last</span><span>Chg%</span></div>',unsafe_allow_html=True)
        try:
            for mv in movers()[:8]:
                mc="#22c55e" if mv["p"]>=0 else "#ef4444"; ms2="▲" if mv["p"]>=0 else "▼"
                st.markdown(f'<div class="mrow"><span style="color:#d1d5db;font-weight:600;">{mv["t"]}</span><span style="color:#8892a4;">${mv["l"]:.2f}</span><span style="color:{mc};">{ms2}{abs(mv["p"]):.2f}%</span></div>',unsafe_allow_html=True)
        except: st.caption("Temporarily unavailable")
        st.markdown("</div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 1 — PORTFOLIO
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown(f'<div style="padding:0.7rem 1rem;border-bottom:1px solid #1e2530;"><span style="font-family:\'IBM Plex Mono\',monospace;font-size:0.85rem;font-weight:700;color:#fff;">{lt("Portfolio","My Money","LOADOUT")}</span></div>',unsafe_allow_html=True)
    pv2=pval(); pnl2=pv2-10000; inv=pv2-st.session_state.cash
    c1,c2,c3,c4=st.columns(4)
    c1.metric(lt("Portfolio Value","Total Worth","LOADOUT VALUE"),f"${pv2:,.2f}")
    c2.metric(lt("Cash","Cash (Ammo)","AMMO"),f"${st.session_state.cash:,.2f}")
    c3.metric(lt("Total P&L","Profit/Loss","K/D BOUNTY"),f"${pnl2:,.2f}",f"{pnl2/100:+.1f}%")
    c4.metric(lt("Invested","In Stocks","ON THE FIELD"),f"${inv:,.2f}")
    if not st.session_state.portfolio:
        st.info(lt("No open positions.","You don't own any stocks yet! Go to Trade tab.","INVENTORY EMPTY — head to ENGAGE tab."))
    else:
        rows=[]
        for t_,pos in st.session_state.portfolio.items():
            pr=price(t_); pn,pt=ppnl(t_)
            rows.append({"Ticker":t_,"Shares":f"{pos['s']:.4f}","Entry":f"${pos['a']:.2f}","Now":f"${pr:.2f}","Value":f"${pos['s']*pr:,.2f}","P&L":f"{'+'if pn>=0 else ''}${pn:.2f}","P&L%":f"{pt:+.1f}%"})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        if len(st.session_state.portfolio)>=2:
            lbls=list(st.session_state.portfolio.keys())+["Cash"]
            vals=[st.session_state.portfolio[t_]["s"]*price(t_) for t_ in st.session_state.portfolio]+[st.session_state.cash]
            fig_p=go.Figure(go.Pie(labels=lbls,values=vals,hole=0.55,
                marker=dict(colors=["#3b82f6","#22c55e","#f59e0b","#8b5cf6","#ef4444","#06b6d4"],line=dict(color="#0b0e11",width=2)),
                textfont=dict(family="IBM Plex Mono",size=10)))
            fig_p.update_layout(paper_bgcolor="#0b0e11",plot_bgcolor="#0b0e11",font_color="#8892a4",height=240,
                margin=dict(l=0,r=0,t=20,b=0),legend=dict(font=dict(family="IBM Plex Mono",size=10),bgcolor="rgba(0,0,0,0)"),
                title=dict(text=lt("Allocation","Split","LOADOUT SPLIT"),font=dict(family="IBM Plex Mono",size=11,color="#8892a4")))
            st.plotly_chart(fig_p,use_container_width=True)
    if st.session_state.trades:
        st.markdown(f"#### {lt('Trade History','All My Trades','MATCH HISTORY')}")
        st.dataframe(pd.DataFrame(st.session_state.trades)[::-1].head(30),use_container_width=True,hide_index=True)
        if len(st.session_state.trades)>1:
            run=10000.0; eq=[]
            for tr in st.session_state.trades: run+=tr.get("pnl",0); eq.append({"#":len(eq)+1,"Value":round(run,2)})
            fig_e=go.Figure(go.Scatter(x=[e["#"] for e in eq],y=[e["Value"] for e in eq],
                line=dict(color="#3b82f6",width=1.5),fill="tozeroy",fillcolor="rgba(59,130,246,0.06)"))
            fig_e.add_hline(y=10000,line_color="#374151",line_dash="dash",line_width=0.8)
            fig_e.update_layout(paper_bgcolor="#111519",plot_bgcolor="#0b0e11",height=190,
                margin=dict(l=6,r=6,t=20,b=6),showlegend=False,
                title=dict(text=lt("Equity Curve","How Your Money Grew","PERFORMANCE ARC"),font=dict(family="IBM Plex Mono",size=11,color="#8892a4")),
                xaxis=dict(gridcolor="#1e2530",tickfont=dict(family="IBM Plex Mono",size=9)),
                yaxis=dict(gridcolor="#1e2530",side="right",tickfont=dict(family="IBM Plex Mono",size=9)))
            st.plotly_chart(fig_e,use_container_width=True)

    # ── Local Data & Export ────────────────────
    st.markdown("---")
    st.markdown(f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.7rem;font-weight:700;color:#8892a4;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;">{lt("💾 Local Data & Export","💾 Save & Download Your Data","💾 SAVE SYSTEM")}</div>', unsafe_allow_html=True)

    si_info = get_save_info()
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown(f"""
        <div class="panel">
          <div class="ph">Save File</div>
          <div style="padding:0.6rem 0.75rem;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;line-height:1.8;">
            <div style="color:#8892a4;">Location</div>
            <div style="color:#d1d5db;word-break:break-all;">{si_info['path']}</div>
            <div style="color:#8892a4;margin-top:0.4rem;">Last Saved</div>
            <div style="color:{'#22c55e' if si_info['exists'] else '#4b5563'};">
              {si_info.get('last_saved','Not saved yet')}
            </div>
            <div style="color:#8892a4;margin-top:0.4rem;">Format</div>
            <div style="color:#d1d5db;">JSON + CSV (auto)</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with col_s2:
        st.markdown('<div class="ph" style="background:#161b21;border:1px solid #1e2530;border-radius:3px 3px 0 0;padding:0.38rem 0.75rem;">Export Portfolio</div>', unsafe_allow_html=True)
        if st.session_state.portfolio:
            rows_export = []
            for t_, pos in st.session_state.portfolio.items():
                pr = price(t_); pn, pt = ppnl(t_)
                rows_export.append({"Ticker": t_, "Shares": pos['s'], "Avg_Entry": pos['a'],
                                    "Current_Price": pr, "Value": pos['s']*pr,
                                    "PnL": pn, "PnL_Pct": pt})
            df_export = pd.DataFrame(rows_export)
            st.download_button(
                label=lt("⬇ Download Positions CSV","⬇ Download My Stocks (CSV)","⬇ EXPORT LOADOUT"),
                data=df_export.to_csv(index=False),
                file_name=f"tradesim_positions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv", use_container_width=True,
            )
        else:
            st.caption("No positions to export.")

        if st.session_state.trades:
            df_trades_export = pd.DataFrame(st.session_state.trades)
            st.download_button(
                label=lt("⬇ Download Trade History CSV","⬇ Download All My Trades","⬇ EXPORT MATCH HISTORY"),
                data=df_trades_export.to_csv(index=False),
                file_name=f"tradesim_trades_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv", use_container_width=True,
            )
        else:
            st.caption("No trades to export.")

    with col_s3:
        st.markdown('<div class="ph" style="background:#161b21;border:1px solid #1e2530;border-radius:3px 3px 0 0;padding:0.38rem 0.75rem;">Backup & Restore</div>', unsafe_allow_html=True)

        # Manual save button
        if st.button(lt("💾 Force Save Now","💾 Save My Progress Now","💾 MANUAL SAVE"), use_container_width=True):
            save_portfolio()
            save_settings()
            st.success(lt(f"Saved to {SAVE_FILE}",
                          f"Saved! Your data is at: {SAVE_FILE}",
                          f"PROGRESS SAVED — {SAVE_FILE}"))

        # Download full JSON backup
        try:
            backup_data = {
                "cash":       st.session_state.cash,
                "portfolio":  st.session_state.portfolio,
                "trades":     st.session_state.trades,
                "created_at": st.session_state.get("created_at",""),
                "exported_at": datetime.now().isoformat(),
                "settings": {
                    "lang_mode": st.session_state.lang_mode,
                    "sl": st.session_state.sl,
                    "period": st.session_state.period,
                }
            }
            st.download_button(
                label=lt("⬇ Download Full Backup (JSON)","⬇ Download Full Backup","⬇ EXPORT FULL SAVE FILE"),
                data=json.dumps(backup_data, indent=2),
                file_name=f"tradesim_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json", use_container_width=True,
            )
        except Exception as e:
            st.caption(f"Backup error: {e}")

        # Restore from uploaded file
        uploaded = st.file_uploader(
            lt("Restore from backup JSON","Restore from a backup file","LOAD SAVE FILE"),
            type=["json"], label_visibility="collapsed",
            help="Upload a previously downloaded backup JSON to restore your portfolio"
        )
        if uploaded:
            try:
                restore_data = json.loads(uploaded.read())
                st.session_state.cash      = float(restore_data["cash"])
                st.session_state.portfolio = restore_data["portfolio"]
                st.session_state.trades    = restore_data["trades"]
                if "settings" in restore_data:
                    s = restore_data["settings"]
                    st.session_state.lang_mode = s.get("lang_mode", "standard")
                    st.session_state.sl        = float(s.get("sl", 5.0))
                    st.session_state.period    = s.get("period", "6mo")
                save_portfolio()
                save_settings()
                st.success(lt("✅ Portfolio restored successfully!",
                              "✅ Your saved data has been restored!",
                              "✅ SAVE FILE LOADED — GOOD TO GO"))
                st.rerun()
            except Exception as e:
                st.error(f"Could not restore backup: {e}")

    # Stats summary
    started = st.session_state.get("created_at","")
    num_trades = len(st.session_state.trades)
    buys  = len([t for t in st.session_state.trades if t.get("action")=="BUY"])
    sells = len([t for t in st.session_state.trades if t.get("action")=="SELL"])
    wins  = len([t for t in st.session_state.trades if t.get("action")=="SELL" and t.get("pnl",0)>0])
    wr    = round(wins/sells*100,1) if sells>0 else 0
    pv_now= pval(); total_pnl = pv_now - 10000

    st.markdown(f"""
    <div class="panel" style="margin-top:0.5rem;">
      <div class="ph">Account Statistics</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0;">
        <div style="padding:0.5rem 0.75rem;border-right:1px solid #1e2530;border-bottom:1px solid #1e2530;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#8892a4;text-transform:uppercase;">Total Trades</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.95rem;color:#fff;font-weight:700;">{num_trades}</div>
        </div>
        <div style="padding:0.5rem 0.75rem;border-right:1px solid #1e2530;border-bottom:1px solid #1e2530;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#8892a4;text-transform:uppercase;">Win Rate</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.95rem;color:{'#22c55e' if wr>=50 else '#ef4444'};font-weight:700;">{wr}%</div>
        </div>
        <div style="padding:0.5rem 0.75rem;border-right:1px solid #1e2530;border-bottom:1px solid #1e2530;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#8892a4;text-transform:uppercase;">Total P&L</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.95rem;color:{'#22c55e' if total_pnl>=0 else '#ef4444'};font-weight:700;">{'+'if total_pnl>=0 else ''}${total_pnl:,.2f}</div>
        </div>
        <div style="padding:0.5rem 0.75rem;border-bottom:1px solid #1e2530;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#8892a4;text-transform:uppercase;">Started</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#d1d5db;">{started[:10] if started else '—'}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — NEWS & REPORTS  (Apple News / NYT style)
# ══════════════════════════════════════════════
with tabs[2]:
    arts=get_news(st.session_state.ticker)
    now_s=datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f"""
    <div style="padding:1rem 1.2rem 0;">
      <div class="masthead">TradeSim Market Intelligence</div>
      <div class="datebar">
        {now_s} · Real-time market news & analysis
        <span style="float:right;color:#22c55e;"><span class="ldot green"></span> Live Data: Yahoo Finance</span>
      </div>
    </div>""",unsafe_allow_html=True)

    # Category filter
    sel_cat=st.session_state.news_cat
    cf=st.columns([1,1,1,1,1,4])
    cats2=["All","Markets","ASX","Tech","Economy"]
    for i,(c,cat) in enumerate(zip(cf[:5],cats2)):
        with c:
            if st.button(cat,key=f"nc{i}"):
                st.session_state.news_cat=cat; st.rerun()
    st.markdown("<hr style='border-color:#1e2530;margin:0.5rem 0;'>",unsafe_allow_html=True)

    sel_cat=st.session_state.news_cat
    if sel_cat!="All": arts=[a for a in arts if a["cat"]==sel_cat]

    def sbadge(s): return {"bull":'<span class="sbadge sb-bull">Bullish</span>',"bear":'<span class="sbadge sb-bear">Bearish</span>',"neut":'<span class="sbadge sb-neut">Neutral</span>'}[s]
    def tks_html(tks): return " ".join([f'<span class="tc">{t}</span>' for t in tks[:3]])

    feats=[a for a in arts if a.get("feat")]; rest2=[a for a in arts if not a.get("feat")]

    if feats:
        fa=feats[0]
        col_m,col_s=st.columns([2,1],gap="medium")
        with col_m:
            st.markdown(f"""
            <div style="padding:0 0.4rem;">
              <div class="ncat {fa['cls']}">{fa['cat'].upper()}</div>
              <div class="nhl-lg">{fa['hl']}</div>
              <div class="nsumm">{fa['summ']}</div>
              <div class="nmeta">
                {sbadge(fa['sent'])}
                <span class="nsrc">{fa['src']}</span>
                <span>·</span><span>{fa['time']}</span>
                <span>·</span>{tks_html(fa['tks'])}
                <span>·</span><a href="{fa['url']}" target="_blank" class="nlink">Read full article ↗</a>
              </div>
            </div>""",unsafe_allow_html=True)
        with col_s:
            for a in feats[1:3]:
                st.markdown(f"""
                <div style="border-left:2px solid #1e2530;padding-left:0.75rem;margin-bottom:0.9rem;">
                  <div class="ncat {a['cls']}">{a['cat'].upper()}</div>
                  <div class="nhl-sm">{a['hl']}</div>
                  <div class="nsumm" style="font-size:0.74rem;">{a['summ'][:120]}…</div>
                  <div class="nmeta">{sbadge(a['sent'])}<span class="nsrc">{a['src']}</span><span>·</span>{tks_html(a['tks'])}<span>·</span><a href="{a['url']}" target="_blank" class="nlink">↗</a></div>
                </div>""",unsafe_allow_html=True)

    st.markdown('<hr class="news-divider" style="border-color:#1e2530;margin:0.8rem 0;">',unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.12em;color:#4b5563;margin-bottom:0.7rem;">Latest Stories</div>',unsafe_allow_html=True)

    remaining=(feats[3:] if len(feats)>3 else [])+rest2
    cols3=st.columns(3,gap="medium")
    for i,art in enumerate(remaining[:9]):
        with cols3[i%3]:
            st.markdown(f"""
            <div class="ncard">
              <div class="nbody">
                <div class="ncat {art['cls']}">{art['cat'].upper()}</div>
                <div class="nhl-sm" style="font-size:0.88rem;">{art['hl']}</div>
                <div class="nsumm" style="font-size:0.75rem;">{art['summ'][:130]}…</div>
                <div class="nmeta">{sbadge(art['sent'])}<span class="nsrc">{art['src']}</span><span>·</span><span>{art['time']}</span></div>
                <div style="margin-top:0.4rem;display:flex;justify-content:space-between;align-items:center;">
                  <div>{tks_html(art['tks'])}</div>
                  <a href="{art['url']}" target="_blank" class="nlink" style="color:#3b82f6;">Read ↗</a>
                </div>
              </div>
            </div>""",unsafe_allow_html=True)

    st.markdown("""
    <hr style="border-color:#1e2530;margin:0.8rem 0;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#4b5563;line-height:1.9;">
      <strong style="color:#8892a4;">Data Sources:</strong>
      <a href="https://finance.yahoo.com" target="_blank" style="color:#3b82f6;text-decoration:none;">Yahoo Finance</a> ·
      <a href="https://www.reuters.com/markets/" target="_blank" style="color:#3b82f6;text-decoration:none;">Reuters</a> ·
      <a href="https://www.bloomberg.com/markets" target="_blank" style="color:#3b82f6;text-decoration:none;">Bloomberg</a> ·
      <a href="https://www.afr.com/markets" target="_blank" style="color:#3b82f6;text-decoration:none;">AFR</a> ·
      <a href="https://www.cnbc.com/markets/" target="_blank" style="color:#3b82f6;text-decoration:none;">CNBC</a> ·
      <a href="https://www.wsj.com/markets" target="_blank" style="color:#3b82f6;text-decoration:none;">WSJ</a> ·
      <a href="https://www.smh.com.au/business/markets" target="_blank" style="color:#3b82f6;text-decoration:none;">SMH</a> ·
      <a href="https://www.ft.com/markets" target="_blank" style="color:#3b82f6;text-decoration:none;">FT</a><br>
      <span style="color:#374151;">Market data is real-time via Yahoo Finance. News summaries are curated educational content — always verify at the linked source before making any investment decisions.</span>
    </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — BACKTEST
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown(f'<div style="padding:0.7rem 1rem;border-bottom:1px solid #1e2530;"><span style="font-family:\'IBM Plex Mono\',monospace;font-size:0.85rem;font-weight:700;color:#fff;">{lt("Backtest Simulator","Strategy Time Machine","REPLAY MODE")}</span></div>',unsafe_allow_html=True)
    st.info(lt("SMA Golden/Death Cross: buy when SMA20>SMA50, sell when SMA20<SMA50.",
               "We go back in time and test a simple rule: buy when short average goes above long average, sell when it drops below.",
               "FIXED STRATEGY: PUSH on golden cross, EXTRACT on death cross. Running replay..."))
    c1,c2=st.columns(2)
    with c1: bt_t=st.text_input(lt("Ticker","Stock Code","Target"),st.session_state.ticker)
    with c2: bt_y=st.slider(lt("Years","Years back","Seasons back"),1,5,2)
    if st.button(lt("▶  Run Backtest","▶  Test It!","▶  LAUNCH REPLAY"),type="primary",use_container_width=True):
        with st.spinner("Running…"):
            res=backtest(bt_t,bt_y)
        if not res:
            st.error(lt("Not enough data.","Not enough history. Try SPY or BHP.AX.","NOT ENOUGH MATCH DATA."))
        else:
            c1,c2,c3,c4=st.columns(4)
            c1.metric(lt("Final Value","Ended With","FINAL LOOT"),f"${res['fv']:,.2f}")
            c2.metric(lt("Total Return","Gain/Loss","TOTAL GAIN"),f"{res['ret']:+.1f}%")
            c3.metric(lt("Win Rate","% Profitable","WIN RATE"),f"{res['wr']}%")
            c4.metric(lt("# Trades","How Many","ENGAGEMENTS"),res["nt"])
            c5,c6=st.columns(2)
            c5.metric(lt("Best Trade","Best Win","BEST KILL"),f"${res['best']:,.2f}")
            c6.metric(lt("Worst Trade","Worst Loss","WORST DEATH"),f"${res['worst']:,.2f}")
            eq_df=pd.DataFrame(res["eq"])
            if not eq_df.empty:
                fig_bt=go.Figure()
                fig_bt.add_trace(go.Scatter(x=eq_df["date"],y=eq_df["value"],line=dict(color="#3b82f6",width=1.5),fill="tozeroy",fillcolor="rgba(59,130,246,0.05)",name="Portfolio"))
                fig_bt.add_hline(y=10000,line_color="#374151",line_dash="dash",line_width=0.8)
                buys=[t for t in res["trades"] if t["type"]=="BUY"]; sells2=[t for t in res["trades"] if t["type"]=="SELL"]
                fig_bt.add_trace(go.Scatter(x=[t["date"] for t in buys],y=[t["price"] for t in buys],mode="markers",marker=dict(color="#22c55e",size=7,symbol="triangle-up"),name="Buy",yaxis="y2"))
                fig_bt.add_trace(go.Scatter(x=[t["date"] for t in sells2],y=[t["price"] for t in sells2],mode="markers",marker=dict(color="#ef4444",size=7,symbol="triangle-down"),name="Sell",yaxis="y2"))
                fig_bt.update_layout(template="plotly_dark",paper_bgcolor="#111519",plot_bgcolor="#0b0e11",height=300,
                    margin=dict(l=6,r=6,t=20,b=6),
                    xaxis=dict(gridcolor="#1e2530",tickfont=dict(family="IBM Plex Mono",size=9)),
                    yaxis=dict(gridcolor="#1e2530",side="left",tickfont=dict(family="IBM Plex Mono",size=9),title="Portfolio $"),
                    yaxis2=dict(overlaying="y",side="right",showgrid=False,tickfont=dict(family="IBM Plex Mono",size=9),title="Price"),
                    legend=dict(font=dict(family="IBM Plex Mono",size=10),bgcolor="rgba(0,0,0,0)"),
                    title=dict(text=f"{bt_t} — SMA Crossover ({bt_y}y)",font=dict(family="IBM Plex Mono",size=11,color="#8892a4")))
                st.plotly_chart(fig_bt,use_container_width=True)
            if res["trades"]: st.dataframe(pd.DataFrame(res["trades"]),use_container_width=True,hide_index=True)
            verdict="✅ Strategy outperformed cash." if res["ret"]>0 else "📉 Buy-and-hold may have beaten this strategy in this period."
            st.markdown(f'<div class="aibox std"><div class="aitag std">📊 BACKTEST ANALYSIS</div><strong>{res["wr"]}% win rate</strong> — {res["wr"]:.0f}/100 sell trades profitable.<br><br>$10,000 → <strong>${res["fv"]:,.2f}</strong> ({res["ret"]:+.1f}%) · Best: <span style="color:#22c55e;">${res["best"]:,.2f}</span> · Worst: <span style="color:#ef4444;">${res["worst"]:,.2f}</span><br><br>{verdict}</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — LEARN
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown(f'<div style="padding:0.7rem 1rem;border-bottom:1px solid #1e2530;"><span style="font-family:\'IBM Plex Mono\',monospace;font-size:0.85rem;font-weight:700;color:#fff;">{lt("Trading Concepts","Trading Explained Simply","FIELD MANUAL")}</span></div>',unsafe_allow_html=True)

    LEARN=[
        {"ts":"📊 RSI — Relative Strength Index","tb":"📊 RSI — Is It Overbought or Oversold?","tf":"🩸 RSI — ENEMY HEALTH METER",
         "cs":"""**RSI** (0–100) measures momentum — overbought vs oversold.\n\n| RSI | Signal | Action |\n|-----|--------|--------|\n| >70 | 🔴 Overbought | Consider selling |\n| <30 | 🟢 Oversold | Possible bounce |\n| 30–70 | 🟡 Neutral | Normal |\n\nBest used with trend indicators — not in isolation.""",
         "cb":"""**RSI = temperature gauge for a stock.**\n\n🌡️ **Too hot (>70):** Everyone bought — price got too high. May drop.\n🌡️ **Too cold (<30):** Everyone sold — price may bounce back up!\n🌡️ **Normal (30–70):** Just doing its thing.\n\n**Simple rule:** Below 30 = look to buy. Above 70 = be careful buying.""",
         "cf":"""**RSI = enemy's health bar.**\n\n🩸 RSI<30 — LOW HP. Push. High kill potential.\n⚡ RSI>70 — FULL HP + JUICED. Don't 1v1. Wait.\n⚔️ 30–70 — Even match. Read the map.\n\n**Always check the map (trend) before engaging.**"""},
        {"ts":"📈 Moving Averages (SMA)","tb":"📈 Moving Averages — The Stock's Habit Line","tf":"🗺️ SMAs — MAP CONTROL LINES",
         "cs":"""**SMAs** smooth price by averaging N closing days.\n\n- **SMA20** = 20-day avg (short-term)\n- **SMA50** = 50-day avg (medium-term)\n\n**Golden Cross** (SMA20>SMA50) = 🟢 Bullish\n**Death Cross** (SMA20<SMA50) = 🔴 Bearish""",
         "cb":"""SMA = average price over the last 20 or 50 days. Smooths out wild swings.\n\n📅 **SMA20** = recent 20-day average (short-term mood)\n📅 **SMA50** = 50-day average (longer trend)\n\n⭐ **Golden Cross** = SMA20 jumps above SMA50. Buy signal!\n☠️ **Death Cross** = SMA20 drops below SMA50. Warning!\n\nPrice above both averages = uptrend. Below both = downtrend.""",
         "cf":"""**SMAs = map control lines. Hold them = advantage.**\n\n🏔️ Price above SMA20 & SMA50 → HIGH GROUND. Push!\n💀 Price below SMA20 & SMA50 → LOW GROUND. Defend or extract.\n🔥 **Golden Cross** = KILLSTREAK ACTIVATED — major buy trigger.\n💀 **Death Cross** = WIPE — rotate out immediately."""},
        {"ts":"📦 ETFs Explained","tb":"📦 ETFs — The Easy Investing Bundle","tf":"🧰 ETFs — SQUAD BUNDLE PACKS",
         "cs":"""**ETF** = basket of stocks trading as one share.\n\n| ETF | Tracks |\n|-----|--------|\n| SPY | S&P 500 (top 500 US) |\n| QQQ | NASDAQ 100 (top 100 tech) |\n| VAS.AX | ASX 300 (top 300 AUS) |\n\nBenefits: instant diversification, low fees, liquid.""",
         "cb":"""ETF = shopping basket of stocks. Buy one ETF = own a tiny slice of many companies.\n\n🛒 **VAS.AX** → top 300 Australian companies in one click!\n🛒 **SPY** → top 500 American companies\n🛒 **QQQ** → top 100 tech companies\n\nIf one company crashes, others absorb the hit. Much safer for beginners!""",
         "cf":"""**ETFs = squad bundle packs. Buy the whole team instead of going solo.**\n\n🎮 **SPY** = Meta squad — stable, high long-run win rate.\n🎮 **QQQ** = Tech squad — high DPS, can crash hard.\n🎮 **VAS.AX** = AUS local servers — home advantage.\n\n**Solo queue = one bad pick wipes your run. ETF = 300 players carrying.**"""},
        {"ts":"⚠️ Stop-Loss — Capital Protection","tb":"⚠️ Stop-Loss — Your Safety Net","tf":"🛡️ STOP-LOSS — RESPAWN INSURANCE",
         "cs":"""Auto-sells when price drops N% below entry.\n\n**Example:** Buy $100, 5% stop → auto-sells at $95. Max loss = $5.\n\n- Risk max 1–2% of capital per trade\n- Set stop *immediately* after buying\n- Never move it down hoping for recovery""",
         "cb":"""You buy at $100. Set 5% stop-loss. If it drops to $95 — **auto-sold!** You lose $5 instead of $50+.\n\n🛡️ Like a safety net under a tightrope walker. Hope you never need it — but it saves you!\n\n**Set your Safety Net % in the sidebar. We handle it automatically.**""",
         "cf":"""**No stop = permadeath mode.**\n\nBuy $100 → set 5% stop → auto-extracts at $95 → took 5 damage and lived.\nNo stop → stock craters to $40 → ACCOUNT DESTROYED.\n\n**Rules:** Never risk >1–2% bankroll per play. Set stop BEFORE entering. Never push it down — that's cope."""},
        {"ts":"🇦🇺 Trading ASX Stocks","tb":"🇦🇺 How to Trade Australian Stocks","tf":"🇦🇺 ASX — AUS REGIONAL SERVERS",
         "cs":"""**ASX** lists 2,000+ companies. Tickers end in **.AX**.\n\n| Sector | Names |\n|--------|-------|\n| Banking | CBA, WBC, NAB, ANZ |\n| Mining | BHP, RIO, FMG |\n| Retail | WOW, WES |\n| Healthcare | CSL |\n\n**Hours:** 10am–4pm AEST Mon–Fri\n**ETFs:** VAS.AX, STW.AX, IOZ.AX""",
         "cb":"""Australia's stock exchange is the **ASX.** All codes end in **.AX**.\n\n- **BHP.AX** = one of the world's biggest mining companies ⛏️\n- **CBA.AX** = Australia's biggest bank 🏦\n- **WOW.AX** = Woolworths — yes the supermarket! 🛒\n\n**Open:** 10am–4pm Australian Eastern Time, Mon–Fri.\n\n**Easiest start:** Buy **VAS.AX** — covers Australia's top 300 companies in one trade.""",
         "cf":"""**ASX = AUS regional server. Different timezone, different meta.**\n\nAll AUS tickers end in **.AX** (regional tag).\n\n🏆 S-Tier: BHP.AX, CBA.AX, CSL.AX\n✅ A-Tier: WES.AX, NAB.AX, RIO.AX, MQG.AX\n\n**Server hours:** 10am–4pm AEST, Mon–Fri. Weekend = maintenance.\n**Best starter loadout:** VAS.AX — the AUS squad pack."""},
    ]

    for c in LEARN:
        title={"standard":c["ts"],"beginner":c["tb"],"fps":c["tf"]}[m]
        content={"standard":c["cs"],"beginner":c["cb"],"fps":c["cf"]}[m]
        with st.expander(title): st.markdown(content)

    gt=lt("📖 Full Trading Glossary","📖 Trading Words — Plain English","📖 MARKET WARFARE GLOSSARY")
    with st.expander(gt):
        if m=="standard":
            st.markdown("""| Term | Definition |\n|------|-----------|\n| Bull market | Rising prices — positive sentiment |\n| Bear market | Falling prices — negative sentiment |\n| Volatility | Price swing magnitude |\n| Portfolio | All your investments |\n| Dividend | Profit share paid to shareholders |\n| P&L | Profit and Loss |\n| ETF | Exchange-Traded Fund — basket of stocks |\n| RSI | Relative Strength Index — momentum indicator |\n| SMA | Simple Moving Average — smoothed trend |\n| Golden Cross | SMA20>SMA50 — bullish signal |\n| Death Cross | SMA20<SMA50 — bearish signal |\n| Stop-Loss | Auto-sell at set % loss |\n| Drawdown | Portfolio peak-to-trough loss |""")
        elif m=="beginner":
            st.markdown("""**Bull market 🐂** — Prices going UP everywhere. Happy times!\n\n**Bear market 🐻** — Prices going DOWN. Scary times.\n\n**Shares/Stock 🍕** — A piece of ownership in a company. Like one pizza slice.\n\n**Portfolio 🎒** — All your investments together.\n\n**Dividend 💰** — Some companies pay you money just for owning their stock!\n\n**P&L** — Profit and Loss. How much you made or lost.\n\n**Volatility 🎢** — How wildly prices swing up and down.\n\n**Stop-Loss 🛡️** — Auto-sell if price drops X%. Your safety net.\n\n**Golden Cross ⭐** — 20-day average jumps above 50-day. Buy signal!\n\n**Death Cross ☠️** — 20-day drops below 50-day. Warning signal.""")
        else:
            st.markdown("""| Market Term | FPS Translation |\n|---|---|\n| Bull market | SERVER BUFF — all stocks gaining XP |\n| Bear market | SERVER NERF — stocks debuffed |\n| Volatility | LAG / DESYNC |\n| Portfolio | YOUR INVENTORY / LOADOUT |\n| Dividend | PASSIVE INCOME XP |\n| Stop-Loss | RESPAWN INSURANCE / ARMOUR |\n| Buy | PUSH / ENGAGE |\n| Sell | EXTRACT / RETREAT |\n| RSI | ENEMY HP BAR |\n| SMA | MAP CONTROL LINE |\n| Golden Cross | KILLSTREAK ACTIVATED 🔥 |\n| Death Cross | WIPE / ROTATE OUT 💀 |\n| ETF | SQUAD BUNDLE PACK |\n| P&L | K/D RATIO |\n| Drawdown | TAKING SUSTAINED DAMAGE |\n| ATH | LEGENDARY NOSCOPE MOMENT |""")
