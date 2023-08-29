# bache.py

from iapws import iapws95

def calculate_bache_properties(T, P):
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

def calculate_bache_mass_balance(QBPB, Qpolissage, QSAP, Qdésurchauffe):
    Qentree_bache = QBP + Qpolissage
    Qsortie_bache = QSAP + Qdésurchauffe
    Rm_bache = (Qsortie_bache / Qentree_bache) * 100
    pertes_bache = Qentree_bache - Qsortie_bache

    # Return the calculated results as a dictionary
    mass_balance_results = {
        'Qentree_bache': Qentree_bache,
        'Qsortie_bache': Qsortie_bache,
        'Rm_bache': Rm_bache,
        'pertes_bache': pertes_bache
    }
    return mass_balance_results

def calculate_bache_energy_balance(QBPB,  Qpolissage, QSAP, Qdésurchauffe, TBPB, PBPB,  TSAP, PSAP, Tdésurchauffe, Pdésurchauffe, Tpolissage, Ppolissage):
    HBPB, entropyBPB, gibbs_free_energyBPB, densityBPB, cpBPB, cvBPB = calculate_bache_properties(TBPB, PBPB)

    HSAP, entropySAP, gibbs_free_energySAP, densitySAP, cpSAP, cvSAP = calculate_bache_properties(TSAP, PSAP)
    Hdésurchauffe, entropydésurchauffe, gibbs_free_energydésurchauffe, densitydésurchauffe, cpdésurchauffe, cvdésurchauffe = calculate_bache_properties(Tdésurchauffe, Pdésurchauffe)
    Hpolissage, entropypolissage, gibbs_free_energypolissage, densitypolissage, cppolissage, cvpolissage = calculate_bache_properties(Tpolissage, Ppolissage)

    Eentree_bache = (QBPB * HBPB * 1000) +  (Qpolissage * Hpolissage * 1000)
    Esortie_bache = (QSAP * HSAP * 1000) + (Qdésurchauffe * Hdésurchauffe * 1000)
    Re_bache = (Esortie_bache / Eentree_bache) * 100
    pertes_bache_energy = (Eentree_bache - Esortie_bache) / 3600

    # Return the calculated results as a dictionary
    energy_balance_results = {
        'Eentree_bache': Eentree_bache,
        'Esortie_bache': Esortie_bache,
        'Re_bache': Re_bache,
        'pertes_bache_energy': pertes_bache_energy
    }
    return energy_balance_results


