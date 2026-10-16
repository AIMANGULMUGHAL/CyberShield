
from flask import Flask, render_template_string, request, jsonify
from inference_engine import analyze_threat
from knowledge_base import RULES

app = Flask(__name__)


# ============================================================
# CYBERSHIELD WEB INTERFACE
# Everything is inside app.py
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>CYBERSHIELD — Expert Security System</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    min-height: 100vh;
    background: #02050A;
    color: #F4F7FA;
    font-family: Arial, sans-serif;
    overflow-x: hidden;
}

/* ============================================================
   MATRIX BACKGROUND
============================================================ */

#matrix {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
    background: #02050A;
}

.matrix-overlay {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(
            circle at center,
            rgba(0, 183, 255, 0.05),
            transparent 55%
        );
    z-index: -1;
    pointer-events: none;
}

/* ============================================================
   HEADER
============================================================ */

.header {
    height: 82px;
    background: rgba(3, 7, 13, 0.94);
    border-bottom: 1px solid #172333;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 35px;

    position: relative;
    z-index: 5;
}

.brand-area {
    display: flex;
    align-items: center;
    gap: 12px;
}

.shield {
    font-size: 34px;
    color: #FF1744;
    filter: drop-shadow(0 0 10px rgba(255,23,68,0.5));
}

.brand {
    font-family: Consolas, monospace;
    font-size: 26px;
    font-weight: 900;
    letter-spacing: 1px;
}

.brand-subtitle {
    color: #FF4D6D;
    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;

    color: #00FF9D;

    font-family: Consolas, monospace;
    font-size: 12px;
    font-weight: bold;
}

.status-dot {
    width: 9px;
    height: 9px;
    background: #00FF9D;
    border-radius: 50%;

    box-shadow: 0 0 12px #00FF9D;

    animation: pulse 1.5s infinite;
}

@keyframes pulse {

    0%,100% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: .4;
        transform: scale(.75);
    }
}

/* ============================================================
   DASHBOARD
============================================================ */

.dashboard {
    width: min(1450px, 96%);
    margin: 25px auto;

    display: grid;
    grid-template-columns: 1fr 1fr;

    gap: 24px;
}

/* ============================================================
   PANELS
============================================================ */

.panel {
    background: rgba(7, 12, 19, 0.93);

    border: 1px solid #172333;
    border-radius: 18px;

    padding: 22px;

    box-shadow:
        0 15px 50px rgba(0,0,0,.35),
        inset 0 0 30px rgba(0,183,255,.015);

    backdrop-filter: blur(8px);
}

/* ============================================================
   VISUAL
============================================================ */

.visual {
    height: 160px;

    background:
        radial-gradient(
            circle,
            rgba(255,23,68,.09),
            transparent 60%
        ),
        #03070C;

    border: 1px solid #24111A;
    border-radius: 14px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    margin-bottom: 22px;
}

.warning {
    font-size: 65px;
    color: #FF1744;

    text-shadow:
        0 0 15px rgba(255,23,68,.55),
        0 0 35px rgba(255,23,68,.2);

    animation: warningPulse 2s infinite;
}

@keyframes warningPulse {

    0%,100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.08);
    }
}

.warning-text {
    margin-top: 5px;

    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;

    color: #FF4D6D;
}

/* ============================================================
   TITLES
============================================================ */

.section-title {
    font-family: Consolas, monospace;
    font-size: 20px;
    font-weight: bold;

    margin-bottom: 5px;
}

.section-subtitle {
    color: #718096;
    font-size: 12px;

    margin-bottom: 18px;
}

/* ============================================================
   QUESTION CARDS
============================================================ */

.question {
    display: flex;
    align-items: center;
    justify-content: space-between;

    background: #0A111B;

    border: 1px solid #14202D;
    border-radius: 11px;

    padding: 13px 15px;

    margin-bottom: 9px;

    transition: .25s;
}

.question:hover {
    border-color: #FF1744;

    transform: translateX(3px);

    box-shadow:
        0 0 15px rgba(255,23,68,.08);
}

