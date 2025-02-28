from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_cancer_categories', methods=['GET'])
def get_cancer_categories():
    response = jsonify({
        'cancer_categories': util.get_cancer_categories()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_diagnosis_methods', methods=['GET'])
def get_diagnosis_methods():
    response = jsonify({
        'diagnosis_methods': util.get_diagnosis_methods()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_treatment_categories', methods=['GET'])
def get_treatment_categories():
    response = jsonify({
        'treatment_categories': util.get_treatment_categories()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_stage_label', methods=['GET'])
def get_stage_label():
    try:
        stage_numeric = int(request.args.get('stage'))
        stage_label = util.get_stage_label(stage_numeric)
        response = jsonify({'stage_label': stage_label})
    except Exception as e:
        response = jsonify({'error': str(e)})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_treatment', methods=['GET', 'POST'])
def predict_treatment():
    # For GET requests, use query parameters; for POST, use form data
    data = request.form if request.method == 'POST' else request.args

    try:
        age = float(data['age_at_diagnosis'])
        stage = int(data['ajcc_pathologic_stage'])
        cancer_category = data['cancer_category']  # e.g. "Invasive Ductal Carcinoma (IDC)"
        diagnosis_method = data['diagnosis_method']  # e.g. "Needle Biopsy"
        treatment_category = data['treatment_category']  # e.g. "Chemotherapy"
    except Exception as e:
        return jsonify({'error': str(e)})

    # Use the utility function to predict treatment/therapy
    prediction = util.predict_treatment_or_therapy(age, stage, cancer_category, diagnosis_method, treatment_category)

    # Map the prediction to the desired response
    if prediction == 1:
        output = "Needs Treatment/Therapy"
    elif prediction == 0:
        output = "No Treatment Required"
    else:
        output = "Prediction Error"

    response = jsonify({'prediction': output})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Flask server for treatment prediction...")
    util.load_saved_artifacts()
    app.run()
