// @ts-check
import { defineConfig } from 'astro/config';
import pagefind from "astro-pagefind";
// https://astro.build/config
export default defineConfig({
    site: 'https://hieutran106.github.io',
    base: 'lmao/',
    build: {
        format: "file"
    },
    integrations: [pagefind()],
});
