/*
===========================================================
ClickDetect AI
Hover Detector

Responsibilities
----------------
• Detect hovered elements
• Identify Articles vs YouTube
• Apply hover delay
• Prevent duplicate requests
• Notify controller

No API calls.
No popup.
No rendering.

===========================================================
*/

export class HoverDetector {

    constructor(controller) {

        this.controller = controller;

        this.hoverDelay = 500;

        this.hoverTimer = null;

        this.currentElement = null;

        this.initialize();

    }

    //======================================================
    // Initialize
    //======================================================

    initialize() {

        document.addEventListener(

            "mouseover",

            this.onMouseOver.bind(this)

        );

        document.addEventListener(

            "mouseout",

            this.onMouseOut.bind(this)

        );

    }

    //======================================================
    // Mouse Enter
    //======================================================

onMouseOver(event) {

    let target = null;

    //--------------------------------------------------
    // YouTube
    //--------------------------------------------------

    if (window.location.hostname.includes("youtube.com")) {

        target = event.target.closest("a.ytLockupMetadataViewModelTitle");

    }

    //--------------------------------------------------
    // Other websites
    //--------------------------------------------------

    else {

        target = event.target.closest("a");

    }

    if (!target)
        return;

    if (target === this.currentElement)
        return;

    this.currentElement = target;

    clearTimeout(this.hoverTimer);

    this.hoverTimer = setTimeout(() => {

        this.processHover(target);

    }, this.hoverDelay);

}

    //======================================================
    // Mouse Leave
    //======================================================

    onMouseOut(event) {

        // Cancel only if we've actually left the current element
        if (
            this.currentElement &&
            event.relatedTarget &&
            this.currentElement.contains(event.relatedTarget)
        ) {
            return;
        }

        clearTimeout(this.hoverTimer);

        this.currentElement = null;

    }

    //======================================================
    // Hover Processing
    //======================================================

   processHover(element) {

    //--------------------------------------------------
    // YouTube
    //--------------------------------------------------

    if (window.location.hostname.includes("youtube.com")) {

        this.controller.handleYoutubeHover(element);

        return;

    }

    //--------------------------------------------------
    // Articles
    //--------------------------------------------------

    this.controller.handleArticleHover(element);

}





    //======================================================
    // Detect YouTube Links
    //======================================================

    isYoutube(url) {

        return (

            url.includes("youtube.com/watch") ||

            url.includes("youtu.be/")

        );

    }

}