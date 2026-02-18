/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    {
      type: "doc",
      id: "index",
      label: "Introduction",
    },
    {
      type: "category",
      label: "Getting Started",
      collapsed: false,
      items: ["getting-started/quickstart", "getting-started/configuration"],
    },
    {
      type: "category",
      label: "Architecture",
      collapsed: false,
      items: ["architecture/overview"],
    },
    {
      type: "category",
      label: "Core Guides",
      items: [
        "guides/agentic-loop",
        "guides/state-management",
        "guides/element-mapping",
        "guides/java-generation",
        "guides/self-healing",
      ],
    },
    {
      type: "category",
      label: "Tutorials",
      items: [
        "tutorials/first-run",
        "tutorials/authenticated-crawl",
        "tutorials/custom-selectors",
      ],
    },
    {
      type: "category",
      label: "Use Cases",
      items: ["use-cases/ecommerce-webapp", "use-cases/internal-portal"],
    },
    {
      type: "category",
      label: "API Reference",
      items: ["api/core-interfaces"],
    },
    {
      type: "category",
      label: "Troubleshooting",
      items: ["troubleshooting/common-issues"],
    },
    {
      type: "category",
      label: "Contributing",
      items: ["contributing/guidelines"],
    },
    {
      type: "doc",
      id: "changelog",
      label: "Changelog",
    },
  ],
};

export default sidebars;