.question-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.number {
    color: #FF1744;

    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;
}

.question-text {
    color: #D8E0EA;

    font-size: 13px;
    font-weight: bold;
}

select {
    width: 105px;

    padding: 8px 10px;

    background: #111A25;
    color: white;

    border: 1px solid #263545;
    border-radius: 8px;

    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;

    outline: none;

    cursor: pointer;
}

select:focus {
    border-color: #FF1744;
}

/* ============================================================
   FIREWALL
============================================================ */

.firewall-box {
    margin-top: 14px;

    padding: 15px;

    background: rgba(0,183,255,.035);

    border: 1px solid #14202D;
    border-radius: 11px;
}

.firewall-title {
    font-family: Consolas, monospace;
    color: #00B7FF;

    font-size: 11px;
    font-weight: bold;

    margin-bottom: 8px;
}

/* ============================================================
   BUTTON
============================================================ */

.analyze-button {
    width: 100%;

    margin-top: 15px;

    padding: 15px;

    border: none;
    border-radius: 10px;

    background: #FF1744;
    color: white;

    font-family: Consolas, monospace;
    font-size: 13px;
    font-weight: bold;

    cursor: pointer;

    transition: .25s;

    box-shadow:
        0 8px 25px rgba(255,23,68,.18);
}

.analyze-button:hover {
    background: #8B1026;

    transform: translateY(-2px);

    box-shadow:
        0 12px 30px rgba(255,23,68,.25);
}

.analyze-button:active {
    transform: scale(.98);
}

/* ============================================================
   RIGHT HEADER
============================================================ */

.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 18px;
}

.result-title {
    font-family: Consolas, monospace;
    font-size: 20px;
    font-weight: bold;
}

.scan-status {
    color: #00B7FF;

    font-family: Consolas, monospace;
    font-size: 10px;
    font-weight: bold;
}

/* ============================================================
   THREAT CARD
============================================================ */

.threat-card {
    min-height: 190px;

    background:
        radial-gradient(
            circle,
            rgba(255,23,68,.06),
            transparent 65%
        ),
        #080D14;

    border: 1px solid #24111A;
    border-radius: 15px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    text-align: center;

    padding: 20px;
}

.threat-icon {
    font-size: 44px;

    color: #FF1744;

    margin-bottom: 8px;
}

.result-label {
    color: #00B7FF;

    font-family: Consolas, monospace;
    font-size: 24px;
    font-weight: bold;

    max-width: 90%;
}

.risk-label {
    color: #718096;

    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: bold;

    margin-top: 9px;
}

/* ============================================================
   RISK
============================================================ */

.risk-section {
    margin-top: 20px;
}

.risk-heading {
    color: #718096;

    font-family: Consolas, monospace;
    font-size: 10px;
    font-weight: bold;

    margin-bottom: 8px;
}

.risk-track {
    width: 100%;
    height: 9px;

    background: #111A25;

    border-radius: 10px;

    overflow: hidden;
}

.risk-fill {
    width: 0%;
    height: 100%;

    background: #FF1744;

    border-radius: 10px;

    transition: width 1s ease;
}

/* ============================================================
   INFORMATION BOXES
============================================================ */

.box-title {
    font-family: Consolas, monospace;
    font-size: 12px;
    font-weight: bold;

    margin-top: 20px;
    margin-bottom: 8px;
}

.reason-box {
    min-height: 130px;

    background: #080D14;

    border: 1px solid #14202D;
    border-radius: 12px;

    padding: 15px;

    color: #D8E0EA;

    font-family: Consolas, monospace;
    font-size: 11px;

    line-height: 1.7;

    white-space: pre-line;
}

.advice-box {
    min-height: 75px;

    background: #08131A;

    border: 1px solid #14202D;
    border-radius: 12px;

    padding: 15px;

    color: #00B7FF;

    font-size: 12px;
    font-weight: bold;

    line-height: 1.6;
}

/* ============================================================
   RESET
============================================================ */

