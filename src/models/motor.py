class Motor:
    def __init__(self, efficiency: float, torque_constant: float) -> None:
        self.efficiency = min(1.0, max(0.01, efficiency))
        self.torque_constant = torque_constant

    def torque_to_current(self, torque: float) -> float:
        # converts torque to current, for calculating power
        # formula T = kt * I  ->  I = T / kt
        ideal_current = torque / self.torque_constant
        
        if torque > 0:
            # Fahren: Motor zieht Strom (Verluste aufschlagen)
            return ideal_current / self.efficiency
        else:
            # Rekuperieren: Motor wirkt als Generator (Verluste abziehen)
            return ideal_current * self.efficiency

    def power(self, torque: float, omega: float) -> float:
        # omega -> winkelgeschwindigkeit des rads
        mech_power = torque * omega
        
        if torque > 0:
            return mech_power / self.efficiency
        else:
            return mech_power * self.efficiency