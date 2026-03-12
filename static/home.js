const form = document.getElementById("symptomForm");
const textarea = document.getElementById("message");
const loadingDiv = document.getElementById("loadingDiv");
const resultBox = document.getElementById("resultBox");


form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const text = textarea.value;

    if (!text.trim()) {
        alert("Please enter symptoms");
        return;
    }

    loadingDiv.style.display = "block";
    resultBox.style.display = "none";

    try {

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text
            })
        });

        const data = await response.json();

        loadingDiv.style.display = "none";

        resultBox.style.display = "block";

        resultBox.innerHTML = `
            <h3>Diagnostic Prediction</h3>
            <p><strong>Predicted Condition:</strong> ${data.prediction}</p>
        `;

    } catch (error) {

        loadingDiv.style.display = "none";

        resultBox.style.display = "block";

        resultBox.innerHTML = "Error occurred while predicting.";

    }

});