.reset-button {
    width: 100%;

    margin-top: 18px;

    padding: 11px;

    background: #111A25;
    color: #D8E0EA;

    border: 1px solid #263545;
    border-radius: 9px;

    font-family: Consolas, monospace;
    font-size: 10px;
    font-weight: bold;

    cursor: pointer;

    transition: .2s;
}

.reset-button:hover {
    background: #1A2635;
}

/* ============================================================
   FOOTER
============================================================ */

.footer {
    text-align: center;

    padding: 5px 0 15px;

    color: #344454;

    font-family: Consolas, monospace;
    font-size: 8px;
}

/* ============================================================
   RESPONSIVE
============================================================ */

@media(max-width: 900px) {

    .dashboard {
        grid-template-columns: 1fr;
    }

    .header {
        padding: 0 18px;
    }

    .brand-subtitle {
        display: none;
    }
}

@media(max-width: 550px) {

    .brand {
        font-size: 20px;
    }

    .shield {
        font-size: 27px;
    }

    .status {
        font-size: 9px;
    }

    .panel {
        padding: 15px;
    }

    .question {
        align-items: flex-start;
        gap: 10px;
    }

    .question-text {
        font-size: 11px;
    }

}

</style>
</head>


<body>

<canvas id="matrix"></canvas>

<div class="matrix-overlay"></div>


<!-- ========================================================
     HEADER
========================================================= -->

<header class="header">

    <div class="brand-area">

        <div class="shield">🛡</div>

        <div class="brand">
            CYBERSHIELD
        </div>

        <div class="brand-subtitle">
            / EXPERT SECURITY SYSTEM
        </div>

    </div>


    <div class="status">

        <span class="status-dot"></span>

        SYSTEM ONLINE

    </div>

</header>


<!-- ========================================================
     DASHBOARD
========================================================= -->

<main class="dashboard">


<!-- ========================================================
     LEFT PANEL
========================================================= -->

<section class="panel">


    <div class="visual">

        <div class="warning">
            ⚠
        </div>

        <div class="warning-text">
            THREAT DETECTION ACTIVE
        </div>

    </div>


    <div class="section-title">
        SECURITY ASSESSMENT
    </div>

    <div class="section-subtitle">
        Select the suspicious activity detected on the system.
    </div>


    <!-- R1 -->

    <div class="question">

        <div class="question-left">

            <span class="number">01</span>

            <span class="question-text">
                Multiple failed login attempts?
            </span>

        </div>

        <select id="failed_logins">

            <option value="No">No</option>
            <option value="Yes">Yes</option>

        </select>

    </div>


    <!-- R2 -->

    <div class="question">

        <div class="question-left">

            <span class="number">02</span>

            <span class="question-text">
                Ransom note / file encryption?
            </span>

        </div>

        <select id="ransom_note">

            <option value="No">No</option>
            <option value="Yes">Yes</option>

        </select>

    </div>


    <!-- R3 -->

    <div class="question">

        <div class="question-left">

            <span class="number">03</span>

            <span class="question-text">
                Abnormally high outbound traffic?
            </span>

        </div>

        <select id="high_traffic">

            <option value="No">No</option>
            <option value="Yes">Yes</option>

        </select>

    </div>


    <!-- R4 -->

    <div class="question">

        <div class="question-left">

            <span class="number">04</span>

            <span class="question-text">
                Unauthorized popups / endpoint malware?
            </span>

        </div>

        <select id="popups">

            <option value="No">No</option>
            <option value="Yes">Yes</option>

        </select>

    </div>


    <!-- FIREWALL -->

    <div class="firewall-box">

        <div class="firewall-title">
            🔥 FIREWALL STATUS
        </div>

        <select id="firewall">

            <option value="enabled">
                ENABLED
            </option>

            <option value="disabled">
                DISABLED
            </option>

        </select>

    </div>


    <button
        class="analyze-button"
        onclick="analyzeThreat()"
    >
        ⚡ ANALYZE THREAT
    </button>


