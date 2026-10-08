# Setup guide (read once, then delete this file from the repo)

Everything you need to go live. Do the steps in order; it takes about 20 minutes.

---

## 1. Create the special profile repository

GitHub shows a repo's README on your profile only if the repo name **exactly equals your username**.

1. Go to https://github.com/new
2. Repository name: `SnehaPoojary20` (you'll see "This is a special repository" appear)
3. Visibility: **Public**
4. Leave "Add a README", `.gitignore` and licence **unchecked** (you're pushing your own files)
5. Click **Create repository**

## 2. Put the files on your computer and push

You're on Windows, so use **Git Bash** (installed with Git) or PowerShell. Download this folder from the chat, then:

```bash
cd path/to/SnehaPoojary20          # the folder with README.md inside
git init
git branch -M main
git add .
git commit -m "feat: new profile README with auto-updating stats"
git remote add origin https://github.com/SnehaPoojary20/SnehaPoojary20.git
git push -u origin main
```

If Git asks you to sign in, use your browser login or a Personal Access Token as the password.
If it says `user.name` is unknown: `git config --global user.name "Sneha Poojary"` and `git config --global user.email "snehapoojary2004@gmail.com"`, then commit again.

Where to write what:

| File | What it is | Edit it when |
|---|---|---|
| `README.md` | The page recruiters see | Projects, status, links change |
| `assets/hero.svg` | Animated banner | You want different role text or colours |
| `assets/stats.svg` | Stats card (**auto-generated**) | Never by hand, the Action overwrites it |
| `scripts/update_profile.py` | Fetches GitHub, LeetCode and Hashnode numbers | You change a username |
| `.github/workflows/update-profile.yml` | Runs the script every day | You change the schedule |
| `data/stats.json` | Snapshot from Apify, used as fallback | Auto-updated |

## 3. Turn the automation on

1. Repo → **Settings → Actions → General → Workflow permissions** → choose **Read and write permissions** → Save.
2. Repo → **Actions** tab → **Update profile** → **Run workflow**. Wait for the green tick.
3. Refresh your profile. The "GitHub contributions" tile now shows your real total (it shows `-` until the first run, because GitHub only exposes that number through its API).

**Optional, counts private work too:** create a fine-grained token (Settings → Developer settings → Personal access tokens) with read-only access to your account, save it in the repo under **Settings → Secrets and variables → Actions** as `PROFILE_TOKEN`, and tick *Include private contributions on my profile* in your profile's contribution settings.

## 4. Profile settings (github.com/settings/profile)

| Field | Paste this |
|---|---|
| Name | `Sneha Poojary` |
| Bio (160 max) | `Backend & AI engineer. FastAPI · PostgreSQL · Docker. Shipped 3 live services with tests + CI. Open to SDE-1 roles.` |
| Location | `Mumbai, Maharashtra` |
| Website | `https://portfolio-iota-pearl-81.vercel.app/` |
| Social links | LinkedIn, LeetCode (`https://leetcode.com/u/SnehaPoojary__/`), Hashnode, HackerRank |
| Status | Emoji 💼, text `Open to SDE-1 / Backend / AI roles` |

Upload a clear, friendly, front-facing photo (recruiters notice a blank avatar).

## 5. Pin six repositories

Profile → **Customize your pins**. Order matters, strongest first:

1. `Silent-Bug-Predictor`
2. `Explain-My-Code`
3. `NibbleNote`
4. `AI_Engineer_Case_Study`
5. `Portfolio`
6. `SnehaPoojary20` (this repo) is optional, skip it if you prefer five

### Make each pinned repo hire-ready

For every pinned repo, open **About (gear icon)** and fill:

- **Description:** one line, outcome first. Example for Silent Bug Predictor: `FastAPI service that scores Python files for bug risk (AST + commit history → XGBoost). JWT auth, pytest, Docker.`
- **Website:** the live URL
- **Topics:** `fastapi`, `python`, `xgboost`, `postgresql`, `docker`, `github-actions`, `machine-learning` (pick what's true)
- At the top of each repo README: live link, a 10-second GIF or screenshot, and a CI status badge.

**Fix before you apply:** the pinned description of `Explain-My-Code` still says *GPT-3.5*, but your resume says you migrated to Gemini. Update it so repo and resume agree: `AI code explainer: Python AST pre-processing + Gemini API, Pydantic-validated output, AST-only fallback on failure.` Recruiters do cross-check.

Consider renaming `AI_Engineer_Case_Study` to `expert-call-transcript-analyzer` (Settings → Repository name). GitHub redirects the old link. A descriptive name reads better than an assessment label.

## 6. Keep LinkedIn consistent

LinkedIn headline (220 max):
`Backend & AI Engineer | Python, FastAPI, PostgreSQL, Docker | Built and deployed 3 production-style services with CI and tests | Open to SDE-1 roles`

Use the same project wording as this README. One story across GitHub, resume and LinkedIn is more believable than three different ones.

## 7. What recruiters in late 2026 look for (and what this page does about it)

My judgment from how hiring for early-career backend and AI roles generally works, not a statistic:

- **Skim time is seconds.** The page leads with role, status and one visual, then proof. Keep the README to about two screens.
- **Shipped beats listed.** A live URL, tests and CI say more than a wall of skill badges. Every project links to a deployment.
- **AI roles want reliability, not just API calls.** Schema-validated LLM output and graceful fallbacks (already in Explain My Code) are exactly what interviewers probe. Keep that front and centre.
- **Self-hosted stats over third-party widgets.** Public stat-card services rate-limit and break. Yours is generated inside your own repo.
- **Dark and light mode.** The stats card adapts to the viewer's theme.
- **Honest numbers.** Your 332 LeetCode solves and 5 articles are real; keep claims you can defend in an interview.

Highest-value additions when you have time: a small evaluation script for your LLM outputs (accuracy on a handful of test cases), an architecture diagram in each project README, and a few merged pull requests to open-source projects.

## 8. Troubleshooting

- **Action fails with "Permission denied to github-actions":** redo step 3.1.
- **Stats card doesn't change:** GitHub caches images; hard refresh (Ctrl+Shift+R) or wait a few minutes.
- **Contributions tile still `-`:** run the workflow manually and open the run log to see the error.
- **Mermaid diagram not drawing:** it only renders on github.com, not in some previews.
