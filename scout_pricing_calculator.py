"""
Scout Financial - Pricing Calculator
A Streamlit web application for calculating service pricing

To run locally:
1. pip install streamlit
2. streamlit run scout_pricing_calculator.py

To deploy on Streamlit Community Cloud:
1. Push this file to a GitHub repository
2. Go to share.streamlit.io
3. Connect your GitHub and select this file
"""

import streamlit as st
from dataclasses import dataclass
from typing import Dict, Callable
import base64

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Scout Financial - Pricing Calculator",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #93c5fd;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Card Styling */
    .service-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .service-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    .service-card.selected {
        border-color: #3b82f6;
        background: #eff6ff;
    }
    
    /* Tier Card Styling */
    .tier-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        height: 100%;
    }
    
    .tier-card.tier-1 { border-top: 4px solid #64748b; }
    .tier-card.tier-2 { border-top: 4px solid #3b82f6; }
    .tier-card.tier-3 { border-top: 4px solid #6366f1; }
    
    .tier-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .tier-badge.tier-1 { background: #64748b; }
    .tier-badge.tier-2 { background: #3b82f6; }
    .tier-badge.tier-3 { background: #6366f1; }
    
    /* Quote Summary Box */
    .quote-summary {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 100%);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
    }
    
    .quote-summary h3 {
        color: #93c5fd;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .quote-summary .total {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    /* Discount Badge */
    .discount-badge {
        background: #dcfce7;
        border: 1px solid #86efac;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .discount-badge h4 {
        color: #166534;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .discount-badge p {
        color: #15803d;
        margin: 0;
        font-size: 0.85rem;
    }
    
    /* Progress Steps */
    .step-indicator {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .step {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .step.active {
        background: #3b82f6;
        color: white;
    }
    
    .step.completed {
        background: #22c55e;
        color: white;
    }
    
    .step.inactive {
        background: #e2e8f0;
        color: #94a3b8;
    }
    
    /* Feature List */
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0 0;
    }
    
    .feature-list li {
        font-size: 0.8rem;
        color: #64748b;
        padding: 0.2rem 0;
    }
    
    .feature-list li::before {
        content: "✓ ";
        color: #22c55e;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Button Styling */
    .stButton > button {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Slider Styling */
    .stSlider {
        padding-top: 0.25rem;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
    }
    
    .stSlider > div > div > div > div {
        background: #1e3a5f;
        border: 2px solid white;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PRICING DATA
# ============================================================================
PRICING = {
    'bookkeeping': {
        'name': 'Bookkeeping',
        'icon': '📊',
        'description': 'Transaction categorization, reconciliation, financial statements, and reporting',
        'tiers': {
            1: {
                'name': 'Foundation',
                'response_time': '5 business days',
                'description': 'Standard monthly close, basic reporting',
                'features': ['Monthly reconciliation', 'Standard financial statements', 'Email support', 'Reports by 10th business day'],
                'get_price': lambda exp: 845 if exp <= 30000 else 1278 if exp <= 60000 else 1712 if exp <= 100000 else 2145 if exp <= 150000 else 2578 if exp <= 200000 else 3000
            },
            2: {
                'name': 'Growth',
                'response_time': '3 business days',
                'description': 'Accelerated close, enhanced reporting',
                'features': ['Weekly reconciliation', 'Custom financial reports', 'Priority email + phone', 'Reports by 6th business day', 'Cash flow analysis'],
                'get_price': lambda exp: 1100 if exp <= 30000 else 1662 if exp <= 60000 else 2226 if exp <= 100000 else 2789 if exp <= 150000 else 3352 if exp <= 200000 else 3900
            },
            3: {
                'name': 'Performance',
                'response_time': 'Same day',
                'description': 'Real-time support, controller-level insights',
                'features': ['Real-time reconciliation', 'Executive dashboards', 'Dedicated accountant', 'Same-day response', 'Strategic insights'],
                'get_price': lambda exp: 1430 if exp <= 30000 else 2161 if exp <= 60000 else 2893 if exp <= 100000 else 3625 if exp <= 150000 else 4358 if exp <= 200000 else 5070
            }
        }
    },
    'hr': {
        'name': 'HR Services',
        'icon': '👥',
        'description': 'Employee relations, compliance, handbooks, onboarding, and HR advisory',
        'tiers': {
            1: {
                'name': 'Foundation',
                'response_time': '72 hours',
                'description': 'Basic HR compliance & support',
                'weekly_base': 250,
                'per_ee': 21.67,
                'features': ['Onboarding/offboarding packets', 'Offer letter templates', 'Basic compliance support', 'Employee document library']
            },
            2: {
                'name': 'Growth',
                'response_time': '24 hours',
                'description': 'Comprehensive HR administration',
                'weekly_base': 395,
                'per_ee': 43.33,
                'features': ['Everything in Foundation', 'Benefits administration', 'Job descriptions', 'Employee handbook', 'Performance reviews']
            },
            3: {
                'name': 'Performance',
                'response_time': '4 hours',
                'description': 'Strategic HR partnership',
                'weekly_base': 595,
                'per_ee': 60.67,
                'features': ['Everything in Growth', 'Employee & manager training', 'Disciplinary actions support', 'Talent acquisition']
            }
        }
    },
    'payroll': {
        'name': 'Payroll',
        'icon': '💵',
        'description': 'Payroll processing, tax filings, direct deposit, W-2s, and time tracking',
        'tiers': {
            1: {
                'name': 'Foundation',
                'response_time': '48 hours',
                'description': 'Standard payroll processing',
                'weekly_base': 50,
                'per_ee_weekly': 5,
                'features': ['Bi-weekly/monthly payroll', 'Direct deposit', 'Tax filings', 'W-2/1099 preparation']
            },
            2: {
                'name': 'Growth',
                'response_time': '24 hours',
                'description': 'Enhanced payroll with time tracking',
                'weekly_base': 75,
                'per_ee_weekly': 7.50,
                'features': ['Everything in Foundation', 'Weekly payroll option', 'Time & attendance integration', 'PTO tracking', 'Multi-state support']
            },
            3: {
                'name': 'Performance',
                'response_time': 'Same day',
                'description': 'Full-service payroll management',
                'weekly_base': 100,
                'per_ee_weekly': 10,
                'features': ['Everything in Growth', 'On-demand pay', 'Custom reporting', 'Garnishment handling', 'Dedicated specialist']
            }
        }
    },
    'tax': {
        'name': 'Tax Services',
        'icon': '📋',
        'description': 'Corporate tax preparation, filings, planning, and year-round support',
        'tiers': {
            1: {
                'name': 'Starter',
                'response_time': '5 business days',
                'description': 'Simple tax situations',
                'annual': 750,
                'features': ['Federal corporate tax return', 'Single state filing', 'DE franchise tax', 'Tax extension filing']
            },
            2: {
                'name': 'Essentials',
                'response_time': '3 business days',
                'description': 'Growing business tax needs',
                'annual': 2450,
                'features': ['Everything in Starter', 'City tax returns', 'Up to 10 1099s included', 'Quarterly check-ins']
            },
            3: {
                'name': 'Standard',
                'response_time': '24 hours',
                'description': 'Complex tax situations',
                'annual': 5400,
                'features': ['Everything in Essentials', 'Multi-state filings', 'Up to 25 1099s included', 'Tax planning consultation']
            }
        }
    },
    'cfo': {
        'name': 'CFO Services',
        'icon': '📈',
        'description': 'Financial modeling, budgeting, forecasting, investor reporting, and strategy',
        'tiers': {
            1: {
                'name': 'Basic',
                'response_time': '48 hours',
                'description': 'Financial analysis & insights',
                'monthly': 1750,
                'features': ['Custom financial model', 'Budget vs actuals', 'KPI dashboard', 'Monthly strategy call']
            },
            2: {
                'name': 'Essentials',
                'response_time': '24 hours',
                'description': 'Growth-stage financial leadership',
                'monthly': 3150,
                'features': ['Everything in Basic', 'Cash flow optimization', 'Investor reporting', 'Fundraising support', 'Bi-weekly calls']
            },
            3: {
                'name': 'Custom',
                'response_time': '4 hours',
                'description': 'Full fractional CFO partnership',
                'monthly': 5250,
                'features': ['Everything in Essentials', '13-week cash flow forecast', 'Board presentations', 'M&A strategy', 'Weekly calls']
            }
        }
    },
    'coo': {
        'name': 'COO / Operations',
        'icon': '⚙️',
        'description': 'Business setup, banking, vendor management, and operational support',
        'tiers': {
            1: {
                'name': 'Starter',
                'response_time': '72 hours',
                'description': 'Business launch package',
                'monthly': 62.50,
                'features': ['Business incorporation', 'Banking setup', 'Payroll system setup', 'Bookkeeping setup']
            },
            2: {
                'name': 'Essentials',
                'response_time': '24 hours',
                'description': 'Ongoing operations support',
                'monthly': 500,
                'features': ['Banking support', 'HR/payroll/benefits coordination', 'Invoice collection', 'Bill payment management']
            },
            3: {
                'name': 'Custom',
                'response_time': '4 hours',
                'description': 'Full operations management',
                'monthly': 1500,
                'features': ['Everything in Essentials', 'High-volume AP/AR', 'Multi-state compliance', 'Stock administration']
            }
        }
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def format_currency(amount: float) -> str:
    """Format a number as USD currency."""
    return f"${amount:,.0f}"

def format_percent(amount: float) -> str:
    """Format a decimal as percentage."""
    return f"{amount * 100:.0f}%"

def calculate_weekly_price(service: str, tier: int, employees: int, monthly_expenses: int) -> float:
    """Calculate weekly price for a service tier."""
    tier_data = PRICING[service]['tiers'][tier]
    
    if service == 'bookkeeping':
        monthly = tier_data['get_price'](monthly_expenses)
        return monthly / 4.33
    elif service == 'hr':
        return tier_data['weekly_base'] + (tier_data['per_ee'] * employees / 4.33)
    elif service == 'payroll':
        return tier_data['weekly_base'] + (tier_data['per_ee_weekly'] * employees)
    elif service == 'tax':
        return tier_data['annual'] / 52
    else:  # cfo, coo
        return tier_data['monthly'] / 4.33

def get_auto_tax_tier(states: int, is_profitable: bool, monthly_revenue: int, 
                      has_1099s: bool, num_1099s: int, entity_type: str) -> int:
    """Auto-select minimum tax tier based on business complexity."""
    complexity = 1
    
    # Calculate annual revenue from monthly
    annual_revenue = monthly_revenue * 12
    
    if states > 1:
        complexity = max(complexity, 3)
    if is_profitable and annual_revenue > 500000:
        complexity = max(complexity, 3)
    if has_1099s and num_1099s > 10:
        complexity = max(complexity, 3)
    if has_1099s and 0 < num_1099s <= 10:
        complexity = max(complexity, 2)
    if entity_type == 'C-Corporation':
        complexity = max(complexity, 2)
    if annual_revenue > 1000000:
        complexity = max(complexity, 2)
    if annual_revenue > 5000000:
        complexity = max(complexity, 3)
    
    return min(complexity, 3)

def calculate_discounts(service_count: int, employees: int, payment_term: str) -> Dict[str, float]:
    """Calculate all applicable discounts."""
    # Bundle discount
    if service_count >= 5:
        bundle = 0.30
    elif service_count >= 4:
        bundle = 0.25
    elif service_count >= 3:
        bundle = 0.20
    elif service_count >= 2:
        bundle = 0.18
    else:
        bundle = 0
    
    # Volume discount
    if employees >= 100:
        volume = 0.30
    elif employees >= 51:
        volume = 0.20
    elif employees >= 26:
        volume = 0.15
    elif employees >= 11:
        volume = 0.10
    else:
        volume = 0
    
    # Payment term discount
    payment_discounts = {
        'Monthly': 0,
        'Quarterly (5% off)': 0.05,
        'Annual (15% off)': 0.15,
        'Multi-year (20% off)': 0.20
    }
    payment = payment_discounts.get(payment_term, 0)
    
    total = min(bundle + volume + payment, 0.40)
    
    return {
        'bundle': bundle,
        'volume': volume,
        'payment': payment,
        'total': total
    }

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'selected_services' not in st.session_state:
    st.session_state.selected_services = {s: False for s in PRICING.keys()}

if 'tiers' not in st.session_state:
    st.session_state.tiers = {s: 2 for s in PRICING.keys()}

# ============================================================================
# HEADER
# ============================================================================

# Scout Financial Owl Logo embedded as base64
LOGO_BASE64 = """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

"""

# Display header with embedded logo
st.markdown(f"""
<div class="main-header">
    <img src="data:image/png;base64,{LOGO_BASE64.strip()}" style="width: 50px; height: 50px; border-radius: 8px;">
    <div>
        <h1>Scout Financial</h1>
        <p>Pricing Calculator</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Progress indicator
cols = st.columns([1, 2, 1])
with cols[1]:
    step_html = '<div class="step-indicator">'
    for i in range(1, 4):
        if i < st.session_state.step:
            step_html += f'<div class="step completed">✓</div>'
        elif i == st.session_state.step:
            step_html += f'<div class="step active">{i}</div>'
        else:
            step_html += f'<div class="step inactive">{i}</div>'
        if i < 3:
            step_html += '<div style="width: 60px; height: 4px; background: #e2e8f0; align-self: center; border-radius: 2px;"></div>'
    step_html += '</div>'
    st.markdown(step_html, unsafe_allow_html=True)

# ============================================================================
# STEP 1: CLIENT INFORMATION
# ============================================================================
if st.session_state.step == 1:
    st.markdown("## Tell us about your business")
    st.markdown("We'll use this to recommend the right services and pricing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 Company Details")
        company_name = st.text_input("Company Name", placeholder="Your Company Inc.")
        
        industry = st.selectbox("Industry", [
            "Artists/Content Creators", "Food & Beverage", "Medical/Dental", 
            "Nonprofit", "Professional Services", "Real Estate", "Retail", "Other"
        ])
        
        entity_type = st.selectbox("Entity Type", [
            "LLC", "S-Corporation", "C-Corporation", "Partnership", 
            "Sole Proprietorship", "Nonprofit 501(c)(3)"
        ])
        
        col1a, col1b = st.columns(2)
        with col1a:
            employees = st.number_input("Number of Employees", min_value=1, value=10)
        with col1b:
            states = st.number_input("States Operating In", min_value=1, max_value=50, value=1)
    
    with col2:
        st.markdown("### 💰 Financial Information")
        
        st.markdown("**Monthly Expenses ($)**")
        monthly_expenses = st.slider(
            "Monthly Expenses", 
            min_value=0, 
            max_value=500000, 
            value=50000, 
            step=5000,
            format="$%d",
            label_visibility="collapsed"
        )
        
        st.markdown("**Average Monthly Revenue ($)**")
        monthly_revenue = st.slider(
            "Average Monthly Revenue", 
            min_value=0, 
            max_value=2000000, 
            value=50000, 
            step=5000,
            format="$%d",
            label_visibility="collapsed"
        )
        
        is_profitable = st.checkbox("Currently profitable")
        has_1099s = st.checkbox("We issue 1099s to contractors")
        
        num_1099s = 0
        if has_1099s:
            num_1099s = st.number_input("How many 1099s annually?", min_value=0, value=5)
    
    # Store in session state
    st.session_state.company_name = company_name
    st.session_state.industry = industry
    st.session_state.entity_type = entity_type
    st.session_state.employees = employees
    st.session_state.states = states
    st.session_state.monthly_expenses = monthly_expenses
    st.session_state.monthly_revenue = monthly_revenue
    st.session_state.is_profitable = is_profitable
    st.session_state.has_1099s = has_1099s
    st.session_state.num_1099s = num_1099s
    
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("Continue to Services →", type="primary", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# ============================================================================
# STEP 2: SERVICE SELECTION
# ============================================================================
elif st.session_state.step == 2:
    st.markdown("## Select your services")
    st.markdown("Choose the services you need. Bundle more to save more!")
    
    cols = st.columns(3)
    
    for idx, (service_key, service_data) in enumerate(PRICING.items()):
        with cols[idx % 3]:
            is_selected = st.session_state.selected_services[service_key]
            
            # Create a card-like container
            with st.container():
                selected_class = "selected" if is_selected else ""
                st.markdown(f"""
                <div class="service-card {selected_class}">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 2rem;">{service_data['icon']}</span>
                        <h3 style="margin: 0; font-size: 1.1rem;">{service_data['name']}</h3>
                    </div>
                    <p style="color: #64748b; font-size: 0.85rem; margin: 0;">{service_data['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.checkbox(f"Select {service_data['name']}", value=is_selected, key=f"select_{service_key}"):
                    st.session_state.selected_services[service_key] = True
                else:
                    st.session_state.selected_services[service_key] = False
    
    # Bundle discount notification
    service_count = sum(st.session_state.selected_services.values())
    if service_count >= 2:
        discount_pct = "18%" if service_count == 2 else "20%" if service_count == 3 else "25%" if service_count == 4 else "30%"
        st.markdown(f"""
        <div class="discount-badge">
            <h4>🎉 Bundle Discount Unlocked!</h4>
            <p>{service_count} services selected = {discount_pct} bundle discount</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col3:
        can_proceed = service_count > 0
        if st.button("Choose Your Tiers →" if can_proceed else "Select at least one service", 
                     type="primary" if can_proceed else "secondary", 
                     disabled=not can_proceed,
                     use_container_width=True):
            st.session_state.step = 3
            st.rerun()

# ============================================================================
# STEP 3: TIER SELECTION & SUMMARY
# ============================================================================
elif st.session_state.step == 3:
    st.markdown("## Choose your service levels")
    st.markdown("Select the tier that matches your needs for each service")
    
    # Get auto-selected tax tier
    auto_tax_tier = get_auto_tax_tier(
        st.session_state.states,
        st.session_state.is_profitable,
        st.session_state.monthly_revenue,
        st.session_state.has_1099s,
        st.session_state.num_1099s,
        st.session_state.entity_type
    )
    
    col_main, col_summary = st.columns([2, 1])
    
    with col_main:
        for service_key, is_selected in st.session_state.selected_services.items():
            if not is_selected:
                continue
            
            service_data = PRICING[service_key]
            st.markdown(f"### {service_data['icon']} {service_data['name']}")
            
            if service_key == 'tax' and auto_tax_tier > 1:
                st.warning(f"⚠️ Your business complexity requires minimum Tier {auto_tax_tier}")
            
            tier_cols = st.columns(3)
            
            for tier_num in [1, 2, 3]:
                tier_data = service_data['tiers'][tier_num]
                weekly_price = calculate_weekly_price(
                    service_key, tier_num, 
                    st.session_state.employees, 
                    st.session_state.monthly_expenses
                )
                
                with tier_cols[tier_num - 1]:
                    # Check if tier is disabled for tax
                    is_disabled = service_key == 'tax' and tier_num < auto_tax_tier
                    is_current = st.session_state.tiers[service_key] == tier_num
                    
                    st.markdown(f"""
                    <div class="tier-card tier-{tier_num}">
                        <span class="tier-badge tier-{tier_num}">TIER {tier_num}</span>
                        <h4 style="margin: 0.5rem 0;">{tier_data['name']}</h4>
                        <p style="font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">
                            {format_currency(weekly_price)}<span style="font-size: 0.9rem; color: #64748b;">/wk</span>
                        </p>
                        <p style="color: #64748b; font-size: 0.85rem;">{tier_data['description']}</p>
                        <p style="font-size: 0.8rem;"><strong>⏱️ Response:</strong> {tier_data['response_time']}</p>
                        <ul class="feature-list">
                            {''.join([f'<li>{f}</li>' for f in tier_data['features'][:4]])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if is_disabled:
                        st.button(f"Not available", key=f"tier_{service_key}_{tier_num}", disabled=True, use_container_width=True)
                    else:
                        if st.button(
                            "✓ Selected" if is_current else "Select",
                            key=f"tier_{service_key}_{tier_num}",
                            type="primary" if is_current else "secondary",
                            use_container_width=True
                        ):
                            st.session_state.tiers[service_key] = tier_num
                            st.rerun()
            
            st.markdown("---")
    
    with col_summary:
        st.markdown("### 📋 Your Quote")
        
        if st.session_state.company_name:
            st.markdown(f"**Prepared for:** {st.session_state.company_name}")
        
        # Calculate totals
        weekly_subtotal = 0
        line_items = []
        
        for service_key, is_selected in st.session_state.selected_services.items():
            if not is_selected:
                continue
            
            tier = st.session_state.tiers[service_key]
            if service_key == 'tax':
                tier = max(tier, auto_tax_tier)
            
            weekly_price = calculate_weekly_price(
                service_key, tier,
                st.session_state.employees,
                st.session_state.monthly_expenses
            )
            weekly_subtotal += weekly_price
            
            tier_name = PRICING[service_key]['tiers'][tier]['name']
            line_items.append((PRICING[service_key]['name'], tier_name, weekly_price))
        
        # Display line items
        for name, tier_name, price in line_items:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**{name}** ({tier_name})")
            with col2:
                st.markdown(f"**{format_currency(price)}**")
        
        st.markdown("---")
        
        # Subtotal
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Subtotal**")
        with col2:
            st.markdown(f"**{format_currency(weekly_subtotal)}/wk**")
        
        # Payment terms
        payment_term = st.selectbox("Payment Terms", [
            "Monthly", "Quarterly (5% off)", "Annual (15% off)", "Multi-year (20% off)"
        ])
        
        # Calculate discounts
        service_count = sum(st.session_state.selected_services.values())
        discounts = calculate_discounts(service_count, st.session_state.employees, payment_term)
        
        if discounts['total'] > 0:
            st.markdown("""
            <div class="discount-badge">
                <h4>💰 Your Savings</h4>
            """, unsafe_allow_html=True)
            
            if discounts['bundle'] > 0:
                st.markdown(f"Bundle ({service_count} services): **-{format_percent(discounts['bundle'])}**")
            if discounts['volume'] > 0:
                st.markdown(f"Volume ({st.session_state.employees} employees): **-{format_percent(discounts['volume'])}**")
            if discounts['payment'] > 0:
                st.markdown(f"Payment term: **-{format_percent(discounts['payment'])}**")
            
            discount_amount = weekly_subtotal * discounts['total']
            st.markdown(f"**Total Savings: -{format_currency(discount_amount)}/wk**")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Final totals
        weekly_total = weekly_subtotal * (1 - discounts['total'])
        monthly_total = weekly_total * 4.33
        annual_total = weekly_total * 52
        
        st.markdown(f"""
        <div class="quote-summary">
            <h3>Weekly Total</h3>
            <p class="total">{format_currency(weekly_total)}</p>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #93c5fd;">Monthly Equivalent</span>
                    <span style="font-weight: 600;">{format_currency(monthly_total)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #93c5fd;">Annual Total</span>
                    <span style="font-weight: 600;">{format_currency(annual_total)}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #93c5fd;">Per Employee/Week</span>
                    <span style="font-weight: 600;">{format_currency(weekly_total / st.session_state.employees)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("📧 Get Your Custom Quote", type="primary", use_container_width=True):
            st.success("Quote request submitted! Our team will contact you shortly.")
        
        st.caption("Final pricing confirmed after consultation")
    
    # Back button
    st.markdown("---")
    if st.button("← Back to Services"):
        st.session_state.step = 2
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    <p>© 2026 Scout Financial. All rights reserved.</p>
    <p>16 N Marengo Ave Ste 303, Pasadena, CA 91101 | 844-839-9100 | www.scoutfi.com</p>
</div>
""", unsafe_allow_html=True)
