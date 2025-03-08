import pandas as pd
from parameters_classes.house_properties import HouseProperties

class HouseCashFlowCalculations (HouseProperties):
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
 

    def get_yearly_schedule(self, initial_year, final_year):

        yearly_schedule = pd.Series(range(initial_year, final_year+1))

        return yearly_schedule

   

    def get_monthly_schedule (self, initial_month, final_month):

        yearly_schedule = pd.Series(range(initial_month, final_month))

        return yearly_schedule

   

    def get_monthly_mortgage_payment(self, house_price_purchase_year):

        mortgage_principal = house_price_purchase_year - self.initial_equity_financing

        monthly_payment = (mortgage_principal * self.monthly_mortgage_rate * (1+self.monthly_mortgage_rate)**self.total_number_installments)/(((1+self.monthly_mortgage_rate)**self.total_number_installments)-1)

        return round(monthly_payment)

    def get_interests_payments (self, house_price_purchase_year):
            
            monthly_mortgage_payment = self.get_monthly_mortgage_payment(house_price_purchase_year)

            mortgage_principal = house_price_purchase_year - self.initial_equity_financing

            first_interest_payment = round(mortgage_principal * self.monthly_mortgage_rate)

            first_principal_repayment = monthly_mortgage_payment - first_interest_payment

            interest_payment_list = [first_interest_payment]

            principal_repayment_list = [first_principal_repayment]


            for i in range(1,self.total_number_installments):

                interest_payment_list.append(round((mortgage_principal - sum(principal_repayment_list[:i]))*self.monthly_mortgage_rate))

                principal_repayment_list.append(monthly_mortgage_payment - interest_payment_list[i])

            return interest_payment_list
