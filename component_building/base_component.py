import numpy as np
import pandas as pd
from parameters_classes.investment_evaluation_parameters import InvestmentEvaluation
from parameters_classes.purchase_transaction_costs import PurchaseTransactionCosts
from parameters_classes.static_bills_info import StaticBillsInformation
from calculations_classes.house_purchase_cashflows import HouseCashFlowCalculations


class HouseCashFlowComponent(HouseCashFlowCalculations, InvestmentEvaluation, StaticBillsInformation, PurchaseTransactionCosts):

    def __init__(self, **kwargs):
        # Call super().__init__ once with all keyword arguments.
        super().__init__(**kwargs)

    def get_static_cashflows(self) -> pd.DataFrame :
        df = pd.DataFrame()        
        df['month'] = self.get_monthly_schedule(1, self.final_horizon*12+1)
        df['transaction_id'] = [self.transaction_id] * len(df)
        df['year'] = np.ceil(df['month']/12)
        df['rent'] = round(self.current_rent*(1+self.rent_increase_pct)**(df['year']-1))
        df['house_price'] = round(self.house_price*(1+self.house_price_pct_increase)**(df['year']-1))        
        return  df
    
    def get_house_price_purchase(self):
        df_static_cashflow = self.get_static_cashflows()
        house_price_purchase = df_static_cashflow.loc[self.first_month_purchase-1, 'house_price']
        return house_price_purchase
    
    def get_house_purchase_cashflow(self):
        df = pd.DataFrame()
        df['month'] = self.get_monthly_schedule(self.first_month_purchase, self.total_number_installments+self.first_month_purchase)
        house_price_purchase = self.get_house_price_purchase()
        df['monthly_mortgage_payments'] = self.get_monthly_mortgage_payment(house_price_purchase)
        df['interest_paymnents'] = pd.Series(self.get_interests_payments(house_price_purchase))
        df['tax_benefit_interest_payment'] = round(self.tax_rate*df['interest_paymnents'])
        return df
    
    def get_house_purchase_billing_information(self, df):
        df=df.copy()
        house_price_purchase = self.get_house_price_purchase()
        df['energy_bills_monthly'] = self.energy_bills_monthly*(1+self.inflation_rate/12)**(df['month']-1)
        df['house_upkeeping_bills_monthly'] = self.house_upkeeping_bills_monthly*(1+self.inflation_rate/12)**(df['month']-1)
        df['vve_bill_monthly'] = self.vve_bill_monthly*(1+self.inflation_rate/12)**(df['month']-1)
        df['service_cost_bill_monthly'] = self.service_cost_bill_monthly*(1+self.inflation_rate/12)**(df['month']-1)
        df['other_bills_monthly'] = self.other_bills_monthly*(1+self.inflation_rate/12)**(df['month']-1)
        df['manteinance_costs_bill_monthly'] = round((self.manteinance_rate*house_price_purchase)*(1+self.inflation_rate/12)**(df['month']-1))
        return df.round(0)
    
    def get_base_house_cashflows_component(self):
        df_static_cashflows = self.get_static_cashflows()
        df_house_purchase_cashflow = self.get_house_purchase_cashflow()
        df_house_purchase_cashflow_with_bills = self.get_house_purchase_billing_information(df=df_house_purchase_cashflow)
        df_base_house_cashflow_component = df_static_cashflows.merge(df_house_purchase_cashflow_with_bills, on='month', how='left').fillna(0)    
        return df_base_house_cashflow_component

    def get_house_sale_price_cashflow(self, df):
        df['sales_cashflow'] = 0
        df.loc[self.month_sale-1,'sales_cashflow'] = round(df.loc[self.month_sale-1,'house_price']*(1-self.sales_commission))
        return df
    
    def get_rent_billing_information(self, df):
        df=df.copy()
        df['rent_energy_bills_monthly'] = round(self.rent_energy_bills_monthly*(1+self.inflation_rate)**(df['year']-1))
        df['rent_house_upkeeping_bills_monthly'] = round(self.rent_house_upkeeping_bills_monthly*(1+self.inflation_rate)**(df['year']-1))
        df['rent_other_bills_monthly'] = round(self.rent_other_bills_monthly*(1+self.inflation_rate)**(df['year']-1))
        
        return df
    
    def get_ground_lease_information(self, df):
        
        if self.ground_lease_year_start <= self.final_horizon:
            month_start_ground_lease = self.ground_lease_year_start*12-11            
            df['ground_lease_monthly_cost'] = 0
            df.loc[month_start_ground_lease-1:self.month_sale-1, 'ground_lease_monthly_cost'] = self.ground_lease_monthly
        else:
            df['ground_lease_monthly_cost'] = 0
        
        return df

    
    def get_purchase_transaction_cost(self, df):
        df=df.copy()
        df[['notary_cost', 'mortgage_advisor_cost', 'real_estate_agent_cost',
            'moving_costs', 'property_transfer_tax_cost']] = 0
        
        df.loc[self.first_month_purchase-1, 'notary_cost'] = self.notary_cost
        df.loc[self.first_month_purchase-1, 'mortgage_advisor_cost'] = self.mortgage_advisor_cost
        df.loc[self.first_month_purchase-1, 'real_estate_agent_cost'] = self.real_estate_agent_cost
        df.loc[self.first_month_purchase-1, 'property_transfer_tax_cost'] = round(self.property_transfer_tax_pct* df.loc[self.first_month_purchase-1, 'house_price'])
        
        return df
    
    def get_enriched_house_cashflow_component(self):
        enriched_house_cashflow_component = self.get_base_house_cashflows_component()
        enriched_house_cashflow_component = self.get_house_sale_price_cashflow(enriched_house_cashflow_component)
        enriched_house_cashflow_component = self.get_rent_billing_information(enriched_house_cashflow_component)
        enriched_house_cashflow_component = self.get_ground_lease_information(enriched_house_cashflow_component)
        enriched_house_cashflow_component = self.get_purchase_transaction_cost(enriched_house_cashflow_component)
        return enriched_house_cashflow_component
