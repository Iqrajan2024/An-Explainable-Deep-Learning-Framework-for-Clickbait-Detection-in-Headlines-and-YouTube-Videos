/*
===========================================================
ClickDetect AI
Prediction Card
===========================================================
*/

export class PredictionCard {

    render(response) {

        const prediction =
            response.prediction || "Unknown";

        const confidence =
            Number(response.confidence || 0).toFixed(0);

        const badge =
            response.badge || "";

        const color =
            response.color || "#2563EB";

        return `

<div class="cd-prediction-card">

    <div
        class="cd-confidence-circle"
        style="border-color:${color}; color:${color};"
    >

        <span class="cd-circle-number">

            ${confidence}%

        </span>

    </div>

    <div
        class="cd-prediction-title"
        style="color:${color};"
    >

        ${prediction.toUpperCase()}

    </div>

    <div class="cd-confidence-badge">

        ${badge}

    </div>

</div>

`;

    }

}