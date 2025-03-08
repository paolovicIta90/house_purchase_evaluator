from parameters_classes.base_structure import Base

class StaticBillsInformation(Base):
    def __init__(self,
                 energy_bills_monthly,
                 house_upkeeping_bills_monthly,
                 manteinance_rate,
                 vve_bill_monthly,
                 service_cost_bill_monthly,
                 other_bills_monthly,
                 ground_lease_monthly,
                 ground_lease_year_start,
                 rent_energy_bills_monthly,
                 rent_house_upkeeping_bills_monthly,
                 rent_other_bills_monthly,
                 **kwargs):
        
        self.energy_bills_monthly = energy_bills_monthly
        self.house_upkeeping_bills_monthly = house_upkeeping_bills_monthly
        self.manteinance_rate = manteinance_rate
        self.vve_bill_monthly = vve_bill_monthly
        self.service_cost_bill_monthly = service_cost_bill_monthly
        self.ground_lease_monthly = ground_lease_monthly
        self.ground_lease_year_start = ground_lease_year_start
        self.other_bills_monthly = other_bills_monthly
        self.rent_energy_bills_monthly = rent_energy_bills_monthly
        self.rent_house_upkeeping_bills_monthly = rent_house_upkeeping_bills_monthly
        self.rent_other_bills_monthly = rent_other_bills_monthly

        super().__init__(**kwargs)