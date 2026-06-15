# Applicant Profile — Index

```
06-Applicant-Profile/
├── Home.md                    ← Core identity + 4 differentiators
├── Evidence Bank.md           ← Single source of truth for all facts
├── Research Engineer.md       ← Industry R&D, lab, applied AI roles
├── PhD Profile.md            ← Academic PhD applications
├── Fellowship Profile.md       ← Google PhD, ELLIS, MSCA, ETH AI Center
├── Startup Profile.md         ← Technical founder, AI startup roles
├── LinkedIn Profile.md        ← LinkedIn-optimized About + Experience
├── CV.md                     ← Markdown one-page CV (browser-friendly)
├── cv.tex                    ← LaTeX one-page CV (compile to PDF)
├── Short Bios.md             ← Copy-paste: emails, forms, ATS, elevator
└── Index.md                   ← This file
```

---

## How to Use

1. **Pick your track** → open the relevant profile
2. **Check facts** → always verify against [[Evidence Bank]]
3. **Use quick copy blocks** → [[Short Bios]] for emails, forms, ATS
4. **Compile CV** → use `cv.tex` (LaTeX) or `CV.md` (markdown/browser)

## LaTeX CV Setup

```bash
# Install packages (Ubuntu)
sudo apt install texlive-latex-base texlive-latex-extra

# Compile
pdflatex cv.tex

# Or use Overleaf — copy-paste cv.tex content there
```

## Recommended LaTeX Editors
- **Overleaf** (cloud, no install) — best for quick sharing
- **VS Code + LaTeX Workshop** — best local experience
- **TeXShop** (macOS)
