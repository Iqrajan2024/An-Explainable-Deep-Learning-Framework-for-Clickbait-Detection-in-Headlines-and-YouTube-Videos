/*
===========================================================
ClickDetect AI
Link Highlighter

Responsibilities
----------------
• Highlight analyzed links
• Restore original styling
• Prevent duplicate highlights

No API calls.
No rendering.
No prediction.

===========================================================
*/

export class LinkHighlighter {

    constructor() {

        this.previousElement = null;

        this.originalStyle = {};

    }

    //======================================================
    // Highlight
    //======================================================

    highlight(element, color) {

        if (!element)
            return;

        // Restore previous element
        this.clear();

        this.previousElement = element;

        this.originalStyle = {

            outline: element.style.outline,

            background: element.style.backgroundColor,

            transition: element.style.transition

        };

        element.style.transition =
            "all 0.2s ease";

        element.style.outline =
            `2px solid ${color}`;

        element.style.backgroundColor =
            `${color}20`;

    }

    //======================================================
    // Clear Highlight
    //======================================================

    clear() {

        if (!this.previousElement)
            return;

        this.previousElement.style.outline =
            this.originalStyle.outline;

        this.previousElement.style.backgroundColor =
            this.originalStyle.background;

        this.previousElement.style.transition =
            this.originalStyle.transition;

        this.previousElement = null;

        this.originalStyle = {};

    }

}