</section>


<!-- ========================================================
     RIGHT PANEL
========================================================= -->

<section class="panel">


    <div class="result-header">

        <div class="result-title">
            THREAT ANALYSIS
        </div>

        <div
            class="scan-status"
            id="scanStatus"
        >
            ● READY
        </div>

    </div>


    <!-- THREAT CARD -->

    <div class="threat-card">

        <div
            class="threat-icon"
            id="threatIcon"
        >
            ⚠
        </div>

        <div
            class="result-label"
            id="resultLabel"
        >
            SYSTEM READY
        </div>

        <div
            class="risk-label"
            id="riskLabel"
        >
            RISK LEVEL — UNKNOWN
        </div>

    </div>


    <!-- RISK -->

    <div class="risk-section">

        <div class="risk-heading">
            THREAT SEVERITY
        </div>

        <div class="risk-track">

            <div
                class="risk-fill"
                id="riskFill"
            ></div>

        </div>

    </div>


    <!-- REASONING -->

    <div class="box-title">
        🧠 INFERENCE REASONING
    </div>

    <div
        class="reason-box"
        id="reasonBox"
    >
SYSTEM READY

CyberShield will compare your selected
security indicators against the local
knowledge base and determine the matching
threat rule.
    </div>


    <!-- ADVICE -->

    <div class="box-title">
        🛡 RECOMMENDED ACTION
    </div>

    <div
        class="advice-box"
        id="adviceBox"
    >
        Complete the security assessment to receive
        a recommended defensive action.
    </div>


    <!-- RESET -->

    <button
        class="reset-button"
        onclick="resetSystem()"
    >
        ↻ RESET SCAN
    </button>


</section>

</main>


<footer class="footer">

    CYBERSHIELD • RULE-BASED INFERENCE ENGINE • SECURITY ANALYSIS

</footer>


<script>

/* ============================================================
   MATRIX EFFECT
============================================================ */

const canvas = document.getElementById("matrix");

const ctx = canvas.getContext("2d");

let width;
let height;

let columns = [];

const characters =
"01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%@<>[]{}";


function resizeCanvas() {

    width = canvas.width = window.innerWidth;

    height = canvas.height = window.innerHeight;

    const count = Math.floor(width / 22);

    columns = [];

    for (let i = 0; i < count; i++) {

        columns.push({
            x: i * 22,
            y: Math.random() * -height,
            speed: 2 + Math.random() * 6,
            length: 5 + Math.floor(Math.random() * 10)
        });

    }

}


function drawMatrix() {

    ctx.fillStyle = "rgba(2, 5, 10, 0.16)";

    ctx.fillRect(
        0,
        0,
        width,
        height
    );

    ctx.font = "10px Consolas";

    columns.forEach(column => {

        for (
            let i = 0;
            i < column.length;
            i++
        ) {

            const y =
                column.y -
                (i * 18);

            if (
                y > 0 &&
                y < height
            ) {

                let color = "#123044";

                if (i === 0) {

                    color = "#00B7FF";

                }

                else if (
                    Math.random() < 0.035
                ) {

                    color = "#FF1744";

                }

                ctx.fillStyle = color;

                const char =
                    characters[
                        Math.floor(
                            Math.random() *
                            characters.length
                        )
                    ];

                ctx.fillText(
                    char,
                    column.x,
                    y
                );

            }

        }


        column.y += column.speed;


        if (
            column.y -
            column.length * 18
            > height
        ) {

            column.y =
                Math.random() *
                -500;

            column.speed =
                2 + Math.random() * 6;

        }

    });


    requestAnimationFrame(drawMatrix);

}


window.addEventListener(
    "resize",
    resizeCanvas
);


resizeCanvas();

drawMatrix();


/* ============================================================
   FIND SELECTED THREAT
============================================================ */

function getSelectedThreat() {

    const threats = [
        "failed_logins",
        "ransom_note",
        "high_traffic",
        "popups"
    ];


    for (
        const threat of threats
    ) {

        if (
            document.getElementById(threat).value
            === "Yes"
        ) {

            return threat;

        }

    }


    return null;

}


