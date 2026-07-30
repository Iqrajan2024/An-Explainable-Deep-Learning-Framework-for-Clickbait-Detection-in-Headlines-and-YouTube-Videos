/*
===========================================================
ClickDetect AI
Confidence Renderer
===========================================================
*/

export class ConfidenceRenderer {

    render(response) {

        const prediction =
            response.prediction.prediction;

        const confidence =
            response.prediction.confidence_percentage;

        const badge =
            response.prediction.badge;

        const color =
            response.prediction.color;

        const riskClass =
            prediction === "Clickbait"
                ? "danger"
                : "safe";

        return `

<div class="cd-result-card ${riskClass}">

    <div class="cd-score-circle"
         style="border-color:${color}; color:${color};">

        ${confidence.toFixed(0)}%

    </div>

    <div class="cd-result-text">

        <div class="cd-prediction-text">

            ${prediction.toUpperCase()}

        </div>

        <div class="cd-confidence-badge">

            ${badge}

        </div>

    </div>

</div>

`;

    }

}