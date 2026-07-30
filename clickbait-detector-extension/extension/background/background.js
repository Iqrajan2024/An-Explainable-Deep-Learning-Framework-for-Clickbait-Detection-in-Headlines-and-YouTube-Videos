/*
===========================================================
ClickDetect AI
Background Service Worker

Responsibilities

• Extension installation
• Startup initialization
• Future settings management
• Message relay (if needed)

No DOM manipulation.
No prediction.
No popup rendering.

===========================================================
*/

// ---------------------------------------------------------
// Extension Installed
// ---------------------------------------------------------

chrome.runtime.onInstalled.addListener(() => {

    console.log("======================================");
    console.log("ClickDetect AI Installed");
    console.log("Version 2.0");
    console.log("======================================");

});


// ---------------------------------------------------------
// Browser Startup
// ---------------------------------------------------------

chrome.runtime.onStartup.addListener(() => {

    console.log("ClickDetect AI Started");

});


// ---------------------------------------------------------
// Message Listener
// ---------------------------------------------------------

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    switch (message.type) {

        case "PING":

            sendResponse({
                success: true,
                message: "ClickDetect Background Active"
            });

            break;

        default:

            sendResponse({
                success: false,
                message: "Unknown message."
            });

    }

    return true;

});