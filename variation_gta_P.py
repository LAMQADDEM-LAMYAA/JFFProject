from iapws import iapws95
import matplotlib.pyplot as plt
from iapws import iapws95
import numpy as np


def calculer_efficacite_gta(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha):
    def calculer_proprietes_efficacite_gta(T, P):
        try:
            P_mpa = P / 10.0
            T_c = T + 273.15
            state = iapws95.IAPWS95(T=T_c, P=P_mpa)
            enthalpie = state.h  # Enthalpie spécifique en kJ/kg

            return enthalpie

        except ValueError as e:
            raise ValueError("Erreur lors du calcul des propriétés:", e)

    # Calculer les propriétés pour SAP
    Hadmi= calculer_proprietes_efficacite_gta(Tadmi, Padmi)
    Hst_1 = calculer_proprietes_efficacite_gta(Tst_1,  Pst_1)
    Hécha = calculer_proprietes_efficacite_gta(Técha,  Pécha)

    # Calculer le bilan énergétique
    Pth = ((Qadmi * Hadmi - Qst_1 * Hst_1 - Qécha * Hécha) * 1000 / 3600)*0.001
    efficacité = (PAlt / Pth) * 100
    return efficacité , Pth

# Paramètres constants
PAlt = 25
Qadmi = 126
Qst_1 = 48
Qécha = 62
Tst_1 = 220
Técha = 34
Pst_1 = 4.3
Pécha = 0.06
Padmi = 56
Tadmi = 460
efficacité, Pth = calculer_efficacite_gta(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha)

print("Efficacité : {:.4f}%".format(efficacité))
print("Bilan énergétique : {:.2f} kW".format(Pth))

#Générer des valeurs de température et de pression pour lesquelles vous souhaitez tracer les courbes
Padmi_values = np.linspace(47, 61, 100)  # Range de Tadmi


efficacite_values_Padmi = []


for Padmi in Padmi_values:
    efficacite, _ = calculer_efficacite_gta(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha)
    efficacite_values_Padmi.append(efficacite)

# Tracer la courbe de variation de l'efficacité en fonction de la température d'admission
plt.figure()
plt.plot(Padmi_values, efficacite_values_Padmi, label='Efficacité vs Padmi')
plt.xlabel('pression\'admission (°C)')
plt.ylabel('Efficacité (%)')
plt.legend()
plt.title('Variation de l\'efficacité en fonction de la pression d\'admission')
plt.grid(True)
plt.show()










