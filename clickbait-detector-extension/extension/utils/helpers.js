/*
===========================================================
ClickDetect AI
Helper Functions

Shared utility functions used throughout
the browser extension.

===========================================================
*/

//==========================================================
// Format Confidence
//==========================================================

export function formatConfidence(value) {

    const confidence = Number(value);

    if (Number.isNaN(confidence))
        return "0.0%";

    return `${confidence.toFixed(1)}%`;

}

//==========================================================
// Escape HTML
//==========================================================

export function escapeHTML(text) {

    if (text === null || text === undefined)
        return "";

    const div = document.createElement("div");

    div.textContent = String(text);

    return div.innerHTML;

}

//==========================================================
// Truncate Text
//==========================================================

export function truncate(text, maxLength = 120) {

    if (!text)
        return "";

    if (text.length <= maxLength)
        return text;

    return text.substring(0, maxLength) + "...";

}

//==========================================================
// Debounce
//==========================================================

export function debounce(func, delay) {

    let timeout;

    return (...args) => {

        clearTimeout(timeout);

        timeout = setTimeout(() => {

            func(...args);

        }, delay);

    };

}

//==========================================================
// Clamp Value
//==========================================================

export function clamp(value, min, max) {

    return Math.min(

        Math.max(value, min),

        max

    );

}

//==========================================================
// Generate Cache Key
//==========================================================

export function createCacheKey(type, id) {

    return `${type}:${id}`;

}

//==========================================================
// Safe Array
//==========================================================

export function safeArray(value) {

    if (Array.isArray(value))
        return value;

    return [];

}

//==========================================================
// Safe String
//==========================================================

export function safeString(value) {

    if (value === null || value === undefined)
        return "";

    return String(value).trim();

}