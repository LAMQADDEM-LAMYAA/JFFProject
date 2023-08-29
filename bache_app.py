from flask import Flask, render_template, request
from bache import calculate_bache_mass_balance, calculate_bache_energy_balance, calculate_bache_properties

bache_app = Flask(__name__)


def calculate_bache_mass_balance(QBPB, Qpolissage, QSAP, Qdésurchauffe):
    Qentree_bache = QBPB + Qpolissage
    Qsortie_bache = QSAP + Qdésurchauffe
    Rm_bache = (Qsortie_bache / Qentree_bache) * 100
    pertes_bache = Qentree_bache - Qsortie_bache
    return Qentree_bache, Qsortie_bache, Rm_bache, pertes_bache
def calculate_bache_energy_balance(QBPB, Qpolissage, QSAP, Qdésurchauffe, TBPB, PBPB,  TSAP, PSAP, Tdésurchauffe, Pdésurchauffe, Tpolissage, Ppolissage):
    HBPB, entropyBPB, gibbs_free_energyBPB, densityBPB, cpBPB, cvBPB = calculate_bache_properties(TBPB, PBPB)
    HSAP, entropySAP, gibbs_free_energySAP, densitySAP, cpSAP, cvSAP = calculate_bache_properties(TSAP, PSAP)
    Hdésurchauffe, entropydésurchauffe, gibbs_free_energydésurchauffe, densitydésurchauffe, cpdésurchauffe, cvdésurchauffe = calculate_bache_properties(Tdésurchauffe, Pdésurchauffe)
    Hpolissage, entropypolissage, gibbs_free_energypolissage, densitypolissage, cppolissage, cvpolissage = calculate_bache_properties(Tpolissage, Ppolissage)
    Eentree_bache = (QBPB * HBPB * 1000)  + (Qpolissage * Hpolissage * 1000)
    Esortie_bache = (QSAP * HSAP * 1000) + (Qdésurchauffe * Hdésurchauffe * 1000)
    Re_bache = (Esortie_bache / Eentree_bache) * 100
    pertes_bache_energy = (Eentree_bache - Esortie_bache) / 3600
    return Eentree_bache, Esortie_bache, Re_bache, pertes_bache_energy


def calculate_properties_data(inputs):
    properties_data = []
    for T, P in inputs:
        enthalpy, entropy, gibbs_free_energy, density, cp, cv = calculate_bache_properties(T, P)
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

@bache_app.route('/bache_home', methods=['GET', 'POST'])
def bache_home():
    if request.method == 'POST':
        try:
            QBPB = float(request.form['QBPB'])
            Qpolissage = float(request.form['Qpolissage'])
            QSAP = float(request.form['QSAP'])
            Qdésurchauffe = float(request.form['Qdésurchauffe'])

            Qentree_bache, Qsortie_bache, Rm_bache, pertes_bache = calculate_bache_mass_balance(QBPB, Qpolissage, QSAP, Qdésurchauffe)

            print("Qentree_bache:", Qentree_bache)
            print("Qsortie_bache:", Qsortie_bache)
            print("Rm_bache:", Rm_bache)
            print("pertes_bache:", pertes_bache)

            TBPB = float(request.form['TBPB'])
            PBPB = float(request.form['PBPB'])
            TSAP = float(request.form['TSAP'])
            PSAP = float(request.form['PSAP'])
            Tdésurchauffe = float(request.form['Tdésurchauffe'])
            Pdésurchauffe = float(request.form['Pdésurchauffe'])
            Tpolissage = float(request.form['Tpolissage'])
            Ppolissage = float(request.form['Ppolissage'])

            inputs = [
                (TBPB, PBPB),
                (Tpolissage, Ppolissage),
                (TSAP, PSAP),
                (Tdésurchauffe, Pdésurchauffe),

            ]

            properties_bache_data = calculate_properties_data(inputs)

            Eentree_bache, Esortie_bache, Re_bache, pertes_bache_energy = calculate_bache_energy_balance(QBPB,  Qpolissage, QSAP, Qdésurchauffe, TBPB, PBPB,  TSAP, PSAP, Tdésurchauffe, Pdésurchauffe, Tpolissage, Ppolissage)
            # Print for debugging
            print("Eentree_bache:", Eentree_bache)
            print("Esortie_bache:", Esortie_bache)
            print("Re_bache:", Re_bache)
            print("pertes_bache_energy:", pertes_bache_energy)
            return render_template('bache_result.html',
                                   Qentree_bache=Qentree_bache,
                                   Qsortie_bache=Qsortie_bache,
                                   Rm_bache=Rm_bache,
                                   pertes_bache=pertes_bache,
                                   Eentree_bache=Eentree_bache,
                                   Esortie_bache=Esortie_bache,
                                   Re_bache=Re_bache,
                                   pertes_bache_energy=pertes_bache_energy,
                                   properties_bache_data=properties_bache_data
                                   )

        except Exception as e:
            print("Error in bache_home:", str(e))  # Print the error message to the console
            return str(e)

    return render_template('bache_home.html')

@bache_app.route('/form', methods=['POST'])
def handle_form_data():
    try:
        QBPB = float(request.form['QBPB'])
        TBPB = float(request.form['TBPB'])
        PBPB = float(request.form['PBPB'])
        Qpolissage = float(request.form['Qpolissage'])
        Tpolissage = float(request.form['Tpolissage'])
        Ppolissage = float(request.form['Ppolissage'])
        QSAP = float(request.form['QSAP'])
        TSAP = float(request.form['TSAP'])
        PSAP = float(request.form['PSAP'])
        Qdésurchauffe = float(request.form['Qdésurchauffe'])
        Tdésurchauffe = float(request.form['Tdésurchauffe'])
        Pdésurchauffe = float(request.form['Pdésurchauffe'])


        inputs = [
            (TBPB, PBPB),
            (Tpolissage, Ppolissage),
            (TSAP, PSAP),
            (Tdésurchauffe, Pdésurchauffe),

        ]

        properties_bache_data = calculate_properties_data(inputs)

        bache_results = calculate_bache_energy_balance(QBPB,  Qpolissage, QSAP, Qdésurchauffe, TBPB, PBPB,  TSAP, PSAP, Tdésurchauffe, Pdésurchauffe, Tpolissage, Ppolissage)

        Qentree_bache = QBPB  + Qpolissage
        Qsortie_bache_value = QSAP + Qdésurchauffe
        Rm_bache = (Qsortie_bache_value / Qentree_bache) * 100
        pertes_bache = Qentree_bache - Qsortie_bache_value
        Eentree_bache = bache_results['Eentree_bache']
        Esortie_bache = bache_results['Esortie_bache']
        Re_bache = bache_results['Re_bache']
        pertes_bache_energy =  bache_results['pertes_bache_energy']

        return render_template('bache_result.html',
                               Qentree_bache=Qentree_bache,
                               Qsortie_bache=Qsortie_bache_value,
                               Rm_bache=Rm_bache,
                               pertes_bache=pertes_bache,
                               Eentree_bache=Eentree_bache,
                               Esortie_bache=Esortie_bache,
                               Re_bache=Re_bache,
                               pertes_energy=(Eentree_bache - Esortie_bache) / 3600,
                               properties_bache_data=properties_bache_data
                               )

    except Exception as e:
        print("Error in handle_form_data:", str(e))  # Print the error message to the console
        return str(e)


@bache_app.route('/')
def home():
    return render_template('bache_home.html')

if __name__ == "__main__":

    bache_app.run(debug=True)


