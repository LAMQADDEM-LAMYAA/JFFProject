from flask import Flask, render_template, request
from iapws import iapws95

gta_efficiency_app = Flask(__name__)

# Inside the calculate_gta_efficiency function
def calculate_gta_efficiency(PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha):
    try:
        properties_gta_efficiency_data = [
            calculate_gta_efficiency_properties(Tadmi, Padmi),
            calculate_gta_efficiency_properties(Tst_1, Pst_1),
            calculate_gta_efficiency_properties(Técha, Pécha)
        ]

        # Check if any of the properties_gta_efficiency_data is None
        if None in properties_gta_efficiency_data:
            raise ValueError("Error: One or more properties are not available.")



        # Extracting enthalpy values from the dictionaries
        enthalpy_admi = properties_gta_efficiency_data[0]['Enthalpy']
        enthalpy_st_1 = properties_gta_efficiency_data[1]['Enthalpy']
        enthalpy_écha = properties_gta_efficiency_data[2]['Enthalpy']


        # Calculate total power
        Pth_admi = Qadmi * enthalpy_admi * 1000 / 3600
        Pth_st_1 = Qst_1 * enthalpy_st_1 * 1000 / 3600
        Pth_écha = Qécha * enthalpy_écha * 1000 / 3600

        # Calculate total power
        Pth_total = (Pth_admi - Pth_st_1 - Pth_écha)*0.001

        # Calculate efficiency
        efficiency = (PAlt / Pth_total) * 100

        return Pth_total, efficiency


    except Exception as e:
        raise ValueError("Error in calculating GTA efficiency: {}".format(e))


# Define the function to calculate thermodynamic properties
def calculate_gta_efficiency_properties(T, P):
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

        return {
            'Temperature': T,
            'Pressure': P,
            'Enthalpy': enthalpy,
            'Entropy': entropy,
            'Gibbs Free Energy': gibbs_free_energy,
            'Density': density,
            'Specific Heat Capacity': cp,
            'Specific Heat Capacity at Constant Volume': cv
        }

    except ValueError as e:
        raise ValueError("Error in calculating properties for T={}, P={}: {}".format(T, P, e))
    except AttributeError as e:
        raise AttributeError("Missing attribute in thermodynamic state for T={}, P={}: {}".format(T, P, e))



@gta_efficiency_app.route('/gta_efficiency_home', methods=['GET'])
def gta_efficiency_home():
    return render_template('gta_efficiency_home.html')

# ... (previous code)
@gta_efficiency_app.route('/gta_efficiency_result', methods=['POST'])
def calculate_gta_efficiency_page():
    try:
        PAlt = float(request.form['PAlt'])
        Qadmi = float(request.form['Qadmi'])
        Qst_1 = float(request.form['Qst_1'])
        Qécha = float(request.form['Qécha'])
        Tadmi = float(request.form['Tadmi'])
        Tst_1 = float(request.form['Tst_1'])
        Técha = float(request.form['Técha'])
        Padmi = float(request.form['Padmi'])
        Pst_1 = float(request.form['Pst_1'])
        Pécha = float(request.form['Pécha'])

        # Calculate GTA Efficiency using the provided inputs
        Pth, efficiency = calculate_gta_efficiency(
            PAlt, Qadmi, Qst_1, Qécha, Tadmi, Tst_1, Técha, Padmi, Pst_1, Pécha
        )
        properties_gta_efficiency_data = [
            calculate_gta_efficiency_properties(Tadmi, Padmi),
            calculate_gta_efficiency_properties(Tst_1, Pst_1),
            calculate_gta_efficiency_properties(Técha, Pécha)
        ]

        return render_template(
            'gta_efficiency_result.html',
            PAlt=PAlt,
            Pth=Pth,
            efficiency=efficiency,
            properties_gta_efficiency_data=properties_gta_efficiency_data
        )

    except Exception as e:
        return str(e)
# ... (previous code)

@gta_efficiency_app.route('/form', methods=['POST'])
def handle_form_data():
    try:
        # Retrieve form data
        PAlt = float(request.form['PAlt'])
        Qadmi = float(request.form['Qadmi'])
        Qst_1 = float(request.form['Qst_1'])
        Qécha = float(request.form['Qécha'])
        Tadmi = float(request.form['Tadmi'])
        Tst_1 = float(request.form['Tst_1'])
        Técha = float(request.form['Técha'])
        Padmi = float(request.form['Padmi'])
        Pst_1 = float(request.form['Pst_1'])
        Pécha = float(request.form['Pécha'])

        return render_template('gta_efficiency_result.html',
                               PAlt=PAlt,
                               Qadmi=Qadmi,
                               Qst_1=Qst_1,
                               Qécha=Qécha,
                               Tadmi=Tadmi,
                               Tst_1=Tst_1,
                               Técha=Técha,
                               Padmi=Padmi,
                               Pst_1=Pst_1,
                               Pécha=Pécha)

    except Exception as e:
        return str(e)


@gta_efficiency_app.route('/')
def home():
    return render_template('gta_efficiency_home.html')

if __name__ == "__main__":
    gta_efficiency_app.run(debug=True)