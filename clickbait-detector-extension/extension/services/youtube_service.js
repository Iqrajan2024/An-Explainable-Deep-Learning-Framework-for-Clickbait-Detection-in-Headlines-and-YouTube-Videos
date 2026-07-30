/*
===========================================================
ClickDetect AI
YouTube Service

Responsibilities
----------------
• Extract YouTube video information
• Build standardized payload
• Return data for backend prediction

No API calls.
No rendering.
No prediction.

===========================================================
*/

export class YoutubeService {

    constructor() {}

    //======================================================
    // Main Extraction
    //======================================================

    extract(videoElement) {

    if (!videoElement)
        return null;

    // Find the parent YouTube video container
    const renderer =
        videoElement.closest(
            "ytd-rich-item-renderer, ytd-video-renderer, ytd-compact-video-renderer, yt-lockup-view-model"
        );

    if (!renderer)
        return null;

    // Always use the title link
    const titleElement =
        videoElement;

    //------------------------------------------
    // Video ID
    //------------------------------------------

    const videoId =
        this.extractVideoId(titleElement);

    //------------------------------------------
    // Title
    //------------------------------------------

    const title =
        this.extractTitle(titleElement);

    //------------------------------------------
    // Channel
    //------------------------------------------

    const channel_title =
        this.extractChannel(renderer);

    //------------------------------------------
    // Thumbnail
    //------------------------------------------

    const thumbnail =
        this.extractThumbnail(renderer);

    //------------------------------------------
    // Return
    //------------------------------------------

    const video = {

        videoId,

        title,

        channel_title,

        thumbnail,

        titleElement

    };

    console.log("VIDEO EXTRACTED", video);

    return video;

}


    //======================================================
    // Video ID
    //======================================================

    extractVideoId(videoElement) {

        try {

            const url =
                new URL(videoElement.href);

            return (
                url.searchParams.get("v") || ""
            );

        }

        catch {

            return "";

        }

    }
    //======================================================
    // Title
    //======================================================

   extractTitle(videoElement) {

        return (

            videoElement.getAttribute("aria-label") ||

            videoElement.textContent ||

            ""

        ).trim();

    }

    //======================================================
    // Channel
    //======================================================

   extractChannel(renderer) {

    const links =
        renderer.querySelectorAll("a");

    for (const link of links) {

        if (
            !link.classList.contains("ytLockupMetadataViewModelTitle")
        ) {
            return link.textContent.trim();
        }

    }

    return "";

}

    //======================================================
    // Thumbnail
    //======================================================

    extractThumbnail(renderer) {


        const img =
            renderer.querySelector("img");

        return img?.currentSrc || img?.src || "";

    }

}