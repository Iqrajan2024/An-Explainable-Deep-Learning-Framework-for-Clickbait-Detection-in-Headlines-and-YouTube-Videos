/*
===========================================================
ClickDetect AI
Article Renderer

Prediction Popup
===========================================================
*/

import { ConfidenceRenderer } from "./confidence_renderer.js";
import { ExplanationRenderer } from "./explanation_renderer.js";

export class ArticleRenderer {

    constructor() {

        this.confidenceRenderer =
            new ConfidenceRenderer();

        this.explanationRenderer =
            new ExplanationRenderer();

    }

    render(response) {

        const confidence =
            this.confidenceRenderer.render(response);

        const explanation =
            this.explanationRenderer.render(response);

        return `


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

        ${explanation}

        <div class="cd-footer">

            <button
                id="cd-why-btn"
                class="cd-primary-btn">

                View Full Analysis →

            </button>

        </div>

    </div>


`;

    }

}