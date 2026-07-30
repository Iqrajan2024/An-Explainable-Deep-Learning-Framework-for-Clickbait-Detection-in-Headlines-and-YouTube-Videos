/*
===========================================================
ClickDetect AI
Explanation Page Renderer

Detailed Analysis Popup

===========================================================
*/

export class ExplanationPageRenderer {

    constructor(){}

    render(response){

        const explanation =
            response.explanation || {};

        const headline =
            response.headline || "";

        const summary =
            explanation.summary ||
            "No explanation available.";

        const important =
            explanation.important_words || [];

        const prediction =
            response.prediction?.label ||
            response.label ||
            "Unknown";

        const confidence =
            response.confidence_percentage ??
            response.confidence ??
            0;

        const badge =
            response.confidence_level ||
            "";

        return `

    <div class="cd-header">

        <button
            id="cd-back-btn"
            class="cd-icon-btn">

            ←

        </button>

        <div class="cd-title">

            Detailed Analysis

        </div>

        <button
            id="cd-close-btn"
            class="cd-icon-btn">

            ✕

        </button>

    </div>

    <div class="cd-body">

        ${this.renderHeadline(headline)}

        ${this.renderSummary(summary)}


        ${this.renderImportance(important)}

        <div class="cd-footer-note">

            Words importance shows which words had
            the greatest influence on the AI prediction.

        </div>

    </div>

    `;

    }

    renderHeadline(headline){

        return `

    <div class="cd-card">

        <h3>

            Headline

        </h3>

        <p class="cd-headline">

            ${headline}

        </p>

    </div>

    `;

    }

    renderSummary(summary){

        return `

    <div class="cd-card">

        <h3>

            AI Reasoning

        </h3>

        <p class="cd-summary">

            ${summary}

        </p>

    </div>

    `;

    }


    renderImportance(words){

    if(!words.length){

        return `

<div class="cd-card">

    <h3>

         Most Influential Words Importance

    </h3>

    <div class="cd-empty">

        No influential words available.

    </div>

</div>

`;

    }

    return `

<div class="cd-card">

    <h3>

        Most Influential Words Importance

    </h3>

    <div class="cd-legend">

    <div class="cd-legend-item">

        <span class="cd-legend-color increase"></span>

        Increases Clickbait Score

    </div>

    <div class="cd-legend-item">

        <span class="cd-legend-color decrease"></span>

        Reduces Clickbait Score

    </div>

</div>


    ${words.map(item => `

    <div class="cd-feature">

        <div class="cd-feature-top">

            <span>

                ${item.word}

            </span>

            <span>

                ${Math.abs(item.importance).toFixed(3)}

            </span>

        </div>

        <div class="cd-bar">

            <div
                class="cd-bar-fill ${item.direction}"
                style="width:${Math.min(Math.abs(item.importance)*400,100)}%">

            </div>

        </div>

    </div>

    `).join("")}

</div>

`;

}







  }

