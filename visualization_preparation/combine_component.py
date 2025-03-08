import pandas as pd
from component_building.enriched_component import FinancialEnrichment
from visualization_preparation.input_transformation import InputTransformation



class CombineComponents(InputTransformation):
    
    def __init__(self, manteinance_information, purchase_transaction_costs, **kwargs):               
        self.manteinance_information = manteinance_information
        self.purchase_transaction_costs = purchase_transaction_costs
        super().__init__(**kwargs)

    def create_enriched_component_instance(self, transaction_id: int) -> FinancialEnrichment:
        house_properties = self.modify_house_properties_based_on_user_input(transaction_id)
        combined_parameters = {**house_properties, **self.investment_evaluation_parameters, **self.manteinance_information, **self.purchase_transaction_costs}
        house_cashflow_financially_enriched_instance = FinancialEnrichment(**combined_parameters)
        
        return house_cashflow_financially_enriched_instance

    def create_final_component_with_transactions_user_input(self):

        df_transactions_user_input_validated= self.validate_transactions_user_input()

        combined_components = pd.concat([self.create_enriched_component_instance(transaction_id).get_enriched_component_financial_information() for transaction_id in df_transactions_user_input_validated['transaction_id'].unique()]).reset_index(drop=True)

        combined_yearly_schedule = pd.concat([self.create_transaction_schedule_dataframe_based_on_user_input(transaction_id) for transaction_id in df_transactions_user_input_validated['transaction_id'].unique()]).reset_index(drop=True)

        final_component_with_transactions_user_inputs = combined_yearly_schedule.merge(combined_components, on=['month', 'transaction_id'], how='inner')

        return final_component_with_transactions_user_inputs

    
