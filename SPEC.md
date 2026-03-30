# Risk Assessment AI Agent - Specification

## 1. Project Overview

**Project Name:** Credit Risk Assessment AI Agent  
**Type:** Web Application (Streamlit)  
**Core Functionality:** An AI-powered risk assessment tool that analyzes financial/business data to evaluate credit risk levels and provide actionable recommendations  
**Target Users:** Financial institutions, loan officers, business analysts, and credit assessment teams

## 2. UI/UX Specification

### Layout Structure

- **Single Page Application** with multiple sections
- **Header:** Application title and brief description
- **Sidebar:** Input form for user data entry
- **Main Content Area:** 
  - Assessment results display
  - Risk score visualization
  - Detailed explanations and recommendations

### Visual Design

**Color Palette:**
- Primary: `#1E3A5F` (Deep Navy Blue)
- Secondary: `#2C5282` (Steel Blue)
- Accent Low Risk: `#38A169` (Green)
- Accent Medium Risk: `#D69E2E` (Amber)
- Accent High Risk: `#E53E3E` (Red)
- Background: `#F7FAFC` (Light Gray)
- Card Background: `#FFFFFF` (White)
- Text Primary: `#1A202C` (Dark Gray)
- Text Secondary: `#4A5568` (Medium Gray)

**Typography:**
- Font Family: 'Inter', sans-serif (Google Fonts)
- Heading 1: 32px, Bold
- Heading 2: 24px, SemiBold
- Heading 3: 18px, Medium
- Body: 16px, Regular
- Small: 14px, Regular

**Spacing System:**
- Base unit: 8px
- Padding: 16px, 24px, 32px
- Margins: 16px between sections
- Border radius: 12px for cards

**Visual Effects:**
- Card shadows: `0 4px 6px rgba(0, 0, 0, 0.1)`
- Hover effects on interactive elements
- Smooth transitions: 0.3s ease

### Components

**Input Form (Sidebar):**
- Company/Individual Name (text input)
- Annual Revenue (number input)
- Monthly Expenses (number input)
- Current Outstanding Debt (number input)
- Credit History Duration (dropdown: <1 year, 1-3 years, 3-5 years, 5+ years)
- Payment History (dropdown: Excellent, Good, Fair, Poor)
- Industry Sector (dropdown)
- Requested Loan Amount (number input)
- Loan Purpose (dropdown: Working Capital, Expansion, Equipment, Other)

**Results Display:**
- Risk Score Badge (Large, colored based on risk level)
- Risk Score Gauge (Visual representation 0-100)
- Key Metrics Cards
- Detailed Analysis Section
- Recommendation Panel

**Component States:**
- Default: Standard appearance
- Hover: Slight elevation and color shift
- Active: Full opacity
- Disabled: 50% opacity

## 3. Functionality Specification

### Core Features

1. **Financial Data Input**
   - Form validation for all required fields
   - Real-time input validation
   - Currency formatting for monetary values
   - Smart defaults and placeholders

2. **Risk Assessment Engine**
   - Multi-factor risk scoring algorithm
   - Weighted analysis of:
     - Debt-to-Income ratio (25% weight)
     - Payment history (25% weight)
     - Credit history duration (15% weight)
     - Revenue stability (20% weight)
     - Industry risk factor (15% weight)
   - Score normalization to 0-100 scale
   - Risk categorization: Low (0-33), Medium (34-66), High (67-100)

3. **AI-Powered Analysis**
   - Uses Groq AI (llama-3.3-70b-versatile) for intelligent analysis
   - Generates contextual explanations
   - Provides personalized recommendations
   - Considers industry-specific factors

4. **Results Presentation**
   - Clear risk level indication with color coding
   - Numeric risk score (0-100)
   - Category label (Low/Medium/High)
   - Detailed written explanation
   - Actionable recommendations
   - Key strengths and weaknesses identified

### User Interactions and Flows

1. User enters financial/business data in sidebar
2. User clicks "Assess Risk" button
3. System validates inputs
4. Risk calculation engine processes data
5. AI generates detailed analysis
6. Results display in main area with animations
7. User can export or start new assessment

### Data Handling

- No persistent storage (session-based)
- Local calculation for risk scoring
- API call to Groq for AI analysis
- Environment variable for API key

### Edge Cases

- Missing required fields: Show validation errors
- Invalid numeric inputs: Prevent non-numeric characters
- API timeout: Show retry option
- Zero revenue/debt: Handle gracefully
- Very high risk scores: Cap at 100

## 4. Acceptance Criteria

### Success Conditions

1. **Form Functionality**
   - All input fields accept valid data
   - Validation prevents invalid submissions
   - Form clears after successful assessment

2. **Risk Calculation**
   - Risk score accurately reflects input data
   - Score falls within 0-100 range
   - Risk category matches score range

3. **AI Analysis**
   - Response includes explanation of scoring factors
   - Recommendations are contextual and actionable
   - Analysis completes within 30 seconds

4. **Visual Display**
   - Risk badge displays correct color for level
   - All result sections visible and readable
   - Responsive layout on different screen sizes

5. **User Experience**
   - Page loads within 5 seconds
   - Transitions are smooth
   - Error messages are clear and helpful

### Visual Checkpoints

- [ ] Header with title displays correctly
- [ ] Sidebar form is properly aligned
- [ ] Input fields have correct styling
- [ ] Submit button is prominent and accessible
- [ ] Risk score badge shows correct color
- [ ] Results cards are properly spaced
- [ ] Explanations are readable and formatted
- [ ] Recommendations are actionable

## 5. Technical Stack

- **Frontend:** Streamlit (Python)
- **AI Integration:** Groq API (llama-3.3-70b-versatile)
- **Environment:** Python 3.10+
- **Dependencies:**
  - streamlit
  - groq
  - python-dotenv

## 6. Deployment

- **Platform:** Streamlit Cloud
- **Repository:** GitHub integration
- **Environment Variables:** GROQ_API_KEY
