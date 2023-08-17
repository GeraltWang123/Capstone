import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import numpy_financial as npf

# Set Matplotlib backend to 'Agg'
plt.switch_backend('Agg')

# 定义年收入和WACC
annual_revenue = 2.2e9  # Updated value in EUR
WACC = 0.1014

def compute_NPV(capital_cost, operating_cost, revenue, discount_rate, years=30):
    cash_flows = [-capital_cost] + [(revenue - operating_cost) for _ in range(years)]
    discounted_cash_flows = [cf / ((1 + discount_rate)**i) for i, cf in enumerate(cash_flows)]
    return sum(discounted_cash_flows)

def compute_IRR(capital_cost, operating_cost, revenue, years=30):
    cash_flows = [-capital_cost] + [(revenue - operating_cost) for _ in range(years)]
    return npf.irr(cash_flows)

def compute_metrics_over_lifetime(lifetime, capital_cost, operating_cost):
    npvs = [compute_NPV(capital_cost, operating_cost, annual_revenue, WACC, years=year) for year in lifetime]
    irrs = [compute_IRR(capital_cost, operating_cost, annual_revenue, years=year) for year in lifetime]
    return npvs, irrs

def plot_NPV_IRR_lifetime_years(capital_cost, operating_cost, years):
    lifetime = np.arange(1, years + 1)  
    npvs, irrs = compute_metrics_over_lifetime(lifetime, capital_cost, operating_cost)
    
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot NPV over lifetime
    axs[0].plot(lifetime, npvs, '-o', color='b', label='NPV')
    axs[0].axhline(0, color='black', linewidth=0.5)
    axs[0].set_title(f'Net Present Value over {years} Years')
    axs[0].set_xlabel('Lifetime (Years)')
    axs[0].set_ylabel('NPV in EUR')
    axs[0].grid(True)
    
    # Plot IRR over lifetime
    axs[1].plot(lifetime, np.array(irrs)*100, '-o', color='g', label='IRR')
    axs[1].axhline(0, color='black', linewidth=0.5)
    axs[1].set_title(f'Internal Rate of Return over {years} Years')
    axs[1].set_xlabel('Lifetime (Years)')
    axs[1].set_ylabel('IRR (%)')
    axs[1].grid(True)
    
    plt.tight_layout()
    st.pyplot(fig)

# Streamlit UI
st.title("NPV and IRR Calculator over Lifetime")

# Updated default values for sliders
capital_cost = st.slider('Capital Cost:', min_value=5e9, max_value=15e9, value=11.3502436e9, step=1e8)
operating_cost = st.slider('Operating Cost (Annual):', min_value=1e9, max_value=3e9, value=1.18525428e9, step=1e7)
years = st.slider('Lifetime (Years):', min_value=1, max_value=50, value=30)

plot_NPV_IRR_lifetime_years(capital_cost, operating_cost, years)
