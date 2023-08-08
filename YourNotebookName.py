#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import numpy_financial as npf

# Set Matplotlib backend to 'Agg'
plt.switch_backend('Agg')

# 定义年收入和WACC
annual_revenue = 2.25e9  # in EUR
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
    
    plt.figure(figsize=(14, 6))
    
    # Plot NPV over lifetime
    plt.subplot(1, 2, 1)
    plt.plot(lifetime, npvs, '-o', color='b', label='NPV')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.title(f'Net Present Value over {years} Years')
    plt.xlabel('Lifetime (Years)')
    plt.ylabel('NPV in EUR')
    plt.grid(True)
    
    # Plot IRR over lifetime
    plt.subplot(1, 2, 2)
    plt.plot(lifetime, np.array(irrs)*100, '-o', color='g', label='IRR')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.title(f'Internal Rate of Return over {years} Years')
    plt.xlabel('Lifetime (Years)')
    plt.ylabel('IRR (%)')
    plt.grid(True)
    
    plt.tight_layout()
    st.pyplot()

# Streamlit UI
st.title("NPV and IRR Calculator over Lifetime")

capital_cost = st.slider('Capital Cost:', min_value=5e9, max_value=15e9, value=9.349e9, step=1e8)
operating_cost = st.slider('Operating Cost (Annual):', min_value=1e9, max_value=3e9, value=1.6e9, step=1e7)
years = st.slider('Lifetime (Years):', min_value=1, max_value=50, value=30)

plot_NPV_IRR_lifetime_years(capital_cost, operating_cost, years)


# In[ ]:




