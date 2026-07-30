import { defineConfig } from "vite";

export default defineConfig({

    build: {

        outDir: "extension",

        emptyOutDir: false,

        rollupOptions: {

            input: {

                content: "extension/content/content.js"

            },

            output: {

                entryFileNames: "content.bundle.js"

            }

        }

    }

});