/*
===========================================================
ClickDetect AI

YouTube Metadata Renderer

Popup 3

===========================================================
*/

export class YoutubeMetadataRenderer {

    constructor(){}

    render(response){

        const metadata =
            response.explanation?.metadata || {};

        const summary =
            metadata.summary ||
            "No metadata explanation available.";

        const important =
            metadata.important_features || [];

        const positive =
            metadata.positive_features || [];

        const negative =
            metadata.negative_features || [];

        return `

<div class = "cd-popup">

<div class="cd-header">

    <button
        id="cd-metadata-back-btn"
        class="cd-icon-btn">

        ←

    </button>

    <div class="cd-title">

        Metadata Analysis

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

            AI Reasoning

        </h3>

        <p class="cd-summary">

            ${summary}

        </p>

    </div>

    ${this.renderImportance(
        important,
        positive,
        negative
    )}



</div>
</div>

`;

    }


    renderImportance(features, positive, negative){

        if(!features.length){

            return `

<div class="cd-card">

    <h3>

        Most Influential Metadata Features

    </h3>

    <div class="cd-empty">

        No metadata available.

    </div>

</div>

`;

        }

        return `

<div class="cd-card">

    <h3>

        Most Influential Metadata Features

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

    ${features.map(item=>`

<div class="cd-feature">

    <div class="cd-feature-top">

        <span>

            ${item.feature}

        </span>

        <span>

            ${Math.abs(item.impact).toFixed(3)}

        </span>

    </div>

    <div class="cd-bar">

        <div
            class="cd-bar-fill ${item.direction}"
            style="width:${Math.min(
                Math.abs(item.impact)*3000,
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