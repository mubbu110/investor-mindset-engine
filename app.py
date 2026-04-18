import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Investor Mindset Engine", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "news_text" not in st.session_state:
    st.session_state.news_text = ""

if "result" not in st.session_state:
    st.session_state.result = None

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f6f8fc 0%, #eef3f9 100%);
    color: #0f172a;
}

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

div[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    border-radius: 14px !important;
    border: 1px solid #cbd5e1 !important;
    font-size: 16px !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white !important;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    padding: 12px 16px;
}

.block-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    border: 1px solid #e2e8f0;
}

.signal-buy {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: white;
    border-radius: 22px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 14px 32px rgba(34,197,94,0.25);
}

.signal-hold {
    background: linear-gradient(135deg, #d97706, #f59e0b);
    color: white;
    border-radius: 22px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 14px 32px rgba(245,158,11,0.25);
}

.signal-sell {
    background: linear-gradient(135deg, #dc2626, #ef4444);
    color: white;
    border-radius: 22px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 14px 32px rgba(239,68,68,0.25);
}

.signal-label {
    font-size: 15px;
    letter-spacing: 1px;
    text-transform: uppercase;
    opacity: 0.9;
}

.signal-main {
    font-size: 42px;
    font-weight: 800;
    margin-top: 8px;
}

.signal-score {
    font-size: 18px;
    margin-top: 4px;
    font-weight: 700;
}

.news-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 6px solid #2563eb;
    border-radius: 18px;
    padding: 16px;
}

.insight-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
}

.mini-metric {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 14px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIC
# -----------------------------
def overall_action(score):
    if score >= 3:
        return "BUY"
    if score <= -3:
        return "SELL"
    return "HOLD"

def signal_class(action):
    return {
        "BUY": "signal-buy",
        "HOLD": "signal-hold",
        "SELL": "signal-sell",
    }[action]

def analyze_news(news_text):
    text = news_text.lower()

    positive_words = [
        "breakout", "surge", "growth", "profit", "beats", "bullish",
        "strong", "up", "gain", "record", "expands", "supportive",
        "cools inflation", "rate cut", "improves"
    ]
    negative_words = [
        "war", "crash", "falls", "drop", "weak", "miss", "bearish",
        "inflation", "tension", "selloff", "risk", "uncertainty",
        "cuts outlook", "slowdown", "decline"
    ]

    score = 0
    for word in positive_words:
        if word in text:
            score += 2
    for word in negative_words:
        if word in text:
            score -= 2

    if score > 10:
        score = 10
    if score < -10:
        score = -10

    overall = overall_action(score)

    if overall == "BUY":
        data = {
            "FII": {"score": 5, "action": "BUY", "analysis": "Foreign investors may prefer adding exposure as momentum improves."},
            "DII": {"score": 4, "action": "BUY", "analysis": "Domestic institutions may support the move with steady accumulation."},
            "Retail": {"score": 3, "action": "BUY", "analysis": "Retail sentiment may turn optimistic on positive headlines."},
            "PRO": {"score": 4, "action": "BUY", "analysis": "Professional traders may ride near-term strength."},
            "Value": {"score": 2, "action": "HOLD", "analysis": "Value investors may stay selective despite improving sentiment."},
        }
        summary = "This headline supports a positive short-term market view with improving investor confidence."
    elif overall == "SELL":
        data = {
            "FII": {"score": -5, "action": "SELL", "analysis": "Foreign investors may reduce exposure due to rising uncertainty."},
            "DII": {"score": -2, "action": "HOLD", "analysis": "Domestic institutions may slow buying and absorb volatility carefully."},
            "Retail": {"score": -4, "action": "SELL", "analysis": "Retail traders may react negatively and cut positions."},
            "PRO": {"score": -5, "action": "SELL", "analysis": "Professional money may hedge or exit in the short term."},
            "Value": {"score": -1, "action": "HOLD", "analysis": "Value investors may wait for better entry levels."},
        }
        summary = "This headline creates negative sentiment and suggests a cautious to bearish near-term setup."
    else:
        data = {
            "FII": {"score": -1, "action": "HOLD", "analysis": "Foreign flows may remain mixed until direction becomes clearer."},
            "DII": {"score": 1, "action": "HOLD", "analysis": "Domestic institutions may remain stable but not aggressive."},
            "Retail": {"score": 0, "action": "HOLD", "analysis": "Retail sentiment may stay balanced without a strong trigger."},
            "PRO": {"score": -1, "action": "HOLD", "analysis": "Professional desks may wait for confirmation before taking large bets."},
            "Value": {"score": 2, "action": "BUY", "analysis": "Value investors may look for selective opportunities."},
        }
        summary = "This headline looks neutral overall, with no strong buy or sell conviction across investors."

    return {
        "headline": news_text,
        "summary": summary,
        "overall_score": score,
        "overall_action": overall,
        "data": data,
    }

def create_bar_chart(result):
    names = list(result["data"].keys())
    scores = [result["data"][k]["score"] for k in names]
    colors = []

    for s in scores:
        if s > 0:
            colors.append("#16a34a")
        elif s < 0:
            colors.append("#ef4444")
        else:
            colors.append("#f59e0b")

    fig = go.Figure(go.Bar(
        x=names,
        y=scores,
        marker_color=colors,
        text=[f"{s:+}" for s in scores],
        textposition="outside"
    ))

    fig.add_hline(y=0, line_color="#94a3b8", line_width=1)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=360,
        yaxis=dict(range=[-10, 10], gridcolor="rgba(148,163,184,0.2)"),
        xaxis=dict(showgrid=False),
    )
    return fig

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("""
<div style="padding-top:8px;padding-bottom:12px;">
    <div style="font-size:22px;font-weight:800;color:#facc15;">Investor Mindset Engine</div>
    <div style="font-size:12px;color:#cbd5e1;letter-spacing:1px;">SIMPLE NEWS SENTIMENT DASHBOARD</div>
</div>
""", unsafe_allow_html=True)

