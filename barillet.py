from iapws import iapws95
def calculate_barillet_mass_balance(QSAP,  Qsoutirage, QPAP, QC, QD, QE):
    Qentree = QSAP + Qsoutirage
    Qsortie = QPAP + QC + QD + QE
    Rm = (Qsortie / Qentree) * 100
    pertes = Qentree - Qsortie
    return Qentree, Qsortie, Rm, pertes
def calculate_barillet_energy_balance(QSAP, Qsoutirage, QPAP, QD, QC, TSAP, PSAP,  Tsoutirage, Psoutirage,  TPAP, PPAP, TC, PC, TD, PD):
    def calculate_barillet_properties(T, P):
        try:
            P_mpa = P / 10.0
            T_c = T + 273.15
            state = iapws95.IAPWS95(T=T_c, P=P_mpa)
            enthalpy = state.h  # Specific enthalpy in kJ/kg
            entropy = state.s  # Specific entropy in kJ/kg·K
            gibbs_free_energy = state.g  # Specific Gibbs free energy in kJ/kg
            density = state.rho  # Density in kg/m³
            cp = state.cp  # Specific heat capacity at constant pressure in kJ/kg·K
            cv = state.cv  # Specific heat capacity at constant volume in kJ/kg·K

            return enthalpy, entropy, gibbs_free_energy, density, cp, cv

        except ValueError as e:
            raise ValueError("Error in calculating properties:", e)

    # Calculate properties for SAP
    HSAP, entropySAP, gibbs_free_energySAP, densitySAP, cpSAP, cvSAP = calculate_barillet_properties(TSAP, PSAP)

    # Calculate properties for PAP
    HPAP, entropyPAP, gibbs_free_energyPAP, densityPAP, cpPAP, cvPAP = calculate_barillet_properties(TPAP, PPAP)
    # Calculate properties for soutirage
    Hsoutirage, entropysoutirage, gibbs_free_energysoutirage, densitysoutirage, cpsoutirage, cvsoutirage = calculate_barillet_properties(
        Tsoutirage, Psoutirage)
    # Calculate properties for condenseur
    HC, entropyC, gibbs_free_energyC, densityC, cpC, cvC = calculate_barillet_properties(TC, PC)
    # Calculate properties for Dégaseur
    HD, entropyD, gibbs_free_energyD, densityD, cpD, cvD = calculate_barillet_properties(TD, PD)

    # Calculate energy balance
    Eentree = (QSAP * HSAP + Qsoutirage * Hsoutirage ) * 1000
    Esortie = (QPAP * HPAP + QD * HD + QC * HC) * 1000
    Re = (Esortie / Eentree) * 100
    pertes = (Eentree - Esortie) / 3600
    return Eentree, Esortie, Re, pertes