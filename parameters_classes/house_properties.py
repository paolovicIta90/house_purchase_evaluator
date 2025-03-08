from parameters_classes.base_structure import Base

class HouseProperties(Base):   

    def __init__(self, current_rent, house_price, purchase_year, mortgage_rate, 
                 mortgage_term, transaction_id, year_sale, initial_equity_financing = 0, **kwargs):
       

        self.house_price  = house_price

        self.purchase_year  = purchase_year

        self.mortgage_rate = mortgage_rate

        self.mortgage_term = mortgage_term

        self.initial_equity_financing = initial_equity_financing

        self.current_rent = current_rent

        self.mortgage_principal = self.house_price - self.initial_equity_financing

        self.total_number_installments = self.mortgage_term * 12

        self.monthly_mortgage_rate = self.mortgage_rate/12

        self.transaction_id = transaction_id

        self.first_month_purchase = self.purchase_year*12-11

        self.year_sale = year_sale

        self.month_sale = year_sale*12

        self.sales_commission = 0.02

        super().__init__(**kwargs)