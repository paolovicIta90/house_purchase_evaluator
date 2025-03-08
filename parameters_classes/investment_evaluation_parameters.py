from parameters_classes.base_structure import Base

class InvestmentEvaluation(Base):   

    def __init__(self, investment_evaluation_horizon, final_horizon, alternative_investments_return, 
                 house_price_pct_increase, tax_rate, rent_increase_pct, inflation_rate, **kwargs):
 
        self.investment_evaluation_horizon  = investment_evaluation_horizon

        self.final_horizon  = final_horizon

        self.alternative_investments_return = alternative_investments_return

        self.house_price_pct_increase = house_price_pct_increase

        self.tax_rate = tax_rate

        self.rent_increase_pct = rent_increase_pct

        self.inflation_rate = inflation_rate

        super().__init__(**kwargs)