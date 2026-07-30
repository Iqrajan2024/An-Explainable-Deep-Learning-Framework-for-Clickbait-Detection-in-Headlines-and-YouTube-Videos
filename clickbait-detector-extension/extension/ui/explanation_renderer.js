/*
===========================================================
ClickDetect AI
Explanation Renderer

Prediction Popup

Displays only:

• Important Words
• Positive Indicators
• Negative Indicators

===========================================================
*/

export class ExplanationRenderer {

    constructor() {}

    render(response){

    const explanation =
        response.explanation || {};

    const positive =
        explanation.positive_words || [];

    const negative =
        explanation.negative_words || [];

    const important =
        explanation.important_words || [];

    return `

<div class="cd-summary-card">

    <div class="cd-section-title">

        Key Influential Words

    </div>

    <div class="cd-chip-container">

        ${important.map(item=>`

            <span class="cd-chip">

                ${item.word}

            </span>

        `).join("")}

    </div>

</div>

`;

}

     renderWords(words, css){

        if(!words.length){

            return `

    <p class="cd-none">

        None

    </p>

    `;

        }

        return words.map(item=>`

    <span class="cd-chip ${css}">

        ${item.word}

    </span>

    `).join("");

    }


}

