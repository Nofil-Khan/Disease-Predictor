// -----------------------------
// DOM Elements
// -----------------------------
const form = document.getElementById("symptomForm");
const textarea = document.getElementById("symptoms");

const loadingDiv = document.getElementById("loadingDiv");
const resultBox = document.getElementById("resultBox");
const predictionContent = document.getElementById("predictionContent");
const idleState = document.getElementById("idleState");

const menuBtn = document.getElementById("menu-btn");
const closeBtn = document.getElementById("close-btn");
const sidebar = document.getElementById("sidebar");


// -----------------------------
// Sidebar toggle
// -----------------------------
menuBtn.onclick = () => sidebar.classList.add("active");
closeBtn.onclick = () => sidebar.classList.remove("active");


// -----------------------------
// UI State Controller
// -----------------------------
function setUIState(state) {
    idleState.style.display = "none";
    loadingDiv.style.display = "none";
    resultBox.style.display = "none";

    if (state === "idle") idleState.style.display = "block";
    if (state === "loading") loadingDiv.style.display = "block";
    if (state === "result") resultBox.style.display = "block";
}


// -----------------------------
// Form Submit Handler
// -----------------------------
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = textarea.value.trim();

    if (!text) {
        alert("Enter symptoms first.");
        return;
    }

    setUIState("loading");

    try {
        // 🔥 use full URL to avoid path issues
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ symptoms: text })
        });

        console.log("STATUS:", response.status);

        const data = await response.json();
        console.log("DATA:", data);

        // -----------------------------
        // Backend error
        // -----------------------------
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
        }

        if (data.error) {
            throw new Error(data.error);
        }

        const pred = data.prediction;

        if (!pred) {
            throw new Error("Prediction missing in response");
        }

        // -----------------------------
        // Render result
        // -----------------------------
        predictionContent.innerHTML = `
            <p><strong>Disease:</strong> ${pred.disease}</p>
            <p><strong>Confidence:</strong> ${pred.confidence ?? "N/A"}%</p>

            <p><strong>Recognized Symptoms:</strong></p>
            <ul>
                ${(pred.recognized_symptoms || [])
                    .map(s => `<li>${s}</li>`)
                    .join("")}
            </ul>

            <p><strong>Top Predictions:</strong></p>
            <ul>
                ${Object.entries(pred.top_predictions || {})
                    .map(([d, p]) => `<li>${d}: ${p}%</li>`)
                    .join("")}
            </ul>

            ${
                pred.unknown_symptoms && pred.unknown_symptoms.length
                ? `
                <p><strong>Unrecognized Symptoms:</strong></p>
                <ul>
                    ${pred.unknown_symptoms.map(s => `<li>${s}</li>`).join("")}
                </ul>
                `
                : ""
            }
        `;

        setUIState("result");

    } catch (error) {
        console.error("🔥 FULL ERROR:", error);

        predictionContent.innerHTML = `
            <p style="color:#ef4444;">
                ${error.message || "System Error: Unable to complete analysis."}
            </p>
        `;

        setUIState("result");
    }
});


// -----------------------------
// Initial state
// -----------------------------
setUIState("idle");