/* ============================================================
   ANALYZE
============================================================ */

async function analyzeThreat() {

    const threat =
        getSelectedThreat();


    const firewall =
        document.getElementById(
            "firewall"
        ).value;


    const scanStatus =
        document.getElementById(
            "scanStatus"
        );


    const resultLabel =
        document.getElementById(
            "resultLabel"
        );


    const riskLabel =
        document.getElementById(
            "riskLabel"
        );


    const threatIcon =
        document.getElementById(
            "threatIcon"
        );


    const riskFill =
        document.getElementById(
            "riskFill"
        );


    const reasonBox =
        document.getElementById(
            "reasonBox"
        );


    const adviceBox =
        document.getElementById(
            "adviceBox"
        );


    if (!threat) {

        resultLabel.textContent =
            "NO THREAT INDICATOR";

        resultLabel.style.color =
            "#00B7FF";

        riskLabel.textContent =
            "RISK LEVEL — UNKNOWN";

        scanStatus.textContent =
            "● NO INPUT";

        scanStatus.style.color =
            "#00B7FF";

        riskFill.style.width =
            "0%";

        threatIcon.textContent =
            "✓";

        threatIcon.style.color =
            "#00FF9D";

        reasonBox.textContent =
`NO RULE MATCH

No suspicious indicator was selected.

Select at least one security indicator
and run the analysis again.`;

        adviceBox.textContent =
            "Continue monitoring the system.";

        return;

    }


    scanStatus.textContent =
        "● ANALYZING...";

    scanStatus.style.color =
        "#FF1744";


    resultLabel.textContent =
        "ANALYZING THREAT...";


    resultLabel.style.color =
        "#FF1744";


    reasonBox.textContent =
        "Inference engine is evaluating the knowledge base...";


    await new Promise(
        resolve =>
            setTimeout(
                resolve,
                500
            )
    );


    try {

        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        symptom: threat,

                        firewall: firewall

                    })

                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                "Analysis failed"
            );

        }


        const risk =
            result.severity;


        resultLabel.textContent =
            result.threat;


        riskLabel.textContent =
            "RISK LEVEL — " +
            risk;


        scanStatus.textContent =
            "● THREAT ANALYZED";


        scanStatus.style.color =
            "#00FF9D";


        /* ====================================================
           RISK METER
        ==================================================== */

        let percentage = 20;


        if (
            risk === "CRITICAL" ||
            risk === "CRITICAL HAZARD"
        ) {

            percentage = 100;

        }

        else if (
            risk === "HIGH"
        ) {

            percentage = 80;

        }

        else if (
            risk === "MEDIUM"
        ) {

            percentage = 55;

        }

        else if (
            risk === "LOW"
        ) {

            percentage = 25;

        }


        riskFill.style.width =
            percentage + "%";


        /* ====================================================
           COLORS
        ==================================================== */

        if (
            risk === "HIGH" ||
            risk === "CRITICAL" ||
            risk === "CRITICAL HAZARD"
        ) {

            resultLabel.style.color =
                "#FF1744";

            riskLabel.style.color =
                "#FF4D6D";

            threatIcon.textContent =
                "⚠";

            threatIcon.style.color =
                "#FF1744";

            adviceBox.style.color =
                "#FF4D6D";

        }

        else if (
            risk === "MEDIUM"
        ) {

            resultLabel.style.color =
                "#00B7FF";

            riskLabel.style.color =
                "#00B7FF";

            threatIcon.textContent =
                "⚠";

            threatIcon.style.color =
                "#00B7FF";

            adviceBox.style.color =
                "#00B7FF";

        }

        else {

            resultLabel.style.color =
                "#00FF9D";

            riskLabel.style.color =
                "#00FF9D";

            threatIcon.textContent =
                "✓";

            threatIcon.style.color =
                "#00FF9D";

            adviceBox.style.color =
                "#00FF9D";

        }


        /* ====================================================
           REASONING
        ==================================================== */

        let reasoning =
