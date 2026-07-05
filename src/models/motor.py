class Motor():
    def __init__(self, efficiency: float, torque_constant: float) -> None:        
        self.efficiency = min(1, max(0.01, efficiency))
        self.torque_constant = torque_constant

    def torque_to_current(self, torque: float) -> float:
        #converts torque to current, for calculating power
        #formula T=kt​⋅I - T -> torque, kt -> torque constant, I -> current
        #torque constant is ratio from T/I -> how many amps are needed to create desired torque
        return torque / self.torque_constant
    
    def power(self, torque: float, omega: float) -> float:
        #omega -> winkelgeschwindigkeit des rads
        return torque * omega / self.efficiency
