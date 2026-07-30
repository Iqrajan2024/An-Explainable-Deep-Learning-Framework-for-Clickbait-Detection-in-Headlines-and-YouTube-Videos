/*
===========================================================
ClickDetect AI
Application Constants

Central configuration file shared across
the entire browser extension.

===========================================================
*/

//==========================================================
// Backend
//==========================================================

export const API = {

    BASE_URL: "http://127.0.0.1:8000",

    HEADLINE_ENDPOINT: "/predict/headline",

    YOUTUBE_ENDPOINT: "/predict/youtube",

    REQUEST_TIMEOUT: 30000

};

//==========================================================
// Hover Detection
//==========================================================

export const HOVER = {

    DELAY: 500,

    CACHE_SIZE: 500

};

//==========================================================
// Popup
//==========================================================

export const POPUP = {

    OFFSET_X: 0,

    OFFSET_Y: 10,

    MAX_WIDTH: 380,

    Z_INDEX: 999999

};

//==========================================================
// Highlight Colors
//==========================================================

export const COLORS = {

    CLICKBAIT: "#E53935",

    NOT_CLICKBAIT: "#43A047",

    WARNING: "#FB8C00",

    UNKNOWN: "#9E9E9E"

};

//==========================================================
// Images
//==========================================================

export const IMAGE = {

    WIDTH: 224,

    HEIGHT: 224

};

//==========================================================
// Animation
//==========================================================

export const ANIMATION = {

    TRANSITION: "all 0.2s ease"

};

//==========================================================
// Messages
//==========================================================

export const MESSAGE = {

    LOADING: "Analyzing...",

    BACKEND_OFFLINE:
        "Unable to connect to ClickDetect backend.",

    UNKNOWN_ERROR:
        "Something went wrong.",

    NO_EXPLANATION:
        "No explanation available."

};