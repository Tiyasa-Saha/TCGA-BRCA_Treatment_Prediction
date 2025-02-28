import json
import joblib
import numpy as np

__data_columns = None
__model = None
__cancer_categories = None
__diagnosis_methods = None
__treatment_categories = None


# Dictionary to map numeric AJCC pathologic stage values to categorical labels
__ajcc_stage_map = {
    0: "Stage I",
    1: "Stage IA",
    2: "Stage IB",
    3: "Stage II",
    4: "Stage IIA",
    5: "Stage IIB",
    6: "Stage III",
    7: "Stage IIIA",
    8: "Stage IIIB",
    9: "Stage IIIC",
    10: "Stage IV",
    11: "Stage X"
}

def load_saved_artifacts():
    """
    Loads the saved model and column artifacts.
    """
    global __data_columns, __model, __cancer_categories, __diagnosis_methods, __treatment_categories
    print("Loading saved artifacts...")

    with open("artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

    __model = joblib.load("artifacts/best_gb_model.joblib")

    # Extract categories dynamically
    __cancer_categories = [col.replace("cancer_category_", "") for col in __data_columns if
                           col.startswith("cancer_category_")]
    __diagnosis_methods = [col.replace("diagnosis_method_category_", "") for col in __data_columns if
                           col.startswith("diagnosis_method_category_")]
    __treatment_categories = [col.replace("treatment_category_", "") for col in __data_columns if
                              col.startswith("treatment_category_")]

    print("Artifacts loaded successfully.")


def predict_treatment_or_therapy(age, stage, cancer_category, diagnosis_method, treatment_category):
    """
    Predicts whether treatment or therapy is needed.
    """
    x = np.zeros(len(__data_columns))

    try:
        age_index = __data_columns.index('age_at_diagnosis')
        stage_index = __data_columns.index('ajcc_pathologic_stage')
    except ValueError as e:
        print("Error: Required numeric feature not found in the data columns.")
        return None

    x[age_index] = age
    x[stage_index] = stage

    cancer_col = f"cancer_category_{cancer_category.lower()}"
    diag_col = f"diagnosis_method_category_{diagnosis_method.lower()}"
    treat_col = f"treatment_category_{treatment_category.lower()}"

    if cancer_col in __data_columns:
        x[__data_columns.index(cancer_col)] = 1
    else:
        print(f"Warning: Column '{cancer_col}' not found.")

    if diag_col in __data_columns:
        x[__data_columns.index(diag_col)] = 1
    else:
        print(f"Warning: Column '{diag_col}' not found.")

    if treat_col in __data_columns:
        x[__data_columns.index(treat_col)] = 1
    else:
        print(f"Warning: Column '{treat_col}' not found.")

    prediction = __model.predict([x])[0]
    return prediction


def get_cancer_categories():
    return __cancer_categories


def get_diagnosis_methods():
    return __diagnosis_methods


def get_treatment_categories():
    return __treatment_categories


def get_stage_label(stage_numeric):
    """
    Converts a numeric AJCC pathologic stage to its corresponding categorical label.
    """
    return __ajcc_stage_map.get(stage_numeric, "Unknown Stage")


def get_data_columns():
    return __data_columns


if __name__ == '__main__':
    load_saved_artifacts()
    print("Available Cancer Categories:", get_cancer_categories())
    print("Available Diagnosis Methods:", get_diagnosis_methods())
    print("Available Treatment Categories:", get_treatment_categories())

    # Test getting stage label
    for i in range(12):
        print(f"Numeric Stage {i}: {get_stage_label(i)}")

    # Test prediction
    pred = predict_treatment_or_therapy(
        age=55,
        stage=2,
        cancer_category="Invasive Ductal Carcinoma (IDC)",
        diagnosis_method="Needle Biopsy",
        treatment_category="Chemotherapy"
    )
    print("Test prediction:", pred)
