from iapws import iapws95


def calculer_efficacite_gta(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha):
    def calculer_proprietes_efficacite_gta(T, P):
        try:
            P_mpa = P / 10.0
            T_c = T + 273.15
            state = iapws95.IAPWS95(T=T_c, P=P_mpa)
            enthalpie = state.h  # Enthalpie spécifique en kJ/kg
            entropie = state.s  # Entropie spécifique en kJ/kg·K
            energie_libre_gibbs = state.g  # Énergie libre de Gibbs spécifique en kJ/kg
            densité = state.rho  # Densité en kg/m³
            cp = state.cp  # Capacité calorifique spécifique à pression constante en kJ/kg·K
            cv = state.cv  # Capacité calorifique spécifique à volume constant en kJ/kg·K

            return enthalpie, entropie, energie_libre_gibbs, densité, cp, cv

        except ValueError as e:
            raise ValueError("Erreur lors du calcul des propriétés:", e)

    # Calculer les propriétés pour SAP
    Hadmi, entropieadmi, energie_libre_gibbsadmi, densitéadmi, cpadmi, cvadmi = calculer_proprietes_efficacite_gta(Tadmi, Padmi)
    Hst_1, entropiest_1, energie_libre_gibbsst_1, densitést_1, cpst_1, cvst_1 = calculer_proprietes_efficacite_gta(Tst_1,  Pst_1)
    Hécha, entropieécha, energie_libre_gibbsécha, densitéécha, cpécha, cvécha = calculer_proprietes_efficacite_gta(Técha,  Pécha)

    # Calculer le bilan énergétique
    Pth = (Qadmi * Hadmi - Qst_1 * Hst_1 - Qécha * Hécha) * 1000 / 3600
    efficacité = (PAlt / Pth) * 100
    return efficacité , Pth




