from flask import Flask, render_template, request, send_file
from io import BytesIO
from openpyxl import Workbook
from barillet import calculate_barillet_mass_balance, calculate_barillet_energy_balance
from iapws import iapws95
import logging
from flask import send_from_directory
import os



app = Flask(__name__)

# Define the function to calculate thermodynamic properties
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
# ... (your existing imports and Flask setup)

# Define a function to calculate properties data
def calculate_properties_data(inputs):
    properties_data = []
    for T, P in inputs:
        enthalpy, entropy, gibbs_free_energy, density, cp, cv = calculate_barillet_properties(T, P)
        properties_data.append({
            'Temperature': T,
            'Pressure': P,
            'Enthalpy': enthalpy,
            'Entropy': entropy,
            'Gibbs Free Energy': gibbs_free_energy,
            'Density': density,
            'Specific Heat Capacity': cp,
            'Specific Heat Capacity at Constant Volume': cv
        })
    return properties_data

@app.route('/', methods=['GET'])
def home_get():
    return render_template('home.html')

@app.route('/form', methods=['POST'])
def home_post():
    try:
        # Get user input from the form
        QSAP = float(request.form['QSAP'])
        Qsoutirage = float(request.form['Qsoutirage'])
        QPAP = float(request.form['QPAP'])
        QC = float(request.form['QC'])
        QD = float(request.form['QD'])
        QE = float(request.form['QE'])
        TSAP = float(request.form['TSAP'])
        PSAP = float(request.form['PSAP'])

        Tsoutirage = float(request.form['Tsoutirage'])
        Psoutirage = float(request.form['Psoutirage'])
        TPAP = float(request.form['TPAP'])
        PPAP = float(request.form['PPAP'])
        TC = float(request.form['TC'])
        PC = float(request.form['PC'])
        TD = float(request.form['TD'])
        PD = float(request.form['PD'])
        TE = float(request.form['TE'])
        PE = float(request.form['PE'])

        properties_data = []
        inputs = [(TSAP, PSAP), (TPAP, PPAP), (Tsoutirage, Psoutirage), (TC, PC), (TD, PD) ]
        for T, P in inputs:
            enthalpy, entropy, gibbs_free_energy, density, cp, cv = calculate_barillet_properties(T, P)
            properties_data.append({
                'Temperature': T,
                'Pressure': P,
                'Enthalpy': enthalpy,
                'Entropy': entropy,
                'Gibbs Free Energy': gibbs_free_energy,
                'Density': density,
                'Specific Heat Capacity': cp,
                'Specific Heat Capacity at Constant Volume': cv
            })

        Qentree, Qsortie, Rm, pertes = calculate_barillet_mass_balance(QSAP  ,Qsoutirage, QPAP, QC, QD, QE )
        Eentree, Esortie, Re, pertes_energy = calculate_barillet_energy_balance(QSAP,  Qsoutirage, QPAP, QD, QC, TSAP, PSAP ,
                                                                                Tsoutirage, Psoutirage, TPAP, PPAP, TC, PC,
                                                                                TD, PD )

        if Qentree != 0:
            Rm = (Qsortie / Qentree) * 100
        else:
            Rm = 0

        if Eentree != 0:
            Re = (Esortie / Eentree) * 100
        else:
            Re = 0

        if Eentree == 0:
            pertes_energy = 0
        return render_template(
            'result.html',
            properties_data=properties_data,
            Qentree=Qentree,
            Qsortie=Qsortie,
            Rm=Rm,
            pertes=pertes,
            Eentree=Eentree,
            Esortie=Esortie,
            Re=Re,
            pertes_energy=pertes_energy
        )
    except Exception as e:
        return str(e)

@app.route('/download_excel', methods=['GET', 'POST'])
def download_excel():
    try:
        if request.method == 'POST':
            # Get user input from the form for POST request and process it if needed
            # Add your code here to handle the POST request form data

            return "This route is for POST requests only."

        elif request.method == 'GET':
            # Retrieve the data required for generating the Excel file
            inputs = [
                (float(request.form['TSAP']), float(request.form['PSAP'])),
                (float(request.form['TPAP']), float(request.form['PPAP'])),
                (float(request.form['Tsoutirage']), float(request.form['Psoutirage'])),
                (float(request.form['TC']), float(request.form['PC'])),
                (float(request.form['TD']), float(request.form['PD']))
            ]
            properties_data = calculate_properties_data(inputs)

            # Create an Excel workbook and add the calculated values to a worksheet
            wb = Workbook()
            ws = wb.active

            # Write the headers
            headers = ['Temperature', 'Pressure', 'Enthalpy', 'Entropy', 'Gibbs Free Energy',
                       'Density', 'Specific Heat Capacity', 'Specific Heat Capacity at Constant Volume']
            ws.append(headers)

            # Write the calculated values
            for data in properties_data:
                row = [data['Temperature'], data['Pressure'], data['Enthalpy'], data['Entropy'],
                       data['Gibbs Free Energy'], data['Density'], data['Specific Heat Capacity'],
                       data['Specific Heat Capacity at Constant Volume']]
                ws.append(row)

            # Create a BytesIO object to save the Excel file in memory
            excel_data = BytesIO()
            wb.save(excel_data)
            excel_data.seek(0)

            # Send the Excel file as a response for download
            return send_file(
                excel_data,
                as_attachment=True,
                attachment_filename='result.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

    except Exception as e:
        return str(e)
        # Log the error using Flask's app.logger
        app.logger.error("Error occurred: %s", str(e))
        return "An error occurred while processing the request.", 500

if __name__ == "__main__":
    app.run(debug=True)









