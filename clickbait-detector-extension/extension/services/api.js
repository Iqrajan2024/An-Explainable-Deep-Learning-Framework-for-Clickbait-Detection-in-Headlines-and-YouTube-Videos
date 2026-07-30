/*
===========================================================
ClickDetect AI
Backend API Service

Responsibilities
----------------
• Send requests to FastAPI
• Parse JSON responses
• Handle network errors

No UI.
No rendering.
No DOM access.

===========================================================
*/

export class ApiService {

    constructor() {

        //------------------------------------------
        // Backend URL
        //------------------------------------------

        this.BASE_URL = "http://127.0.0.1:8000";

    }

    //======================================================
    // Generic POST Request
    //======================================================

    async post(endpoint, payload) {

        try {

            const response = await fetch(

                `${this.BASE_URL}${endpoint}`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify(payload)

                }

            );

            if (!response.ok) {

                throw new Error(

                    `Backend Error ${response.status}`

                );

            }

            return await response.json();

        }

        catch (error) {

            console.error(

                "API Error",

                error

            );

            return null;

        }

    }

    //======================================================
    // Headline Prediction
    //======================================================

    async predictHeadline(articleData) {

        return await this.post(

            "/predict/headline",

            {

                headline: articleData.headline

            }

        );

    }

    //======================================================
    // YouTube Prediction
    //======================================================

    

    async predictYoutube(videoData) {

        return await this.post(

            "/predict/youtube",

            {

                videoId: videoData.videoId

            }

        );

    }
}