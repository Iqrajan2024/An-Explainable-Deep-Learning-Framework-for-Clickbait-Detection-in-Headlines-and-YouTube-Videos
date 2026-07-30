/*
===========================================================
ClickDetect AI
Article Service

Responsibilities
----------------
• Extract article information
• Validate extracted data
• Return standardized article object

No API calls.
No rendering.
No prediction.

===========================================================
*/

export class ArticleService {

    constructor() {}

    //======================================================
    // Extract Article Information
    //======================================================

    extract(linkElement) {

        if (!linkElement)
            return null;

        //----------------------------------------------
        // Headline
        //----------------------------------------------

        const headline = this.extractHeadline(
            linkElement
        );

        if (!headline)
            return null;

        //----------------------------------------------
        // URL
        //----------------------------------------------

        const url = linkElement.href || "";

        //----------------------------------------------
        // Domain
        //----------------------------------------------

        let domain = "";

        try {

            domain = new URL(url).hostname;

        }

        catch {

            domain = "";

        }

        //----------------------------------------------
        // Return Standard Object
        //----------------------------------------------

        return {

            headline: headline,

            url: url,

            domain: domain

        };

    }

    //======================================================
    // Extract Headline
    //======================================================

    extractHeadline(linkElement) {

        let text =
            linkElement.innerText ||
            linkElement.textContent ||
            "";

        text = text.trim();

        if (text.length === 0)
            return null;

        return text;

    }

}