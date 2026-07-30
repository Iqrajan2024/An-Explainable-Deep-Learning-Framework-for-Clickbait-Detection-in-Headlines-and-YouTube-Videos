/*
===========================================================
ClickDetect AI
Popup Manager
===========================================================
*/

import { ArticleRenderer } from "../ui/article_renderer.js";
import { YoutubeRenderer } from "../ui/youtube_renderer.js";
import { ExplanationPageRenderer } from "../ui/explanation_page_renderer.js";
import { YoutubeExplanationRenderer } from "../ui/youtube_explanation_renderer.js";
import { YoutubeMetadataRenderer } from "../ui/youtube_metadata_renderer.js";


export class PopupManager {

    constructor() {

        this.popup = null;

        this.articleRenderer = new ArticleRenderer();

        this.youtubeRenderer = new YoutubeRenderer();

        this.youtubeExplanationRenderer =
            new YoutubeExplanationRenderer();

        this.youtubeMetadataRenderer =
            new YoutubeMetadataRenderer();

        this.explanationPageRenderer =
            new ExplanationPageRenderer();

        this.lastElement = null;

        this.lastResponse = null;

        this.lastType = null;

        this.createPopup();

        this.registerEvents();

        this.originalResponse = null;



    }

    //======================================================
    // Create Popup
    //======================================================

    createPopup() {

        this.popup = document.createElement("div");

        this.popup.id = "clickdetect-popup";

        this.popup.className = "cd-popup-container";

        this.popup.style.display = "none";

        document.body.appendChild(this.popup);

    }

    //======================================================
    // Global Events
    //======================================================

    registerEvents() {


        // Click outside
        document.addEventListener("mousedown", (e) => {

            if (
                this.popup.style.display === "block" &&
                !this.popup.contains(e.target)
            ) {

                this.hide();

            }

        });

        // ESC key
        document.addEventListener("keydown", (e) => {

            if (e.key === "Escape") {

                this.hide();

            }

        });

    }

    //======================================================
    // Show Article
    //======================================================

    showArticle(element, response) {

        this.popup.style.width = "340px";
        this.popup.style.maxWidth = "340px";
        this.popup.style.height = "420px";

        this.lastElement = element;

        this.lastResponse = response;

        this.originalResponse = response;

        this.lastType = "article";

        this.positionPopup(element);

        this.popup.innerHTML =
            this.articleRenderer.render(response);

        this.attachEvents();

        this.show()

    }




    //======================================================
    // Show YouTube
    //======================================================

    showYoutube(element, response) {

        this.popup.style.width = "340px";
        this.popup.style.maxWidth = "340px";
        this.popup.style.height = "420px";

        this.lastElement = element;

        this.lastResponse = response;

        this.originalResponse = response;

        this.lastType = "youtube";

        this.positionPopup(element);

        this.popup.innerHTML =
            this.youtubeRenderer.render(response);

        this.attachEvents();

        this.show();
    }

    //======================================================
    // Show YouTube Explanation
    //======================================================

    showYoutubeExplanation() {

        this.popup.style.width = "340px";
        this.popup.style.maxWidth = "340px";
        this.popup.style.height = "420px";

        this.popup.innerHTML =
            this.youtubeExplanationRenderer.render(
                this.lastResponse
            );

        this.attachEvents();

    }

    showMetadataAnalysis(){

        this.popup.style.width = "340px";
        this.popup.style.maxWidth = "340px";
        this.popup.style.height = "420px";

        this.popup.innerHTML =
            this.youtubeMetadataRenderer.render(
                this.lastResponse
            );

        this.attachEvents();

    }



    //======================================================
    // Loading
    //======================================================

    showLoading() {

    this.popup.style.width = "220px";
    this.popup.style.maxWidth = "220px";
    this.popup.style.height = "60px";

    this.positionPopup();

    this.popup.innerHTML = `
        <div class="cd-loading-toast">

            <div class="cd-spinner"></div>

            <div class="cd-loading-text">
                Analyzing...
            </div>

        </div>
    `;

    this.show();

}

    showExplanation() {

        this.popup.style.width = "340px";
        this.popup.style.maxWidth = "340px";
        this.popup.style.height = "420px";

        this.popup.innerHTML =
            this.explanationPageRenderer.render(
                this.lastResponse
            );

        this.attachEvents();

    }


    attachEvents() {

    //-----------------------------------
    // Close
    //-----------------------------------

    const close =
        this.popup.querySelector("#cd-close-btn");

    if (close) {

        close.onclick = () => {

            this.hide();

        };

    }

    //-----------------------------------
    // View Full Analysis
    //-----------------------------------

    const why =
        this.popup.querySelector("#cd-why-btn");

    if (why) {

        why.onclick = () => {

            console.log("WHY BUTTON CLICKED");
            console.log("lastType =", this.lastType);

            if(this.lastType == "article"){

                this.showExplanation();

            }
            else{

                console.log("Opening YouTube explanation");

                this.showYoutubeExplanation();

            }

        };

    }


    //-----------------------------------
    // Metadata Analysis
    //-----------------------------------

    const metadata =
        this.popup.querySelector(
            "#cd-metadata-btn"
        );

    if (metadata) {

        metadata.onclick = () => {

            this.showMetadataAnalysis();

        };

    }

    const metadataBack =
        this.popup.querySelector(
            "#cd-metadata-back-btn"
        );

    if(metadataBack){

        metadataBack.onclick = () => {

            this.showYoutubeExplanation();

        };

    }

    //-----------------------------------
    // Back
    //-----------------------------------

    const back =
        this.popup.querySelector("#cd-back-btn");

    if (back) {

        back.onclick = () => {

            if (this.lastType === "article") {

                this.showArticle(
                    this.lastElement,
                    this.lastResponse
                );

            }

            else {

                this.showYoutube(
                    this.lastElement,
                    this.originalResponse
                );

            }

        };

    }



}




    //======================================================
    // Error
    //======================================================

    showError(element, message) {

    this.positionPopup(element);

    this.popup.innerHTML = `

<div class="cd-error-toast">

    <div class="cd-error-icon">

        <img
            src="${chrome.runtime.getURL("icons/alert-triangle.svg")}"
            alt="Warning"
        >

    </div>

    <div class="cd-error-text">

        Unable to connect to backend

    </div>

</div>
`;

    this.attachEvents();

    this.show();

}

    //======================================================
    // Position
    //======================================================

    positionPopup() {

        this.popup.style.position = "fixed";

        this.popup.style.right = "20px";

        this.popup.style.bottom = "20px";

        this.popup.style.left = "auto";

        this.popup.style.top = "auto";

        this.popup.style.zIndex = "999999";

    }
    //======================================================
    // Show
    //======================================================

    show() {

        this.popup.style.display = "block";

        requestAnimationFrame(() => {

            this.popup.classList.add("show");

        });

    }

    //======================================================
    // Hide
    //======================================================

    hide() {

        this.popup.classList.remove("show");

        setTimeout(() => {

            this.popup.style.display = "none";

        }, 180);

    }

}