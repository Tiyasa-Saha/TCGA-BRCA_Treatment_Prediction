// Function to get selected stage value from radio buttons
function getStageValue() {
    var uiStage = document.getElementsByName("uiStage");
    for (var i in uiStage) {
        if (uiStage[i].checked) {
            return parseInt(uiStage[i].value);
        }
    }
    return -1; // Invalid Value
}

// Function to make API call for treatment prediction
function onClickedPredictTreatment() {
    console.log("Predict button clicked");

    var age = document.getElementById("uiAge").value;
    var stage = getStageValue();
    var cancerCategory = document.getElementById("uiCancerCategory").value;
    var diagnosisMethod = document.getElementById("uiDiagnosisMethod").value;
    var treatmentCategory = document.getElementById("uiTreatmentCategory").value;

    var resultDiv = document.getElementById("uiResult");

    // Ensure all fields are selected before making the request
    if (age === "" || stage === -1 || cancerCategory === "" || diagnosisMethod === "" || treatmentCategory === "") {
        resultDiv.innerHTML = "<h2 style='color:red;'>Please fill in all fields.</h2>";
        return;
    }

    var url = "http://127.0.0.1:5000/predict_treatment";

    $.post(url, {
        age_at_diagnosis: parseFloat(age),
        ajcc_pathologic_stage: stage,
        cancer_category: cancerCategory,
        diagnosis_method: diagnosisMethod,
        treatment_category: treatmentCategory
    }, function(data, status) {
        console.log("Prediction:", data.prediction);
        resultDiv.innerHTML = "<h2>" + data.prediction + "</h2>";
    }).fail(function(error) {
        resultDiv.innerHTML = "<h2 style='color:red;'>Error in prediction. Try again.</h2>";
    });
}

// Function to load dropdown values from API
function loadDropdowns() {
    console.log("Loading dropdown options...");

    var cancerCategoryDropdown = document.getElementById("uiCancerCategory");
    var diagnosisMethodDropdown = document.getElementById("uiDiagnosisMethod");
    var treatmentCategoryDropdown = document.getElementById("uiTreatmentCategory");

    // Fetch Cancer Categories
    $.get("http://127.0.0.1:5000/get_cancer_categories", function(data) {
        $('#uiCancerCategory').empty().append('<option disabled selected>Choose a Cancer Category</option>');
        data.cancer_categories.forEach(function(category) {
            $('#uiCancerCategory').append(new Option(category, category));
        });
    });

    // Fetch Diagnosis Methods
    $.get("http://127.0.0.1:5000/get_diagnosis_methods", function(data) {
        $('#uiDiagnosisMethod').empty().append('<option disabled selected>Choose a Diagnosis Method</option>');
        data.diagnosis_methods.forEach(function(method) {
            $('#uiDiagnosisMethod').append(new Option(method, method));
        });
    });

    // Fetch Treatment Categories
    $.get("http://127.0.0.1:5000/get_treatment_categories", function(data) {
        $('#uiTreatmentCategory').empty().append('<option disabled selected>Choose a Treatment Category</option>');
        data.treatment_categories.forEach(function(treatment) {
            $('#uiTreatmentCategory').append(new Option(treatment, treatment));
        });
    });
}

// Load dropdown options when the page loads
window.onload = loadDropdowns;
