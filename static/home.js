const form = document.getElementById("symptomForm");
const textarea = document.getElementById("symptoms");
const loadingDiv = document.getElementById("loadingDiv");
const resultBox = document.getElementById("resultBox");
const predictionContent = document.getElementById("predictionContent");
const idleState = document.getElementById("idleState");

const menuBtn = document.getElementById("menu-btn");
const closeBtn = document.getElementById("close-btn");
const sidebar = document.getElementById("sidebar");

menuBtn.addEventListener("click", () => {
    sidebar.classList.add("active");
});

closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("active");
});

function setUIState(state) {
    idleState.style.display = "none";
    loadingDiv.style.display = "none";
    resultBox.style.display = "none";

    if (state === "idle") idleState.style.display = "block";
    if (state === "loading") loadingDiv.style.display = "block";
    if (state === "result") resultBox.style.display = "block";
}

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const text = textarea.value.trim();

    if (!text) {
        alert("Error: Input array empty.");
        return;
    }

    setUIState("loading");

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) {
            throw new Error("Server communication failure.");
        }

        const data = await response.json();
        
        let prediction = data.prediction || "";
        prediction = prediction.replace(/```[a-z]*\n?/gi, "").replace(/```/g, "");

        predictionContent.innerHTML = marked.parse(prediction);
        setUIState("result");

    } catch (error) {
        predictionContent.innerHTML = "<p style='color:#ef4444;'>System Error: Unable to complete analysis.</p>";
        setUIState("result");
    }
});