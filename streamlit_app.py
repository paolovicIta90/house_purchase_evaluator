import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from calculations_classes.house_purchase_cashflows import HouseCashFlowCalculations
from component_building.base_component import HouseCashFlowComponent
from component_building.enriched_component import FinancialEnrichment
from parameters_classes.static_parameters import (HOUSE_PROPERTIES, INVESTMENT_EVALUATION_PARAMETERS, MANTEINANCE_INFORMATION, PURCHASE_TRANSACTION_COSTS)
from visualization_preparation.combine_component import CombineComponents
from visualization_preparation.process_data_for_visualization import ProcessDataForVisualization



# Create copies of the static dictionaries (we use lowercase names)
house_properties = HOUSE_PROPERTIES
investment_evaluation_parameters = INVESTMENT_EVALUATION_PARAMETERS
manteinance_information = MANTEINANCE_INFORMATION
purchase_transaction_costs = PURCHASE_TRANSACTION_COSTS

# Title of the Streamlit App
st.title("Real Estate Investment Analysis")

st.set_option('deprecation.showPyplotGlobalUse', False)


# Table for User Input - Top Center
st.subheader("Transaction Data Input")
def default_transaction_data():
    return pd.DataFrame({
        'transaction_id': [1, 2],
        'buy': [1, 8],
        'sell': [7, 45]
    })
df_transactions_user_input = st.data_editor(default_transaction_data(), num_rows="dynamic")
unique_sell_values = sorted(df_transactions_user_input['sell'].unique())



# Create two columns in the sidebar
left_col, right_col = st.sidebar.columns(2)

# --- Left Sidebar: Property & Expenses ---
with left_col:
    st.header("Property & Expenses")
    house_price = st.number_input("House Price", value=house_properties['house_price'])
    mortgage_rate = st.number_input("Mortgage Rate (%)", value=house_properties['mortgage_rate'])
    initial_equity_financing = st.number_input("Initial Equity Financing", value=house_properties['initial_equity_financing'])
    
    energy_bills_monthly = st.number_input("Energy Bills Monthly", value=manteinance_information['energy_bills_monthly'])
    vve_bill_monthly = st.number_input("VVE Bill Monthly", value=manteinance_information['vve_bill_monthly'])
    service_cost_bill_monthly = st.number_input("Service Cost Bill Monthly", value=manteinance_information['service_cost_bill_monthly'])
    ground_lease_monthly = st.number_input("Ground Lease Monthly", value=manteinance_information['ground_lease_monthly'])
    ground_lease_year_start = st.number_input("Ground Lease Year Start", value=manteinance_information['ground_lease_year_start'])
    manteinance_rate_input = st.number_input("Maintenance Rate", value=manteinance_information['manteinance_rate'])
    other_bills_monthly = st.number_input("Other Bills Monthly", value=manteinance_information['other_bills_monthly'])
    rent_energy_bills_monthly = st.number_input("Rent Energy Bills Monthly", value=manteinance_information['rent_energy_bills_monthly'])
    rent_house_upkeeping_bills_monthly = st.number_input("Rent House Upkeeping Bills Monthly", value=manteinance_information['rent_house_upkeeping_bills_monthly'])
    rent_other_bills_monthly = st.number_input("Rent Other Bills Monthly", value=manteinance_information['rent_other_bills_monthly'])

# --- Right Sidebar: Investment Evaluation ---
with right_col:
    st.header("Investment Evaluation")
    investment_evaluation_horizon = st.selectbox("Investment Evaluation Horizon", unique_sell_values)
    final_horizon = st.number_input("Final Horizon", value=investment_evaluation_parameters['final_horizon'])
    alternative_investments_return = st.number_input("Alternative Investments Return", value=investment_evaluation_parameters['alternative_investments_return'])
    house_price_pct_increase = st.number_input("House Price % Increase", value=investment_evaluation_parameters['house_price_pct_increase'])
    tax_rate = st.number_input("Tax Rate", value=investment_evaluation_parameters['tax_rate'])
    rent_increase_pct = st.number_input("Rent Increase %", value=investment_evaluation_parameters['rent_increase_pct'])
    inflation_rate = st.number_input("Inflation Rate", value=investment_evaluation_parameters['inflation_rate'])

# --- Update the dictionaries with the user inputs ---
house_properties['house_price'] = house_price
house_properties['mortgage_rate'] = mortgage_rate
house_properties['initial_equity_financing'] = initial_equity_financing

manteinance_information['energy_bills_monthly'] = energy_bills_monthly
manteinance_information['vve_bill_monthly'] = vve_bill_monthly
manteinance_information['service_cost_bill_monthly'] = service_cost_bill_monthly
manteinance_information['ground_lease_monthly'] = ground_lease_monthly
manteinance_information['ground_lease_year_start'] = ground_lease_year_start
manteinance_information['manteinance_rate'] = manteinance_rate_input
manteinance_information['other_bills_monthly'] = other_bills_monthly
manteinance_information['rent_energy_bills_monthly'] = rent_energy_bills_monthly
manteinance_information['rent_house_upkeeping_bills_monthly'] = rent_house_upkeeping_bills_monthly
manteinance_information['rent_other_bills_monthly'] = rent_other_bills_monthly

investment_evaluation_parameters['investment_evaluation_horizon'] = investment_evaluation_horizon
investment_evaluation_parameters['final_horizon'] = final_horizon
investment_evaluation_parameters['alternative_investments_return'] = alternative_investments_return
investment_evaluation_parameters['house_price_pct_increase'] = house_price_pct_increase
investment_evaluation_parameters['tax_rate'] = tax_rate
investment_evaluation_parameters['rent_increase_pct'] = rent_increase_pct
investment_evaluation_parameters['inflation_rate'] = inflation_rate



# Bottom Center - Visualization Placeholder
st.subheader("Investment Analysis Results")
st.write("Results will be displayed here after processing.")
data_visualization_instance = ProcessDataForVisualization(
    manteinance_information=manteinance_information,
    purchase_transaction_costs=purchase_transaction_costs,
    df_transactions_user_input=df_transactions_user_input,
    house_properties=house_properties,
    investment_evaluation_parameters=investment_evaluation_parameters
)
st.write(data_visualization_instance.print_overall_financial_benefit())
fig = data_visualization_instance.plot_incremental_cashflow()
st.pyplot(fig)