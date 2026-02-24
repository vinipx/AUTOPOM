import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HeroBanner() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroBadge}>Autonomous Test Intelligence</div>
          <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
          <p className={styles.heroSubtitle}>
            AI spider for web discovery and multi-language Playwright Page Objects
          </p>
          <p className={styles.heroDescription}>
            AutoPOM-Agent self-navigates your application or attaches to your existing browser to map resilient selectors,
            infer semantic element names, and synthesize clean POM code (Java, JavaScript, or TypeScript) with
            built-in selector verification and session reuse.
          </p>
          <div className={styles.heroButtons}>
            <Link className={styles.heroPrimary} to="/docs/getting-started/quickstart">
              Get Started →
            </Link>
            <Link className={styles.heroSecondary} to="/docs/architecture/overview">
              View Architecture
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

const capabilityFeatures = [
  {
    badge: 'CRAWLER',
    color: '#2563eb',
    title: 'Autonomous & Hybrid Discovery',
    description:
      'Explores pages autonomously or attaches to existing browser sessions (CDP/Profiles) for manual/automated hybrid workflows.',
  },
  {
    badge: 'SEMANTIC',
    color: '#22c55e',
    title: 'DOM + Vision Mapping',
    description:
      'Combines compact DOM context and visual hints for accurate semantic naming such as closeModalButton and signInButton.',
  },
  {
    badge: 'SELECTORS',
    color: '#8b5cf6',
    title: 'Resilient Locator Strategy',
    description:
      'Builds ranked fallback selectors and avoids unstable IDs/classes common in React and styled-component ecosystems.',
  },
  {
    badge: 'POM',
    color: '#0ea5e9',
    title: 'POM Synthesis',
    description:
      'Transforms structured page models into compile-ready Playwright Page Object classes in Java, JavaScript, or TypeScript.',
  },
  {
    badge: 'AI',
    color: '#ef4444',
    title: 'Agentic Loop',
    description:
      'Observation -> Thought -> Action loop orchestrated by LangChain to make context-aware navigation and extraction decisions.',
  },
  {
    badge: 'HEALING',
    color: '#f59e0b',
    title: 'Self-Healing Verification',
    description:
      'Tests generated selectors immediately, promotes reliable fallbacks, and re-scores confidence before persisting outputs.',
  },
];

const coreFeatures = [
  {
    icon: '🧭',
    title: 'State-Aware Crawling',
    description:
      'Route + DOM fingerprint signatures prevent repeated traversal and infinite loops in dynamic SPAs.',
  },
  {
    icon: '🧠',
    title: 'Token-Efficient AI',
    description:
      'Only compact interactive context is sent to the model, reducing cost while preserving decision quality.',
  },
  {
    icon: '🧱',
    title: 'Schema-Driven Pipeline',
    description:
      'A strict JSON contract decouples crawl logic from code generation for maintainable, testable architecture.',
  },
  {
    icon: '☕',
    title: 'Language-Targeted Output',
    description:
      'Generate Java, JavaScript, or TypeScript page objects with descriptive names, encapsulated locators, and intent-level methods.',
  },
  {
    icon: '🔐',
    title: 'Auth-Aware Discovery',
    description:
      'Supports credentialed flows with environment-based secrets for deeper exploration of protected application areas.',
  },
  {
    icon: '📊',
    title: 'Actionable Reporting',
    description:
      'Produces crawl summaries, selector confidence metrics, and generated artifacts for quick review.',
  },
];

const techStack = [
  { name: 'Python', desc: 'Orchestration Core' },
  { name: 'LangChain', desc: 'Agent Loop' },
  { name: 'BrowserUse', desc: 'Browser Agent' },
  { name: 'Playwright', desc: 'Execution + Validation' },
  { name: 'OpenAI/Gemini', desc: 'Vision + Reasoning' },
  { name: 'JSON Schema', desc: 'Intermediate Contract' },
  { name: 'Generator Core', desc: 'Language Rendering' },
  { name: 'JavaScript/TypeScript/Java', desc: 'POM Output' },
  { name: 'Mermaid', desc: 'Architecture Diagrams' },
];

