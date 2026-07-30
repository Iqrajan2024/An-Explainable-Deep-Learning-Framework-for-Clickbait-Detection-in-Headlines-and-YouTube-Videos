/*
===========================================================
ClickDetect AI
Content Controller

Responsibilities
----------------
• Initialize extension
• Coordinate all modules
• Handle hover events
• Call backend
• Update popup
• Highlight links

No prediction logic.
No rendering logic.
No preprocessing logic.

===========================================================
*/

import { HoverDetector } from "./hover_detector.js";
import { PopupManager } from "./popup_manager.js";
import { LinkHighlighter } from "./link_highlighter.js";

import { ArticleService } from "../services/article_service.js";
import { YoutubeService } from "../services/youtube_service.js";
import { ApiService } from "../services/api.js";

export class ClickDetectController {

    constructor() {

        //----------------------------------------
        // Services
        //----------------------------------------

        this.articleService =
            new ArticleService();

        this.youtubeService =
            new YoutubeService();

        this.api =
            new ApiService();

        //----------------------------------------
        // UI
        //----------------------------------------

        this.popup =
            new PopupManager();

        this.highlighter =
            new LinkHighlighter();

        //----------------------------------------
        // Hover Detection
        //----------------------------------------

        this.detector =
            new HoverDetector(this);

        //----------------------------------------
        // Simple Cache
        //----------------------------------------

        this.cache =
            new Map();

        console.log(
            "ClickDetect AI initialized."
        );

    }

    //======================================================
    // Headline Hover
    //======================================================

    async handleArticleHover(element) {

        try {

            //----------------------------------
            // Extract
            //----------------------------------

            const article =
                this.articleService.extract(element);

            if (!article)
                return;

            //----------------------------------
            // Cache
            //----------------------------------

            const key =
                article.url;

            if (this.cache.has(key)) {

                const cached =
                    this.cache.get(key);

                this.popup.showArticle(
                    element,
                    cached
                );

                this.highlighter.highlight(
                    element,
                    cached.color
                );

                return;

            }

            //----------------------------------
            // Loading
            //----------------------------------

            this.popup.showLoading(element);

            //----------------------------------
            // Backend
            //----------------------------------

            const response =
                await this.api.predictHeadline(
                    article
                );

            console.log("ARTICLE RESPONSE");
            console.log(response);

            if (!response) {

                this.popup.showError(
                    element,
                    "Unable to contact backend."
                );

                return;

            }

            const popupData = {

                ...response,

                headline: article.headline,

                url: article.url,

                domain: article.domain

            };

            this.cache.set(
                key,
                popupData
            );

            this.popup.showArticle(
                element,
                popupData
            );



            this.highlighter.highlight(
                element,
                response.prediction.color
            );

        }

        catch (error) {

            console.error(error);

        }

    }

    //======================================================
    // YouTube Hover
    //======================================================

    async handleYoutubeHover(element) {
        console.log("HANDLE YOUTUBE HOVER");

        try {

            //----------------------------------
            // Extract
            //----------------------------------

            const video =
                this.youtubeService.extract(element);

            if (!video)
                return;

            //----------------------------------
            // Cache
            //----------------------------------

            const key =
                video.videoId;

            if (this.cache.has(key)) {

                const cached =
                    this.cache.get(key);

                this.popup.showYoutube(
                    element,
                    cached
                );

                this.highlighter.highlight(
                    element,
                    cached.color
                );

                return;

            }

            //----------------------------------
            // Loading
            //----------------------------------

            this.popup.showLoading(element);

            //----------------------------------
            // Backend
            //----------------------------------

            const response =
                await this.api.predictYoutube(
                    video
                );



            console.log("VIDEO EXTRACTED");
            console.log(video);

            console.log("BACKEND RESPONSE:", response);
            console.log("JSON:", JSON.stringify(response, null, 2));



            if (!response) {

                this.popup.showError(
                    element,
                    "Unable to contact backend."
                );

                return;

            }

            //----------------------------------
            // Build Popup Data
            //----------------------------------

            const popupData = {

                ...response,

                title: response.title,

                thumbnail: response.thumbnail,

                channel_title: response.channel_title,

                videoId: video.videoId

            };

            //----------------------------------
            // Cache
            //----------------------------------

            this.cache.set(
                key,
                popupData
            );

            //----------------------------------
            // UI
            //----------------------------------


            this.popup.showYoutube(
                video.titleElement,
                popupData
            );

            this.highlighter.highlight(
                video.titleElement,
                response.prediction.color
            );

        }

        catch (error) {

            console.error("YOUTUBE ERROR");

            console.error(error);

            console.error(error.stack);

        }

    }

}

//==========================================================
// Initialize Extension
//==========================================================

new ClickDetectController();