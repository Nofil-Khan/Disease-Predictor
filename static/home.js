const form = document.getElementById("symptomForm");
const textarea = document.getElementById("symptoms");
const loadingDiv = document.getElementById("loadingDiv");
const resultBox = document.getElementById("resultBox");
const predictionContent = document.getElementById("predictionContent");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const text = textarea.value.trim();

    if (!text) {
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
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        loadingDiv.style.display = "none";
        resultBox.style.display = "block";

        let prediction = data.prediction || "";

        // Remove code fences if model returns them
        prediction = prediction.replace(/```[a-z]*\n?/gi, "").replace(/```/g, "");

        // Render markdown
        predictionContent.innerHTML = marked.parse(prediction);

    } catch (error) {

        loadingDiv.style.display = "none";
        resultBox.style.display = "block";

        predictionContent.innerHTML =
            "<p style='color:red;'>Error occurred while predicting.</p>";

    }

});