function CapabilitiesSection() {
  return (
    <section className={styles.capabilities}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>End-to-End Automation Intelligence</h2>
          <p>From autonomous crawl to production-ready Playwright Page Objects</p>
        </div>
        <div className={styles.capabilityGrid}>
          {capabilityFeatures.map((item, idx) => (
            <div key={idx} className={styles.capabilityCard}>
              <span className={styles.capabilityBadge} style={{ backgroundColor: item.color }}>
                {item.badge}
              </span>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function AIAgentSection() {
  return (
    <section className={styles.aiAgent}>
      <div className="container">
        <div className={styles.aiContent}>
          <div className={styles.aiBadge}>NEXT GENERATION</div>
          <h2>Autonomous Test Asset Generation</h2>
          <p>
            AutoPOM-Agent turns application exploration into actionable test automation assets by
            combining browser actions, semantic reasoning, and immediate selector verification.
          </p>
          <div className={styles.aiFeatures}>
            <div className={styles.aiFeatureItem}>
              <strong>Semantic Understanding</strong>
              <span>Maps meaningful names from labels, context, and icon hints instead of raw DOM noise.</span>
            </div>
            <div className={styles.aiFeatureItem}>
              <strong>Deterministic Code Synthesis</strong>
              <span>Generates consistent POM classes in Java, JavaScript, or TypeScript from a stable JSON schema contract.</span>
            </div>
            <div className={styles.aiFeatureItem}>
              <strong>Verification Before Save</strong>
              <span>Selectors are tested and healed immediately to reduce flaky generated artifacts.</span>
            </div>
          </div>
          <div className={styles.archCta}>
            <Link to="/docs/guides/agentic-loop" className={styles.heroPrimary}>
              Explore Agentic Loop →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function ArchitectureSection() {
  return (
    <section className={styles.architecture}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>Layered Architecture</h2>
          <p>Clear separation between discovery, reasoning, verification, and code generation</p>
        </div>
        <div className={styles.archDiagram}>
          <div className={styles.archLayer} data-layer="4">
            <div className={styles.archLabel}>Layer 4 - Multi-language POM Output</div>
            <div className={styles.archClasses}>
              BasePage · Page Objects · Reports
            </div>
          </div>
          <div className={styles.archLayer} data-layer="3">
            <div className={styles.archLabel}>Layer 3 - Synthesis & Healing</div>
            <div className={styles.archClasses}>
              Schema Mapping · Template Rendering · Selector Verification
            </div>
          </div>
          <div className={styles.archLayer} data-layer="2">
            <div className={styles.archLabel}>Layer 2 - Agentic Intelligence</div>
            <div className={styles.archClasses}>
              Observe -> Think -> Act · State Graph · Semantic Extraction
            </div>
          </div>
          <div className={styles.archLayer} data-layer="1">
            <div className={styles.archLabel}>Layer 1 - Browser Runtime</div>
            <div className={styles.archClasses}>
              BrowserUse Context · Playwright Actions · DOM & Screenshot Capture
            </div>
          </div>
        </div>
        <div className={styles.archCta}>
          <Link to="/docs/architecture/overview">Explore Full Architecture →</Link>
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>Built for Real-World Teams</h2>
          <p>Practical defaults and extension points for enterprise automation programs</p>
        </div>
        <div className={styles.featuresGrid}>
          {coreFeatures.map((item, idx) => (
            <div key={idx} className={styles.featureCard}>
              <div className={styles.featureIcon}>{item.icon}</div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function TechStackSection() {
  return (
    <section className={styles.techStack}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>Technology Stack</h2>
          <p>Composable tools optimized for quality, speed, and maintainability</p>
        </div>
        <div className={styles.techGrid}>
          {techStack.map((item, idx) => (
            <div key={idx} className={styles.techPill}>
              <span className={styles.techName}>{item.name}</span>
              <span className={styles.techDesc}>{item.desc}</span>
            </div>
          ))}
        </div>
        <div className={styles.archCta}>
          <Link to="/docs/getting-started/quickstart">View Setup Guide →</Link>
        </div>
      </div>
    </section>
  );
}

function QuickStartSection() {
  return (
    <section className={styles.quickStart}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>Quick Start</h2>
          <p>Run your first crawl and generate language-specific page objects</p>
        </div>
        <div className={styles.codeBlock}>
          <pre>
            <code>{`# guided enterprise runner (recommended)
bash run.sh

# or run directly
PYTHONPATH=src python3 -m autopom.cli.main \\
  --base-url "https://example.com" \\
  --pom-language "typescript" \\
  --browser-adapter "playwright"`}</code>
          </pre>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title="Autonomous POM Generation"
      description={`${siteConfig.title} documentation for architecture, configuration, guides, tutorials, and use cases.`}
    >
      <HeroBanner />
      <main>
        <CapabilitiesSection />
        <AIAgentSection />
        <ArchitectureSection />
        <FeaturesSection />
        <TechStackSection />
        <QuickStartSection />
      </main>
    </Layout>
  );
}
