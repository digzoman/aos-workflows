# AOS-W v0.9 rendered GitHub Pages preview

A GitHub source-code URL ending in blob/main/.../index.html is NOT a rendered interactive visualization.

For workflows that are intentionally public-safe, the repository contains a manually dispatched GitHub Actions workflow at .github/workflows/aosw-v09-pages.yml. Its only allowed example is a fictional six-audience workflow. It generates a self-contained HTML page, checks the explicit fictional demo allowlist and packages only public/index.html for GitHub Pages. The actual deployed URL must be reported by the GitHub Pages action and opened/validated before telling users the webpage is available.

It does NOT publish automatically when code changes or an AOS-W run advances. An authorized GitHub repository owner must configure GitHub Pages. This permission applies only to publishing the webpage; it is not a new human checkpoint for executing normal workflow tasks.

A private source repository does not automatically make GitHub Pages private. Private Pages access depends on the actual GitHub organization/plan and site access settings. Never publish live Ampgent/Bucket 9 agent-files, private prompts, credentials, customer data, unpublished pricing or campaign evidence without distinct scope-specific owner authorization, verified protected hosting and public/private content review.

For confidential workflows, first use an authenticated cloud/local HTML preview, or share the individual self-contained index.html file directly. Do not label a GitHub raw source URL as an interactive page. ZIP is the last resort for visualization, although the complete AOS-W installer still uses ZIP.

The public demo workflow is an explicit manual opt-in and is not deployed by the v0.9 release process.