`RULE MATCH DETECTED

Threat:
${result.threat}

Severity:
${result.severity}

Diagnosis:
${result.diagnosis}

Rule-based inference:
The selected security indicator matched
a rule in the CyberShield knowledge base.`;


        if (
            firewall === "disabled"
        ) {

            reasoning +=
`

Firewall override:
Firewall is disabled, therefore the
inference engine escalated the severity
to CRITICAL HAZARD.`;

        }


        reasonBox.textContent =
            reasoning;


        /* ====================================================
           RECOMMENDED ACTIONS
        ==================================================== */

        let actions = "";


        if (
            Array.isArray(
                result.actions
            )
        ) {

            actions =
                result.actions
                    .map(
                        action =>
                            "• " + action
                    )
                    .join("\n");

        }


        adviceBox.textContent =
            actions ||
            "Follow standard security procedures.";


    }

    catch (error) {

        console.error(error);


        resultLabel.textContent =
            "SYSTEM ERROR";


        resultLabel.style.color =
            "#FF1744";


        scanStatus.textContent =
            "● ERROR";


        scanStatus.style.color =
            "#FF1744";


        threatIcon.textContent =
            "✕";


        threatIcon.style.color =
            "#FF1744";


        reasonBox.textContent =
            "Unable to connect to the CyberShield inference engine.\n\n"
            + error.message;


        adviceBox.textContent =
            "Check the Flask server and try again.";

    }

}


/* ============================================================
   RESET
============================================================ */

function resetSystem() {

    document.getElementById(
        "failed_logins"
    ).value = "No";


    document.getElementById(
        "ransom_note"
    ).value = "No";


    document.getElementById(
        "high_traffic"
    ).value = "No";


    document.getElementById(
        "popups"
    ).value = "No";


    document.getElementById(
        "firewall"
    ).value = "enabled";


    document.getElementById(
        "resultLabel"
    ).textContent =
        "SYSTEM READY";


    document.getElementById(
        "resultLabel"
    ).style.color =
        "#00B7FF";


    document.getElementById(
        "riskLabel"
    ).textContent =
        "RISK LEVEL — UNKNOWN";


    document.getElementById(
        "riskLabel"
    ).style.color =
        "#718096";


    document.getElementById(
        "scanStatus"
    ).textContent =
        "● READY";


    document.getElementById(
        "scanStatus"
    ).style.color =
        "#00B7FF";


    document.getElementById(
        "threatIcon"
    ).textContent =
        "⚠";


    document.getElementById(
        "threatIcon"
    ).style.color =
        "#FF1744";


    document.getElementById(
        "riskFill"
    ).style.width =
        "0%";


    document.getElementById(
        "reasonBox"
    ).textContent =
`SYSTEM READY

CyberShield will compare your selected
security indicators against the local
knowledge base and determine the matching
threat rule.`;


    document.getElementById(
        "adviceBox"
    ).textContent =
        "Complete the security assessment to receive a recommended defensive action.";

}

</script>

</body>
</html>
"""


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template_string(HTML)


# ============================================================
# ANALYZE API
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No input received."
        }), 400


    symptom = data.get("symptom")

    firewall = data.get(
        "firewall",
        "enabled"
    )


    # Validate symptom

    valid_symptoms = [
        rule["symptom"]
        for rule in RULES
    ]


    if symptom not in valid_symptoms:

        return jsonify({
            "error": "Invalid threat indicator."
        }), 400


    # ========================================================
    # CALL INFERENCE ENGINE
    # ========================================================

    result = analyze_threat(
        symptom,
        firewall
    )


    return jsonify(result)


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("=" * 60)
    print(" CYBERSHIELD - CYBERSECURITY EXPERT SYSTEM")
    print("=" * 60)
    print("")
    print(" Open your browser:")
    print(" http://127.0.0.1:5000")
    print("")
    print(" Network access:")
    print(" http://localhost:5000")
    print("")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

