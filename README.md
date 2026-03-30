# Credit Risk Assessment AI Agent

An intelligent credit risk assessment tool powered by AI that analyzes financial and business data to evaluate risk levels, generate detailed explanations, and provide actionable recommendations.

![Risk Assessment](https://img.shields.io/badge/AI-Powered-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)

## Features

- **🤖 AI-Powered Analysis**: Leverages Groq's Llama model for intelligent risk assessment
- **📊 Comprehensive Risk Scoring**: Multi-factor analysis including debt ratios, payment history, and industry risk
- **🎯 Clear Risk Categorization**: Low, Medium, or High risk classification
- **📋 Detailed Explanations**: Clear, actionable insights for credit decisions
- **💡 Smart Recommendations**: Context-aware suggestions for lenders
- **🎨 Modern UI**: Professional, responsive interface built with Streamlit

## Risk Assessment Factors

The AI agent evaluates risk across multiple dimensions:

- **Debt-to-Income Ratio (25%)**: Evaluates debt burden relative to income
- **Payment History (25%)**: Assesses historical payment reliability
- **Credit History Duration (15%)**: Considers length of credit history
- **Revenue Stability (20%)**: Analyzes income consistency and expense ratios
- **Industry Risk (15%)**: Factors in sector-specific risk levels

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd credit-risk-assessment-ai
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Groq API key:
```bash
# Create a .env file in the project root
echo "GROQ_API_KEY=your_api_key_here" > .env
```

Get your Groq API key from: [https://console.groq.com/keys](https://console.groq.com/keys)

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter the applicant and financial data in the sidebar

4. Click "Assess Risk" to generate the AI-powered analysis

## Deployment to Streamlit Cloud

### Option 1: Deploy from GitHub

1. Push your code to a GitHub repository
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository and branch
5. Set the main file path as `app.py`
6. Add your `GROQ_API_KEY` in the advanced settings
7. Click "Deploy!"

### Option 2: Deploy with Secrets

In your Streamlit Cloud app settings, add a secret:
- Key: `GROQ_API_KEY`
- Value: Your Groq API key

## Project Structure

```
credit-risk-assessment-ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # Example environment file
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── SPEC.md            # Project specification
```

## Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

## API Requirements

- **Groq API**: Free tier available at [https://console.groq.com](https://console.groq.com)
- Model used: `llama-3.3-70b-versatile`

## Risk Score Interpretation

| Score Range | Risk Level | Recommendation |
|-------------|------------|---------------|
| 0-33 | 🟢 Low Risk | Approve with standard terms |
| 34-66 | 🟡 Medium Risk | Approve with conditions |
| 67-100 | 🔴 High Risk | Requires additional review |

## Technologies Used

- **Python 3.10+**: Programming language
- **Streamlit**: Web framework
- **Groq API**: AI/ML capabilities
- **python-dotenv**: Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ using Streamlit and Groq AI
