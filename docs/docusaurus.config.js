// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AutoPOM-Agent',
  tagline: 'Autonomous Web Discovery and Multi-language Playwright POM Generation',
  favicon: 'img/logo.svg',

  url: process.env.DOCS_URL || 'https://vinipx.github.io',
  baseUrl: process.env.DOCS_BASE_URL || '/elementor/',

  organizationName: 'vinipx',
  projectName: 'elementor',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/vinipx/elementor/tree/main/docs/',
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    ({
      image: 'img/logo.svg',

      mermaid: {
        theme: {
          light: "base",
          dark: "dark",
        },
        options: {
          themeVariables: {
            primaryColor: "#1a1a2e",
            primaryTextColor: "#e2e8f0",
            primaryBorderColor: "#3b82f6",
            lineColor: "#60a5fa",
            secondaryColor: "#1e1e2e",
            tertiaryColor: "#eff6ff",
          },
        },
      },

      announcementBar: {
        id: "autopom_v1",
        content:
          '🤖 AutoPOM-Agent — AI autonomous crawling + resilient selector mapping + Java/JavaScript/TypeScript Playwright POM synthesis.',
        backgroundColor: "#111111",
        textColor: "#d4d4d8",
        isCloseable: true,
      },

      colorMode: {
        defaultMode: "dark",
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },

      navbar: {
        title: 'AutoPOM-Agent',
        logo: {
          alt: 'AutoPOM-Agent Logo',
          src: 'img/logo.svg',
          srcDark: 'img/logo-dark.svg',
          width: 36,
          height: 36,
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docs',
            position: 'left',
            label: 'Documentation',
          },
          {
            to: "/docs/getting-started/quickstart",
            label: "Getting Started",
            position: "left",
          },
          {
            to: "/docs/architecture/overview",
            label: "Architecture",
            position: "left",
          },
          {
            type: "dropdown",
            label: "Core Guides",
            position: "left",
            items: [
              { label: "Configuration", to: "/docs/getting-started/configuration" },
              { label: "Agentic Loop", to: "/docs/guides/agentic-loop" },
              { label: "State Management", to: "/docs/guides/state-management" },
              { label: "Element Mapping", to: "/docs/guides/element-mapping" },
              { label: "POM Generation", to: "/docs/guides/java-generation" },
              { label: "Self-Healing", to: "/docs/guides/self-healing" },
            ],
          },
          {
            type: "dropdown",
            label: "Tutorials",
            position: "left",
            items: [
              { label: "First Crawl", to: "/docs/tutorials/first-run" },
              { label: "Authenticated Crawl", to: "/docs/tutorials/authenticated-crawl" },
              { label: "Custom Selector Policies", to: "/docs/tutorials/custom-selectors" },
            ],
          },
          {
            type: "dropdown",
            label: "Use Cases",
            position: "left",
            items: [
              { label: "E-commerce App", to: "/docs/use-cases/ecommerce-webapp" },
              { label: "Internal Portal", to: "/docs/use-cases/internal-portal" },
            ],
          },
          {
            to: "/docs/api/core-interfaces",
            label: "API Reference",
            position: "left",
          },
          {
            type: "dropdown",
            label: "Resources",
            position: "left",
            items: [
              {
                to: "/docs/troubleshooting/common-issues",
                label: "Troubleshooting",
              },
              {
                to: "/docs/contributing/guidelines",
                label: "Contributing",
              },
              {
                to: "/docs/changelog",
                label: "Changelog",
              },
            ],
          },
          {
            href: 'https://github.com/vinipx/elementor',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              { label: 'Getting Started', to: '/docs/getting-started/quickstart' },
              { label: 'Configuration', to: '/docs/getting-started/configuration' },
              { label: 'Architecture', to: '/docs/architecture/overview' },
              { label: 'API Reference', to: '/docs/api/core-interfaces' },
            ],
          },
          {
            title: 'Guides',
            items: [
              { label: 'Agentic Loop', to: '/docs/guides/agentic-loop' },
              { label: 'State Management', to: '/docs/guides/state-management' },
              { label: 'Self-Healing', to: '/docs/guides/self-healing' },
            ],
          },
          {
            title: 'Tutorials',
            items: [
              { label: 'First Crawl', to: '/docs/tutorials/first-run' },
              { label: 'Authenticated Crawl', to: '/docs/tutorials/authenticated-crawl' },
              { label: 'Use Cases', to: '/docs/use-cases/ecommerce-webapp' },
            ],
          },
          {
            title: 'Links',
            items: [
              { label: 'GitHub', href: 'https://github.com/vinipx/elementor' },
              { label: 'Contributing', to: '/docs/contributing/guidelines' },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AutoPOM-Agent — MIT License`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: [
          "python",
          "java",
          "bash",
          "json",
          "yaml",
          "markdown",
        ],
      },
    }),
};

export default config;
