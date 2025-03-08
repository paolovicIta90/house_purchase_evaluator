import matplotlib.pyplot as plt
from parameters_classes.static_parameters import INVESTMENT_EVALUATION_PARAMETERS
from visualization_preparation.combine_component import CombineComponents

class ProcessDataForVisualization(CombineComponents):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def prepare_component_for_visualization(self):
        
        final_component_with_transactions_user_inputs = self.create_final_component_with_transactions_user_input()
        investment_evaluation_horizon = self.investment_evaluation_parameters['investment_evaluation_horizon']
        grouped_results = final_component_with_transactions_user_inputs.groupby('year')[['house_sale_cashflow','overall_house_purchase_cashflow', 'overall_rent_cashflow', 'incremental_cashflow_rent_vs_buy', 
                                                                                        'incremental_cashflow_rent_vs_buy_reinvested', 'incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted']].sum()
        grouped_results = grouped_results.reset_index()
        grouped_results['cumulative_incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted'] = grouped_results['incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted'].cumsum()
        return grouped_results.loc[:investment_evaluation_horizon-1,:]

    def print_overall_financial_benefit(self):
        df_component_for_data_visualization = self.prepare_component_for_visualization()
        overall_financial_benefit = df_component_for_data_visualization['incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted'].sum()
        output_string = f"The overall inflation-adjusted benefit of buying a house vs renting (accounting also for cash flows reinvestment) is {overall_financial_benefit}"
        return output_string

    def plot_incremental_cashflow(self):
        """
        Generates a bar chart with:
        - X-axis: 'year' column
        - Y-axis: 'incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted' column
        """
        
        df_for_chart_visualization = self.prepare_component_for_visualization()
        plt.figure(figsize=(10, 5))
        plt.bar(df_for_chart_visualization['year'], df_for_chart_visualization['cumulative_incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted'], color='orange')
        
        plt.xlabel('Year')
        plt.ylabel('Incremental Cashflow (Inflation Adjusted)')
        plt.title('Incremental Cashflow Rent vs Buy (Reinvested & Inflation Adjusted)')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        
        plt.show()