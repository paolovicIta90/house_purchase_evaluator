import numpy as np
from component_building.base_component import HouseCashFlowComponent

class FinancialEnrichment(HouseCashFlowComponent):

    """A class that will enrich the dataframe with financial calculations
    such as the effect of inflation and the total incremental benefit of 
    buying vs renting"""

    def __init__(self, **kwargs):
        # Call super().__init__ once with all keyword arguments.
        super().__init__(**kwargs)

    def get_house_equity(self, df):
        # enriched_house_cashflow_component = self.get_enriched_house_cashflow_component()
        df['principal_repayment'] = df['monthly_mortgage_payments'] - df['interest_paymnents']
        df['cumulative_principal_repayment'] = df['principal_repayment'].cumsum()
        house_price_purchase = self.get_house_price_purchase()
        df['house_equity'] = round(df['cumulative_principal_repayment'] + df['house_price'] - house_price_purchase + self.initial_equity_financing)
        return df
    
    def get_overall_house_purchase_cashflow(self, df):
        
        house_sale_cashflow = df.loc[self.month_sale-1, 'house_equity'] - round(df.loc[self.month_sale-1, 'house_price']*(self.sales_commission))
        
        df['house_sale_cashflow'] = 0
        df['initial_equity_financing'] = 0        
        df.loc[self.month_sale-1, 'house_sale_cashflow'] = house_sale_cashflow
        df.loc[self.first_month_purchase-1, 'initial_equity_financing'] = self.initial_equity_financing
        df['total_transaction_costs'] = df['notary_cost'] + df['mortgage_advisor_cost'] + df['real_estate_agent_cost'] + df['moving_costs'] + df['property_transfer_tax_cost']
        
        df['total_house_recurring_costs'] = df['energy_bills_monthly'] + df['house_upkeeping_bills_monthly'] + df['vve_bill_monthly'] + df['service_cost_bill_monthly'] + df['other_bills_monthly'] + df['manteinance_costs_bill_monthly']
        
        df['overall_house_purchase_cashflow'] = -df['monthly_mortgage_payments'] + df['house_sale_cashflow'] - df['total_transaction_costs'] - df['total_house_recurring_costs'] + df['tax_benefit_interest_payment'] - df['initial_equity_financing']

        return df
    
    def get_overall_rent_cashflow(self,df):
        df['overall_rent_cashflow'] = df['rent'] + df['rent_energy_bills_monthly'] + df['rent_other_bills_monthly'] + df['rent_house_upkeeping_bills_monthly']
        return df
    
    def get_incremental_cashflow_buy_vs_rent(self, df):        
        df['incremental_cashflow_rent_vs_buy'] = np.where(df['year'] < self.purchase_year, 0,df['overall_rent_cashflow'] + df['overall_house_purchase_cashflow'])
        return df
    
    def get_reinvestment_adjustment_for_incremental_cashflow(self, df):
        df['incremental_cashflow_rent_vs_buy_reinvested'] = round(df['incremental_cashflow_rent_vs_buy']*(1+self.alternative_investments_return/12)**(self.investment_evaluation_horizon*12 - df['month']),0)
        return df

    def get_inflation_adjustment_for_incremental_cashflow(self, df):
        df['incremental_cashflow_rent_vs_buy_reinvested_inflation_adjusted'] = round(df['incremental_cashflow_rent_vs_buy_reinvested']/((1+self.inflation_rate/12)**(self.investment_evaluation_horizon*12)),0)
        return df.round(0)
    
    def get_enriched_component_financial_information(self):
        
        enriched_component_financial_information = self.get_enriched_house_cashflow_component()
        
        enriched_component_financial_information = self.get_house_equity(enriched_component_financial_information)
                
        enriched_component_financial_information = self.get_overall_house_purchase_cashflow(enriched_component_financial_information)

        enriched_component_financial_information = self.get_overall_rent_cashflow(enriched_component_financial_information)

        enriched_component_financial_information = self.get_incremental_cashflow_buy_vs_rent(enriched_component_financial_information)
        
        enriched_component_financial_information = self.get_reinvestment_adjustment_for_incremental_cashflow(enriched_component_financial_information)
        
        enriched_component_financial_information = self.get_inflation_adjustment_for_incremental_cashflow(enriched_component_financial_information)
        return enriched_component_financial_information