import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Electricity Bill Calculator 2026", page_icon="⚡", layout="centered")

st.title("⚡ Electricity Bill Calculator")
st.markdown("Calculated using the **April 01, 2026** Tariff Schedule.")

# --- SIDEBAR FOR INPUTS ---
st.sidebar.header("Calculation Settings")

category = st.sidebar.selectbox(
    "Select Consumer Category",
    ["Domestic", "Religious & Charitable", "Industrial", "General Purpose"]
)

mode = st.sidebar.radio(
    "Select Calculation Mode",
    ["Normal (Monthly Units)", "Time of Use (ToU)"]
)

# --- CALCULATION LOGIC ---
energy_charge = 0.0
fixed_charge = 0.0

if mode == "Normal (Monthly Units)":
    units = st.number_input("Total Units Consumed (kWh)", min_value=0.0, value=120.0, step=1.0)
    
    if category == "Domestic":
        if units <= 60:
            if units <= 30:
                energy_charge, fixed_charge = (units * 5.11), 90.85
            else:
                energy_charge = (30 * 5.11) + ((units - 30) * 9.08)
                fixed_charge = 238.48
        else:
            # Consumption above 60 kWh
            if units <= 90:
                energy_charge = (60 * 14.48) + ((units - 60) * 21.01)
                fixed_charge = 454.24
            elif units <= 120:
                energy_charge = (60 * 14.48) + (30 * 21.01) + ((units - 90) * 27.25)
                fixed_charge = 1135.60
            elif units <= 180:
                energy_charge = (60 * 14.48) + (30 * 21.01) + (30 * 27.25) + ((units - 120) * 46.56)
                fixed_charge = 1703.40
            else:
                energy_charge = (60 * 14.48) + (30 * 21.01) + (30 * 27.25) + (60 * 46.56) + ((units - 180) * 69.27)
                fixed_charge = 2384.76

    elif category == "Religious & Charitable":
        if units <= 30: energy_charge, fixed_charge = (units * 5.11), 85.17
        elif units <= 90: energy_charge = (30 * 5.11) + ((units - 30) * 5.11); fixed_charge = 227.12
        elif units <= 120: energy_charge = (90 * 5.11) + ((units - 90) * 9.08); fixed_charge = 397.46
        elif units <= 180: energy_charge = (90 * 5.11) + (30 * 9.08) + ((units - 120) * 21.58); fixed_charge = 1476.28
        else: energy_charge = (90 * 5.11) + (30 * 9.08) + (60 * 21.58) + ((units - 180) * 29.53); fixed_charge = 1930.52

    elif category == "Industrial":
        # Using Rate 1 (Supply < 42kVA)
        if units <= 300: energy_charge, fixed_charge = (units * 9.08), 340.68
        else: energy_charge, fixed_charge = (units * 19.31), 908.48

    elif category == "General Purpose":
        # Using Rate 1 (Supply < 42kVA)
        if units <= 180: energy_charge, fixed_charge = (units * 28.39), 567.80
        else: energy_charge, fixed_charge = (units * 38.61), 1816.96

else: # TIME OF USE MODE
    st.info("Input units used during specific time windows.")
    col1, col2, col3 = st.columns(3)
    with col1: day_u = st.number_input("Day (05:30-18:30)", min_value=0.0)
    with col2: peak_u = st.number_input("Peak (18:30-22:30)", min_value=0.0)
    with col3: off_u = st.number_input("Off-Peak (22:30-05:30)", min_value=0.0)

    if category == "Domestic":
        energy_charge = (day_u * 39.75) + (peak_u * 76.09) + (off_u * 23.85)
        fixed_charge = 2384.76
    elif category == "Industrial":
        energy_charge = (day_u * 17.03) + (peak_u * 31.80) + (off_u * 13.63)
        fixed_charge = 5678.00
    elif category == "General Purpose":
        energy_charge = (day_u * 46.56) + (peak_u * 53.37) + (off_u * 35.20)
        fixed_charge = 5678.00
    else:
        st.warning("ToU is not typically applicable to Religious categories in this schedule.")

total_bill = energy_charge + fixed_charge

# --- DISPLAYING THE RESULTS ---
st.divider()
st.subheader("Bill Breakdown")

res_col1, res_col2 = st.columns(2)
res_col1.metric("Total Bill (Rs.)", f"{total_bill:,.2f}")
res_col2.metric("Fixed Charge (Rs.)", f"{fixed_charge:,.2f}")

# Visualizing the cost split
if total_bill > 0:
    chart_data = pd.DataFrame({
        "Component": ["Energy Charge", "Fixed Charge"],
        "Amount": [energy_charge, fixed_charge]
    })
    st.bar_chart(chart_data, x="Component", y="Amount")

st.caption("Note: This calculation is based on the 2026-04-01 Tariff values provided in your document.")
