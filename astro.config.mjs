import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://forgeyourhabit.com',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ar', 'tr'],
    routing: { prefixDefaultLocale: false },
  },
});
