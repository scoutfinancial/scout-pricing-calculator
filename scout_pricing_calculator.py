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

def get_auto_tax_tier(states: int, is_profitable: bool, annual_revenue: int, 
                      has_1099s: bool, num_1099s: int, has_foreign_ops: bool, 
                      entity_type: str) -> int:
    """Auto-select minimum tax tier based on business complexity."""
    complexity = 1
    
    if states > 1:
        complexity = max(complexity, 3)
    if is_profitable and annual_revenue > 500000:
        complexity = max(complexity, 3)
    if has_1099s and num_1099s > 10:
        complexity = max(complexity, 3)
    if has_1099s and 0 < num_1099s <= 10:
        complexity = max(complexity, 2)
    if has_foreign_ops:
        complexity = 3
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
st.markdown("""
<div class="main-header">
    <div style="font-size: 2.5rem;">🦉</div>
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
            "Professional Services", "Technology / SaaS", "Healthcare", 
            "Retail / E-commerce", "Manufacturing", "Construction", 
            "Nonprofit", "Other"
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
        monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=50000, step=5000)
        annual_revenue = st.number_input("Annual Revenue ($)", min_value=0, value=500000, step=25000)
        
        is_profitable = st.checkbox("Currently profitable")
        has_1099s = st.checkbox("We issue 1099s to contractors")
        
        num_1099s = 0
        if has_1099s:
            num_1099s = st.number_input("How many 1099s annually?", min_value=0, value=5)
        
        has_foreign_ops = st.checkbox("We have international operations")
    
    # Store in session state
    st.session_state.company_name = company_name
    st.session_state.industry = industry
    st.session_state.entity_type = entity_type
    st.session_state.employees = employees
    st.session_state.states = states
    st.session_state.monthly_expenses = monthly_expenses
    st.session_state.annual_revenue = annual_revenue
    st.session_state.is_profitable = is_profitable
    st.session_state.has_1099s = has_1099s
    st.session_state.num_1099s = num_1099s
    st.session_state.has_foreign_ops = has_foreign_ops
    
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
        st.session_state.annual_revenue,
        st.session_state.has_1099s,
        st.session_state.num_1099s,
        st.session_state.has_foreign_ops,
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
