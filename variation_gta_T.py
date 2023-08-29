import numpy as np
import matplotlib.pyplot as plt
from iapws import iapws95

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
        Hadmi = calculer_proprietes_efficacite_gta(Tadmi, Padmi)
        Hst_1 = calculer_proprietes_efficacite_gta(Tst_1, Pst_1)
        Hécha = calculer_proprietes_efficacite_gta(Técha, Pécha)

        # Calculate total power
        Pth = (Qadmi * Hadmi  - Qst_1 * Hst_1 - Qécha * Hécha )* (1000 *0.001) / 3600

        # Calculate efficiency
        efficacite = (PAlt / Pth) * 100

        return Pth, efficacite
# Paramètres constants
PAlt = 25
Qadmi = 126
Qst_1 = 48
Qécha = 62
Tst_1 = 220
Técha = 34
Pst_1 = 4.3
Pécha = 0.04
Padmi = 49
Tadmi = 460
efficacite, Pth = calculer_efficacite_gta(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha)

print("Efficacité : {:.4f}%".format(efficacite))
print("Bilan énergétique : {:.2f} kW".format(Pth))

# Générer des valeurs de température et de pression pour lesquelles vous souhaitez tracer les courbes
Tadmi_values = np.linspace(420, 492, 100)  # Range de Tadmi

efficacite_values_Tadmi = []
for Tadmi in Tadmi_values:
    efficacite, _ = calculer_efficacite_gta(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, 58, Pst_1, Pécha)
    efficacite_values_Tadmi.append(efficacite)


# Tracer la courbe de variation de l'efficacité en fonction de la température d'admission
plt.figure()
plt.plot(Tadmi_values, efficacite_values_Tadmi, label='Efficacité vs Tadmi')
plt.xlabel('Température d\'admission (°C)')
plt.ylabel('Efficacité (%)')
plt.legend()
plt.title('Variation de l\'efficacité en fonction de la température d\'admission')
plt.grid(True)
plt.show()

best_efficiency = 0  # Initialisez la meilleure efficacité à 0
best_Tadmi = 0       # Initialisez la meilleure température d'admission
best_Padmi = 0       # Initialisez la meilleure pression d'admission

for Tadmi in Tadmi_values:

        if efficacite > best_efficiency:
            best_efficiency = efficacite
            best_Tadmi = Tadmi
            best_Padmi = Padmi

print("Meilleure efficacité : {:.4f}%".format(best_efficiency))
print("Meilleure température d'admission : {:.2f} °C".format(best_Tadmi))
print("Meilleure pression d'admission : {:.2f} Bar".format(best_Padmi))
