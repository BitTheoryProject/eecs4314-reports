# EECS4314 Reports - Bit Theory

Website can be viewed [here](https://bittheoryproject.github.io/eecs4314-project/).

- Reports in `a1/ a2/ a3/ a4/` in will be automatically compiled to pdf via `/.github/workflows` and published on merges to `prod` branch.
- Report structure:
  - `/a1/report.tex` -- report LaTeX
  - `/a1/report.pdf` -- compiled pdf
  - `/a1/assets/` -- any relevant images and other resources for this report
- PlantUML files (`**.pu` & `**.puml`) will be built into `svgs` of the same name/directory upon merges to the `main` branch.
  - So upon any changes to `**.pu` or `**.puml` files, make sure to run `git pull origin` once the action completes.

## Tutorial on Basics of LaTeX

- Go to `/tutorial/report.tex` and see the basic syntax and the corresponding `/tutorial/report.pdf`.
## How to Update the Reports

Note: The changes to the reports should be pushed to the  `main` branch locally until ready to be merged to `prod`.

1. Pull the repo: `git pull https://github.com/BitTheoryProject/eecs4314-reports.git`
2. Checkout to main: `git checkout main`
3. Update report your're working on: `a1/ a2/ a3/ a4/`
4. Add your changes: `git add .`
5. Give descriptive name to your changes: `git commit -m "Added sequence diagram to a1"`
6. Push your changes when you're ready to merge to prod: `git push`
5. Go to github and create [pull-request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) from `main` to `prod`, add reviewers, and when ready merge to `prod` and the reports should be updated automatically.

## Reports

- [Conceptual Architecture Report](https://bittheoryproject.github.io/eecs4314-reports/a1/report-lualatex.pdf)
- [Concrete Architecture Report](https://bittheoryproject.github.io/eecs4314-reports/a2/report-lualatex.pdf)
- [Dependency Extraction Report](https://bittheoryproject.github.io/eecs4314-reports/a3/report-lualatex.pdf)
- [Architecture Enhancement Report](https://bittheoryproject.github.io/eecs4314-reports/a4/report-lualatex.pdf)
