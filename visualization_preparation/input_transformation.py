import numpy as np
import pandas as pd
from parameters_classes.base_structure import Base

class InputTransformation(Base):

    def __init__(self, df_transactions_user_input, house_properties, investment_evaluation_parameters, **kwargs):

        self.df_transactions_user_input = df_transactions_user_input
        self.house_properties = house_properties
        self.investment_evaluation_parameters = investment_evaluation_parameters

        super().__init__(**kwargs)



    def validate_transactions_user_input(self):

        df_transactions_user_input = self.df_transactions_user_input.dropna(how='any').copy()
        
        # Check if any row has buy >= sell
        if (self.df_transactions_user_input['buy'] >= self.df_transactions_user_input['sell']).any():
            raise ValueError("Error: There is at least one row where 'buy' is greater than or equal to 'sell'.")

        # Check if buy[i] <= sell[i-1]
        if (self.df_transactions_user_input['buy'][1:].reset_index(drop=True) <= self.df_transactions_user_input['sell'][:-1].reset_index(drop=True)).any():
            raise ValueError("Error: 'buy' at index i is less than or equal to 'sell' at index i-1.")

        # Sort by 'buy' column
        df_transactions_user_input = self.df_transactions_user_input.sort_values(by='buy').reset_index(drop=True)

        # Ensure 'transaction_id' is an increasing integer sequence starting from 1
        df_transactions_user_input['transaction_id'] = range(1, len(df_transactions_user_input) + 1)

        

        return df_transactions_user_input
        


    def convert_user_input_to_dict(self, df):
        return df.set_index('transaction_id').to_dict(orient='index')
        

    def modify_house_properties_based_on_user_input(self, transaction_id : int):

        df_transactions_user_input_validated= self.validate_transactions_user_input()
        transactions_dict = self.convert_user_input_to_dict(df_transactions_user_input_validated)
        house_properties = self.house_properties
        house_properties['transaction_id'] = transaction_id
        house_properties['purchase_year'] = transactions_dict[transaction_id]['buy']
        house_properties['year_sale'] = transactions_dict[transaction_id]['sell']

        return house_properties

    def create_transaction_schedule_dataframe_based_on_user_input(self, transaction_id: int, 
                                                                ):
        
        df_transactions_user_input_validated= self.validate_transactions_user_input()
        final_horizon = self.investment_evaluation_parameters['final_horizon']
        df_transactions_user_input_validated = df_transactions_user_input_validated.set_index('transaction_id')
        first_year_schedule = np.where(transaction_id == 1, 1, df_transactions_user_input_validated.loc[transaction_id, 'buy'].min())
        first_month_schedule = first_year_schedule*12-11
        last_year_schedule = np.where(transaction_id == df_transactions_user_input_validated.index.max(), final_horizon , df_transactions_user_input_validated.loc[transaction_id, 'sell'].max())
        last_month_schedule = last_year_schedule*12                         
        
        monthly_schedule = pd.Series(range(first_month_schedule, last_month_schedule+1))
        df=pd.DataFrame()
        df['month'] = monthly_schedule
        df['transaction_id'] = transaction_id
        
        return df