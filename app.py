import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import random

load_dotenv()

st.set_page_config(
    page_title="Credit Risk Assessment AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #2C5282 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .risk-badge {
        font-size: 2.5rem;
        font-weight: 700;
        padding: 1rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #38A169 0%, #2F855A 100%);
        color: white;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #D69E2E 0%, #B7791F 100%);
        color: white;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #E53E3E 0%, #C53030 100%);
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #4A5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .result-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .result-section h3 {
        color: #1E3A5F;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.5rem;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #EBF8FF 0%, #E6FFFA 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #2C5282;
    }
    
    .strength-item, .weakness-item {
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .strength-item::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #38A169;
        font-weight: 700;
    }
    
    .weakness-item::before {
        content: '✗';
        position: absolute;
        left: 0;
        color: #E53E3E;
        font-weight: 700;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1E3A5F 0%, #2C5282 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .info-box {
        background: #EBF8FF;
        border-left: 4px solid #2C5282;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .sidebar .stTextInput > label, .sidebar .stNumberInput > label, 
    .sidebar .stSelectbox > label {
        font-weight: 600;
        color: #1E3A5F;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_groq_client():
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None


def calculate_risk_score(data):
    debt_to_income = (
        (data["outstanding_debt"] / data["annual_revenue"] * 100)
        if data["annual_revenue"] > 0
        else 100
    )

    payment_history_scores = {"Excellent": 0, "Good": 25, "Fair": 50, "Poor": 100}
    payment_score = payment_history_scores.get(data["payment_history"], 50)

    credit_duration_scores = {
        "< 1 year": 80,
        "1-3 years": 50,
        "3-5 years": 25,
        "5+ years": 0,
    }
    credit_score = credit_duration_scores.get(data["credit_history"], 40)

    monthly_expense_ratio = (
        (data["monthly_expenses"] / (data["annual_revenue"] / 12))
        if data["annual_revenue"] > 0
        else 1
    )
    expense_score = min(monthly_expense_ratio * 50, 100)

    industry_risk_scores = {
        "Technology": 30,
        "Healthcare": 25,
        "Finance": 35,
        "Retail": 45,
        "Manufacturing": 40,
        "Real Estate": 50,
        "Agriculture": 55,
        "Transportation": 50,
        "Energy": 45,
        "Hospitality": 60,
    }
    industry_score = industry_risk_scores.get(data["industry"], 40)

    loan_to_revenue = (
        (data["loan_amount"] / data["annual_revenue"])
        if data["annual_revenue"] > 0
        else 1
    )
    loan_score = min(loan_to_revenue * 40, 100)

    debt_component = min(debt_to_income * 0.25, 25)
    payment_component = payment_score * 0.25
    credit_component = credit_score * 0.15
    expense_component = min(expense_score * 0.20, 20)
    industry_component = industry_score * 0.15

    risk_score = (
        debt_component
        + payment_component
        + credit_component
        + expense_component
        + industry_component
    )

    return {
        "score": min(risk_score, 100),
        "debt_to_income": debt_to_income,
        "payment_score": payment_score,
        "credit_score": credit_score,
        "expense_score": expense_score,
        "industry_score": industry_score,
    }


def get_risk_level(score):
    if score <= 33:
        return "Low Risk", "low"
    elif score <= 66:
        return "Medium Risk", "medium"
    else:
        return "High Risk", "high"


def generate_ai_analysis(client, data, risk_score, risk_level):
    if not client:
        return generate_fallback_analysis(data, risk_score, risk_level)

    prompt = f"""As a financial risk analyst, analyze the following credit application and provide a detailed assessment:

Applicant: {data["applicant_name"]}
Industry: {data["industry"]}
Annual Revenue: ${data["annual_revenue"]:,.2f}
Monthly Expenses: ${data["monthly_expenses"]:,.2f}
Outstanding Debt: ${data["outstanding_debt"]:,.2f}
Credit History: {data["credit_history"]} ({data["credit_duration"]})
Payment History: {data["payment_history"]}
Requested Loan: ${data["loan_amount"]:,.2f} for {data["loan_purpose"]}

Calculated Risk Score: {risk_score["score"]:.1f}/100 ({risk_level[0]})

Please provide in exactly this format:
EXPLANATION: [2-3 sentences explaining the overall risk assessment and key factors]
STRENGTHS: [Bullet points of financial strengths]
WEAKNESSES: [Bullet points of financial concerns or risks]
RECOMMENDATION: [Clear actionable recommendation for the lender]

Keep each section concise but informative."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial risk analyst specializing in credit assessment. Provide clear, professional, and actionable insights.",
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )

        response = chat_completion.choices[0].message.content
        return parse_ai_response(response)

    except Exception as e:
        st.warning(f"AI analysis unavailable: {e}. Using standard analysis.")
        return generate_fallback_analysis(data, risk_score, risk_level)


def parse_ai_response(response):
    sections = {
        "explanation": "",
        "strengths": [],
        "weaknesses": [],
        "recommendation": "",
    }

    current_section = None
    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("EXPLANATION:"):
            current_section = "explanation"
            sections["explanation"] = line.replace("EXPLANATION:", "").strip()
        elif line.startswith("STRENGTHS:"):
            current_section = "strengths"
        elif line.startswith("WEAKNESSES:"):
            current_section = "weaknesses"
        elif line.startswith("RECOMMENDATION:"):
            current_section = "recommendation"
            sections["recommendation"] = line.replace("RECOMMENDATION:", "").strip()
        elif (
            line.startswith("-")
            or line.startswith("•")
            and current_section in ["strengths", "weaknesses"]
        ):
            sections[current_section].append(line.lstrip("-• "))
        elif line and current_section in ["strengths", "weaknesses"]:
            sections[current_section].append(line)

    if not sections["explanation"]:
        sections["explanation"] = response
    if not sections["recommendation"]:
        sections["recommendation"] = (
            "Please review the assessment details above for more information."
        )

    return sections


def generate_fallback_analysis(data, risk_score, risk_level):
    explanations = {
        "Low": f"The applicant {data['applicant_name']} demonstrates strong financial health with manageable debt levels and a solid credit history. The {data['industry']} industry shows stable performance, supporting a positive assessment.",
        "Medium": f"The applicant {data['applicant_name']} shows moderate financial indicators with some areas of concern. While debt levels are manageable, certain factors in the {data['industry']} industry and credit profile warrant careful review.",
        "High": f"The applicant {data['applicant_name']} faces significant financial challenges with elevated debt levels and risk factors in the {data['industry']} industry. Immediate concerns exist regarding creditworthiness and repayment capacity.",
    }

    strengths = []
    if risk_score["payment_score"] < 50:
        strengths.append(f"Excellent payment history showing consistent debt servicing")
    if data["annual_revenue"] > data["outstanding_debt"]:
        strengths.append(f"Revenue exceeds outstanding debt obligations")
    if risk_score["credit_score"] < 40:
        strengths.append(
            f"Established credit history demonstrates financial responsibility"
        )
    if data["monthly_expenses"] < (data["annual_revenue"] / 12) * 0.5:
        strengths.append(f"Healthy expense-to-income ratio below 50%")
    if not strengths:
        strengths.append("Meeting minimum credit requirements")

    weaknesses = []
    if risk_score["debt_to_income"] > 50:
        weaknesses.append(
            f"Debt-to-income ratio of {risk_score['debt_to_income']:.1f}% exceeds recommended levels"
        )
    if risk_score["payment_score"] > 50:
        weaknesses.append("Payment history shows some late or missed payments")
    if data["outstanding_debt"] > data["annual_revenue"]:
        weaknesses.append("Outstanding debt exceeds annual revenue")
    if risk_score["industry_score"] > 45:
        weaknesses.append(
            f"{data['industry']} industry carries inherent market volatility"
        )
    if not weaknesses:
        weaknesses.append("Standard monitoring and review recommended")

    recommendations = {
        "Low": f"APPROVE with standard terms. The applicant qualifies for competitive rates. Consider offering loyalty rewards for timely payments.",
        "Medium": f"APPROVE with conditions. Require additional collateral or co-signer. Implement quarterly financial reviews during loan term.",
        "High": f"REQUIRES REVIEW. Do not approve without significant risk mitigation. Consider restructuring loan terms or reducing amount.",
    }

    risk_category = risk_level.split()[0]

    return {
        "explanation": explanations[risk_category],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendation": recommendations[risk_category],
    }


def main():
    st.markdown(
        """
    <div class="main-header">
        <h1>🤖 Credit Risk Assessment AI Agent</h1>
        <p>Intelligent credit risk analysis powered by advanced AI</p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">Developed by <strong>Nomatter Chisina</strong></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    client = initialize_groq_client()

    tab1, tab2 = st.tabs(["📋 Risk Assessment Form", "💬 Chat with AI Advisor"])

    with tab1:
        show_assessment_form(client)

    with tab2:
        show_chatbot(client)


def show_chatbot(client):
    st.markdown(
        """
    <div class="result-section" style="margin-bottom: 1rem;">
        <h3>💬 AI Risk Advisor Chat</h3>
        <p style="color: #4A5568;">Ask questions about credit risk assessment, loan approvals, or financial analysis in natural language.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about credit risk assessment..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chatbot_response(client, prompt)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.messages:
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.rerun()


def get_chatbot_response(client, prompt):
    risk_context = """You are an expert financial risk analyst specializing in credit assessment. 
    
    You help users understand:
    - Credit risk evaluation criteria
    - Debt-to-income ratios and what they mean
    - Payment history impact on credit scores
    - Industry-specific risk factors
    - Loan approval recommendations
    - Financial metrics and their significance
    
    Provide clear, professional, and actionable insights. Use examples when helpful.
    
    If asked to assess specific scenarios, provide detailed analysis with clear recommendations."""

    chat_history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[-6:]]
    )

    full_prompt = f"""Previous conversation:
{chat_history}

Current question: {prompt}

Please provide a helpful and informative response."""

    if client:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": risk_context},
                    {"role": "user", "content": full_prompt},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"I'm having trouble connecting to the AI service. Please try again. Error: {str(e)}"
    else:
        return get_fallback_chatbot_response(prompt)


def get_fallback_chatbot_response(prompt):
    prompt_lower = prompt.lower()

    if any(word in prompt_lower for word in ["risk level", "assess", "evaluate"]):
        return """Based on general credit risk principles:

**Key factors for risk assessment:**

1. **Debt-to-Income Ratio** - Generally, ratios below 36% are considered healthy
2. **Credit History** - Longer history with on-time payments = lower risk
3. **Payment History** - Consistently paying on time significantly reduces risk
4. **Industry Risk** - Some sectors (like tech startups) carry higher inherent risk
5. **Revenue Stability** - Consistent, growing revenue indicates lower risk

**Risk Categories:**
- 🟢 Low Risk (0-33): Strong financials, good credit history
- 🟡 Medium Risk (34-66): Some concerns but manageable
- 🔴 High Risk (67-100): Significant red flags, requires careful review

Would you like me to analyze a specific case? Use the **Risk Assessment Form** tab for detailed evaluation."""

    elif any(word in prompt_lower for word in ["approve", "approval", "should i lend"]):
        return """When evaluating loan approval, consider:

**Favorable indicators:**
✓ Debt-to-income ratio < 36%
✓ 5+ years of credit history
✓ Excellent payment history
✓ Revenue significantly exceeds debt
✓ Stable industry

**Red flags:**
✗ Debt-to-income > 50%
✗ Poor payment history
✗ Recent credit inquiries
✗ Unstable or declining revenue
✗ High-risk industry with poor fundamentals

**Recommendation:** Use the **Risk Assessment Form** to get a comprehensive score-based evaluation."""

    elif any(word in prompt_lower for word in ["debt", "ratio", "income"]):
        return """**Debt-to-Income Ratio Explained:**

The debt-to-income (DTI) ratio compares your monthly debt payments to your gross monthly income.

**Formula:** DTI = (Monthly Debt Payments / Gross Monthly Income) × 100

**General Guidelines:**
- Below 36%: ✅ Healthy (low risk)
- 36-43%: ⚠️ Moderate (some concern)
- Above 43%: ❌ High (elevated risk)

**Example:** If you earn $10,000/month and have $3,500 in monthly debt payments, your DTI is 35%.

Lenders typically prefer DTI below 36% for optimal loan terms."""

    else:
        return """I'm here to help with credit risk assessment questions!

**I can help with:**
- Explaining risk assessment factors
- Interpreting financial metrics
- Loan approval guidance
- Credit score considerations
- Industry risk factors

**For detailed assessment**, use the **Risk Assessment Form** tab where I can analyze specific financial data and provide a comprehensive risk score.

What would you like to know more about?"""


def show_assessment_form(client):
    with st.sidebar:
        st.markdown("### 📝 Application Data")
        st.markdown("---")

        applicant_name = st.text_input(
            "Applicant Name",
            placeholder="Company or Individual Name",
            help="Enter the name of the loan applicant",
        )

        industry = st.selectbox(
            "Industry Sector",
            options=[
                "Technology",
                "Healthcare",
                "Finance",
                "Retail",
                "Manufacturing",
                "Real Estate",
                "Agriculture",
                "Transportation",
                "Energy",
                "Hospitality",
            ],
            help="Select the primary industry",
        )

        annual_revenue = st.number_input(
            "Annual Revenue ($)",
            min_value=0,
            value=100000,
            step=1000,
            format="%d",
            help="Total annual revenue or income",
        )

        monthly_expenses = st.number_input(
            "Monthly Expenses ($)",
            min_value=0,
            value=5000,
            step=100,
            format="%d",
            help="Average monthly operating expenses",
        )

        outstanding_debt = st.number_input(
            "Outstanding Debt ($)",
            min_value=0,
            value=20000,
            step=1000,
            format="%d",
            help="Total current outstanding debt obligations",
        )

        credit_duration = st.selectbox(
            "Credit History Duration",
            options=["< 1 year", "1-3 years", "3-5 years", "5+ years"],
            help="How long has the applicant had credit?",
        )

        payment_history = st.selectbox(
            "Payment History",
            options=["Excellent", "Good", "Fair", "Poor"],
            help="Overall payment history rating",
        )

        loan_amount = st.number_input(
            "Requested Loan Amount ($)",
            min_value=0,
            value=50000,
            step=5000,
            format="%d",
            help="Amount being requested",
        )

        loan_purpose = st.selectbox(
            "Loan Purpose",
            options=[
                "Working Capital",
                "Business Expansion",
                "Equipment Purchase",
                "Debt Refinancing",
                "Other",
            ],
            help="Primary purpose of the loan",
        )

        st.markdown("---")

        submitted = st.button("🔍 Assess Risk")

        st.markdown(
            """
        <div class="info-box">
            <strong>💡 Tips:</strong><br>
            • Ensure all financial data is accurate<br>
            • Review inputs before assessment<br>
            • Results are based on provided data
        </div>
        """,
            unsafe_allow_html=True,
        )

    if submitted:
        if not applicant_name:
            st.error("⚠️ Please enter the applicant name")
            return

        data = {
            "applicant_name": applicant_name,
            "industry": industry,
            "annual_revenue": annual_revenue,
            "monthly_expenses": monthly_expenses,
            "outstanding_debt": outstanding_debt,
            "credit_duration": credit_duration,
            "credit_history": f"{credit_duration} of credit",
            "payment_history": payment_history,
            "loan_amount": loan_amount,
            "loan_purpose": loan_purpose,
        }

        with st.spinner("🔄 Analyzing risk factors..."):
            risk_score = calculate_risk_score(data)
            risk_level, risk_class = get_risk_level(risk_score["score"])
            analysis = generate_ai_analysis(client, data, risk_score, risk_level)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{data["annual_revenue"]:,.0f}</div>
                <div class="metric-label">Annual Revenue</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{data["outstanding_debt"]:,.0f}</div>
                <div class="metric-label">Outstanding Debt</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            debt_ratio = (
                (data["outstanding_debt"] / data["annual_revenue"] * 100)
                if data["annual_revenue"] > 0
                else 0
            )
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{debt_ratio:.1f}%</div>
                <div class="metric-label">Debt-to-Revenue</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-value">{data["loan_amount"]:,.0f}</div>
                <div class="metric-label">Loan Requested</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        col_risk, col_gauge = st.columns([1, 2])

        with col_risk:
            st.markdown(
                f"""
            <div class="risk-badge risk-{risk_class}">
                {risk_level}<br>
                <span style="font-size: 1rem; opacity: 0.9;">Score: {risk_score["score"]:.1f}/100</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col_gauge:
            st.markdown(
                """
            <div class="result-section">
                <h3>📈 Risk Score Gauge</h3>
            </div>
            """,
                unsafe_allow_html=True,
            )

            score_float = risk_score["score"]

            if score_float <= 33:
                gauge_color = "#38A169"
                active_segment = "low"
            elif score_float <= 66:
                gauge_color = "#D69E2E"
                active_segment = "medium"
            else:
                gauge_color = "#E53E3E"
                active_segment = "high"

            st.markdown(
                f"""
            <div style="display: flex; height: 40px; border-radius: 8px; overflow: hidden; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="flex: 1; background: #E2E8F0; display: flex; align-items: center; justify-content: center; color: {"white" if active_segment == "low" else "#1E3A5F"}; font-weight: 600;">
                    LOW<br><small>0-33</small>
                </div>
                <div style="flex: 1; background: #E2E8F0; display: flex; align-items: center; justify-content: center; color: {"white" if active_segment == "medium" else "#1E3A5F"}; font-weight: 600;">
                    MEDIUM<br><small>34-66</small>
                </div>
                <div style="flex: 1; background: #E2E8F0; display: flex; align-items: center; justify-content: center; color: {"white" if active_segment == "high" else "#1E3A5F"}; font-weight: 600;">
                    HIGH<br><small>67-100</small>
                </div>
            </div>
            
            <div style="position: relative; height: 20px; background: linear-gradient(to right, #38A169, #D69E2E, #E53E3E); border-radius: 10px; margin: 2rem 0;">
                <div style="position: absolute; left: {score_float}%; transform: translateX(-50%); top: -30px;">
                    <div style="font-size: 2rem;">▼</div>
                    <div style="font-weight: 700; font-size: 1.5rem; color: {gauge_color};">{score_float:.1f}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                f"""
            <div class="result-section">
                <h3>📋 Risk Assessment Analysis</h3>
                <p style="font-size: 1.1rem; line-height: 1.8; color: #2D3748;">{analysis["explanation"]}</p>
            </div>
            
            <div class="result-section">
                <h3>💪 Strengths</h3>
                {"".join([f'<div class="strength-item">{s}</div>' for s in analysis["strengths"]])}
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col_right:
            st.markdown(
                f"""
            <div class="result-section">
                <h3>⚠️ Areas of Concern</h3>
                {"".join([f'<div class="weakness-item">{w}</div>' for w in analysis["weaknesses"]])}
            </div>
            
            <div class="recommendation-box">
                <h3 style="margin-top: 0; color: #1E3A5F; font-size: 1.3rem;">🎯 Recommendation</h3>
                <p style="font-size: 1.1rem; line-height: 1.8; color: #2D3748;">{analysis["recommendation"]}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        with st.expander("📊 Detailed Scoring Breakdown"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    """
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #1E3A5F; margin-bottom: 1rem;">Debt Metrics</h4>
                """,
                    unsafe_allow_html=True,
                )
                st.metric("Debt-to-Revenue", f"{risk_score['debt_to_income']:.1f}%")
                st.metric("Industry Risk", f"{risk_score['industry_score']}/100")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown(
                    """
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #1E3A5F; margin-bottom: 1rem;">Credit Profile</h4>
                """,
                    unsafe_allow_html=True,
                )
                st.metric("Credit History Score", f"{risk_score['credit_score']}/100")
                st.metric("Payment History Score", f"{risk_score['payment_score']}/100")
                st.markdown("</div>", unsafe_allow_html=True)

            with col3:
                st.markdown(
                    """
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #1E3A5F; margin-bottom: 1rem;">Financial Health</h4>
                """,
                    unsafe_allow_html=True,
                )
                st.metric("Expense Ratio", f"{risk_score['expense_score']:.1f}/100")
                st.metric("Final Risk Score", f"{risk_score['score']:.1f}/100")
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; padding: 2rem 0; color: #4A5568; font-size: 0.9rem;">
        <p><strong>Credit Risk Assessment AI Agent</strong></p>
        <p>Developed with ❤️ by <strong>Nomatter Chisina</strong></p>
        <p style="margin-top: 0.5rem;">Powered by Groq AI & Streamlit</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
