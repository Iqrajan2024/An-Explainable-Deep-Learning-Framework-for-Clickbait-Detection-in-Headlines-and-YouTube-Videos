/*
===========================================================
ClickDetect AI

YouTube Explanation Renderer

Popup 2

===========================================================
*/

export class YoutubeExplanationRenderer {

    constructor(){}

    //======================================================
    // Render
    //======================================================

    render(response){

        const explanation =
            response.explanation || {};

        const summary =
            explanation.summary ||
            "No explanation available.";

        const title =
            response.title || "";

        const important =
            explanation.text?.important_words || [];

        const positive =
            explanation.text?.positive_words || [];

        const negative =
            explanation.text?.negative_words || [];

        return `


<div class="cd-popup">

<div class="cd-header">

    <button
        id="cd-back-btn"
        class="cd-icon-btn">

        ←

    </button>

    <div class="cd-title">

        Analysis Explanation

    </div>

    <button
        id="cd-close-btn"
        class="cd-icon-btn">

        ✕

    </button>

</div>



<div class="cd-body">

    <div class="cd-card">

        <h3>

            Video Title

        </h3>

        <p class="cd-headline">

            ${title}

        </p>

    </div>

    <div class="cd-card">

        <h3>

            AI Reasoning

        </h3>

        <p class="cd-summary">

            ${summary}

        </p>

    </div>


    ${this.renderImportance(
        important
    )}

    <div class="cd-footer">

        <button
            id="cd-metadata-btn"
            class="cd-primary-btn">

            View Metadata Analysis →

        </button>

    </div>

</div>

</div>

`;

    }



    //======================================================
    // Word Importance
    //======================================================

    renderImportance(words){

        if(!words.length){

            return `

<div class="cd-card">

    <h3>

        Most Influential Text Words

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

        Most Influential Text Words

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
            style="width:${Math.min(
                Math.abs(item.importance) * 400,
                100
            )}%">

        </div>

    </div>

</div>

`).join("")}

</div>

`;

    }

}