sample = "L&T broke out of a month-long consolidation, reclaiming key moving averages."

if st.sidebar.button("Use Sample Headline"):
    st.session_state.news_text = sample

st.sidebar.text_area(
    "Paste market news headline",
    key="news_text",
    height=180,
    placeholder="Paste your market news here..."
)

analyze = st.sidebar.button("Analyze News")

# -----------------------------
# MAIN
# -----------------------------
st.markdown("## News Sentiment Dashboard")
st.markdown("Paste a news headline and get a simple overall market action with investor-wise breakdown.")

if analyze and st.session_state.news_text.strip():
    st.session_state.result = analyze_news(st.session_state.news_text)

result = st.session_state.result

if result:
    action = result["overall_action"].upper()
    score = result["overall_score"]
    card_class = signal_class(action)

    top1, top2 = st.columns([1.3, 2.2])

    with top1:
        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="signal-label">Overall Signal</div>
                <div class="signal-main">{action}</div>
                <div class="signal-score">Score: {score:+}/10</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top2:
        st.markdown(
            f"""
            <div class="news-box">
                <div style="font-size:18px;font-weight:800;color:#0f172a;margin-bottom:8px;">Headline</div>
                <div style="font-size:16px;color:#1e293b;font-weight:600;">{result["headline"]}</div>
                <div style="margin-top:10px;color:#475569;line-height:1.6;">{result["summary"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Investor Score Breakdown")
    chart_col, side_col = st.columns([2.1, 1.2])

    with chart_col:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.plotly_chart(create_bar_chart(result), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with side_col:
        for name, info in result["data"].items():
            color = "#16a34a" if info["score"] > 0 else "#ef4444" if info["score"] < 0 else "#f59e0b"
            st.markdown(
                f"""
                <div class="insight-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-size:17px;font-weight:800;color:#0f172a;">{name}</div>
                        <div style="font-size:14px;font-weight:800;color:{color};">{info["action"]} {info["score"]:+}</div>
                    </div>
                    <div style="margin-top:8px;color:#475569;line-height:1.5;">{info["analysis"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Quick View")
    cols = st.columns(5)
    for i, (name, info) in enumerate(result["data"].items()):
        with cols[i]:
            color = "#16a34a" if info["score"] > 0 else "#ef4444" if info["score"] < 0 else "#f59e0b"
            st.markdown(
                f"""
                <div class="mini-metric">
                    <div style="font-size:12px;color:#64748b;text-transform:uppercase;">{name}</div>
                    <div style="font-size:22px;font-weight:800;color:{color};margin-top:6px;">{info["action"]}</div>
                    <div style="font-size:14px;font-weight:700;color:#334155;">{info["score"]:+}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("Click 'Use Sample Headline' or paste your own news headline, then press Analyze News.")
