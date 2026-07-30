/*
===========================================================
ClickDetect AI
YouTube Renderer

Responsibilities
----------------
• Build YouTube popup
• Combine reusable UI sections
• Return HTML only

No DOM manipulation.
No API calls.
No prediction.

===========================================================
*/

import { ConfidenceRenderer } from "./confidence_renderer.js";
import { VisualizationRenderer } from "./visualization_renderer.js";
import { Header } from "./components/header.js";

export class YoutubeRenderer {

    constructor() {

        this.confidenceRenderer =
            new ConfidenceRenderer();

        this.visualizationRenderer =
            new VisualizationRenderer();

        this.header =
            new Header();

    }

    //======================================================
    // Render
    //======================================================

    render(response) {

    const confidence =
        this.confidenceRenderer.render(response);

    const important =
        response.explanation?.text?.important_words || [];


    return `

<div class="cd-popup">

    <div class="cd-header">

        <div class="cd-title">

            ClickDetect AI

        </div>

        <button
            id="cd-close-btn"
            class="cd-icon-btn">

            ✕

        </button>

    </div>

    <div class="cd-body">

        ${confidence}

        <div class="cd-summary-card">

            <div class="cd-section-title">

                Key Influential Words

            </div>

            <div class="cd-chip-container">

                ${
                    important.length
                    ?
                    important.map(item => `

                        <span class="cd-chip">

                            ${item.word}

                        </span>

                    `).join("")
                    :
                    `<span class="cd-none">None</span>`
                }

            </div>

        </div>


        <div class="cd-footer">

            <button
                id="cd-why-btn"
                class="cd-primary-btn">

                View Full Analysis →

            </button>

        </div>

    </div>

</div>

`;

}

}