/*
===========================================================
ClickDetect AI
Visualization Renderer
===========================================================
*/

export class VisualizationRenderer {

    render(response) {

        const explanation =
            response.explanation || {};

        const words =
            explanation.important_words || [];

        if (!words.length)
            return "";

        return `

<div class="cd-importance">

    <h3>

        Feature Importance

    </h3>

    ${words.map(item => this.renderBar(item)).join("")}

</div>

`;

    }

    renderBar(item){

        const width =
            Math.min(
                Math.abs(item.importance) * 250,
                100
            );

        const positive =
            item.direction === "positive";

        return `

<div class="cd-bar-item">

    <div class="cd-bar-header">

        <span>

            "${item.word}"

        </span>

        <span>

            ${item.importance > 0 ? "+" : ""}
            ${item.importance.toFixed(2)}

        </span>

    </div>

    <div class="cd-bar">

        <div

            class="cd-fill ${positive ? "positive":"negative"}"

            style="width:${width}%">

        </div>

    </div>

</div>

`;

    }

}