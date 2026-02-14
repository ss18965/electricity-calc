import streamlit as st

st.set_page_config(page_title="2026 Electricity Calc", page_icon="⚡")

st.title("⚡ 2026 Electricity Bill Calculator")
st.markdown("### Includes Standard & Time of Use (ToU) logic")

# --- SIDEBAR: CATEGORY SELECTION ---
st.sidebar.header("1. Choose Category")
category = st.sidebar.selectbox(
    "Category",
    ["Domestic", "Religious", "Industrial (Rate 1)", "General Purpose (Rate 1)"]
)

mode = st.sidebar.radio("Calculation Mode", ["Standard (Total Units)", "Time of Use (ToU)"])

energy_charge = 0.0
fixed_charge = 0.0

# --- LOGIC: TIME OF USE (TOU) ---
if mode == "Time of Use (ToU)":
    st.info("Enter your consumption for each time slot (kWh)")
    col_a, col_b, col_c = st.columns(3)
    with col_a: day = st.number_input("Day (05:30-18:30)", min_value=0.0)
    with col_b: peak = st.number_input("Peak (18:30-22:30)", min_value=0.0)
    with col_c: off_peak = st.number_input("Off-Peak (22:30-05:30)", min_value=0.0)

    # Rates based on 2026-04-01 schedule
    if category == "Domestic":
        energy_charge = (day * 39.75) + (peak * 76.09) + (off_peak * 23.85)
        fixed_charge = 2384.76
    elif category == "Industrial (Rate 1)":
        energy_charge = (day * 17.03) + (peak * 31.80) + (off_peak * 13.63)
        fixed_charge = 5678.00 # Rate 2/3 Fixed Charge
    elif category == "General Purpose (Rate 1)":
        energy_charge = (day * 46.56) + (peak * 53.37) + (off_peak * 35.20)
        fixed_charge = 5678.00

# --- LOGIC: STANDARD ---
else:
    units = st.number_input("Total Units Consumed (kWh)", min_value=0.0, value=100.0)
    
    if category == "Domestic":
        if units <= 60:
            if units <= 30: energy_charge, fixed_charge = (units * 5.11), 90.85
            else: energy_charge, fixed_charge = (30 * 5.11) + ((units - 30) * 9.08), 238.48
        else:
            energy_charge = (60 * 14.48)
            if units <= 90: energy_charge += (units - 60) * 21.01; fixed_charge = 454.24
            elif units <= 120: energy_charge += (30 * 21.01) + (units - 90) * 27.25; fixed_charge = 1135.60
            elif units <= 180: energy_charge += (30 * 21.01) + (30 * 27.25) + (units - 120) * 46.56; fixed_charge = 1703.40
            else: energy_charge += (30 * 21.01) + (30 * 27.25) + (60 * 46.56) + (units - 180) * 69.27; fixed_charge = 2384.76

    elif category == "Religious":
        if units <= 30: energy_charge, fixed_charge = (units * 5.11), 85.17
        elif units <= 90: energy_charge, fixed_charge = (30 * 5.11) + ((units - 30) * 5.11), 227.12
        elif units <= 120: energy_charge, fixed_charge = (90 * 5.11) + ((units - 90) * 9.08), 397.46
        elif units <= 180: energy_charge, fixed_charge = (90 * 5.11) + (30 * 9.08) + ((units - 120) * 21.58), 1476.28
        else: energy_charge, fixed_charge = (90 * 5.11) + (30 * 9.08) + (60 * 21.58) + ((units - 180) * 29.53), 1930.52

    elif category == "Industrial (Rate 1)":
        if units <= 300: energy_charge, fixed_charge = (units * 9.08), 340.68
        else: energy_charge, fixed_charge = (units * 19.31), 908.48

    elif category == "General Purpose (Rate 1)":
        if units <= 180: energy_charge, fixed_charge = (units * 28.39), 567.80
        else: energy_charge, fixed_charge = (units * 38.61), 1816.96

total_bill = energy_charge + fixed_charge

# --- RESULTS ---
st.divider()
c1, c2 = st.columns(2)
c1.metric("Total Bill", f"Rs. {total_bill:,.2f}")
c2.metric("Fixed Charge", f"Rs. {fixed_charge:,.2f}")

if mode == "Time of Use (ToU)":
    st.caption("Note: ToU fixed charges are higher as they typically apply to Rate 2/3 contracts.")
  
