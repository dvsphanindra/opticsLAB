from polarization.component_definitions import Linear_Polariser, StateofPolarization, Generic_Waveplate

def polarimeter(deltaR1, thetaR1, deltaLCR1, thetaLCR1, deltaR2, thetaR2, deltaLCR2, thetaLCR2, thetaP1):
	R1 = Generic_Waveplate(name="R1", delta=deltaR1, theta=thetaR1)
	LCR1 = Generic_Waveplate(name="LCR1", delta=deltaLCR1, theta=thetaLCR1)
	R2 = Generic_Waveplate(name="R2", delta=deltaR2, theta=thetaR2)
	LCR2 = Generic_Waveplate(name="LCR2", delta=deltaLCR2, theta=thetaLCR2)
	P1 = Linear_Polariser(name="P1", theta=thetaP1)
	

