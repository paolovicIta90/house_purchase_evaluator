from parameters_classes.base_structure import Base

class PurchaseTransactionCosts(Base):
    
    def __init__(self, notary_cost, mortgage_advisor_cost, real_estate_agent_cost, moving_costs, property_transfer_tax_pct, **kwargs):
        
        self.notary_cost = notary_cost
        
        self.mortgage_advisor_cost = mortgage_advisor_cost
        
        self.real_estate_agent_cost = real_estate_agent_cost
        
        self.moving_costs = moving_costs
        
        self.property_transfer_tax_pct = property_transfer_tax_pct
        
        super().__init__(**kwargs)