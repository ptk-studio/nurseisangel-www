# mochi-agent

This folder is generated and managed by the **Mochi factory's agents** (PTK Studio's agent setup). How the factory
works: [mochi-factory/README.md](https://github.com/ptk-studio/ptk-studio/blob/main/mochi-factory/README.md). The project's
worker writes it through PRs reviewed by the manager (t1-manager), and the Owner approves the plans. Don't edit it by
hand outside that process. It sits at the repo root, outside `docs/`, so GitHub Pages never serves it.

- `PROJECT.md`: what the site is, where it's built, who runs it.
- `METRICS.md`: the metric goals, how each is read, the latest readings.
- `HEALTH-CHECK.md`: the URLs and signals the manager checks every sweep.
- `RELEASE-CHECKS.md`: the checks after every publish.
- `FEEDBACK.md`: the feedback channel and its reading schedule.
- `JOURNAL.md`: dated notes on what changed and why.
- `plans/<YYYY>.md`: the yearly plan. Each plan has a `Status:` line (proposed, or approved with the date).
- `proposals/{pending,approved,rejected,completed}/`: proposals by state.

**Every PTK Studio project and its GitHub repos:** [mochi-factory/project-groups/PROJECTS.md](https://github.com/ptk-studio/ptk-studio/blob/main/mochi-factory/project-groups/PROJECTS.md).
