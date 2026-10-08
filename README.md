<div align="center">

<img src="assets/hero.svg" alt="Sneha Poojary, Backend and AI Engineer" width="100%"/>

<br/>

**Backend & ML systems. Focused on what ships.**
<br/>
Python · FastAPI · Node.js · PostgreSQL · MongoDB · Docker · LLM integration

<br/>

[![Portfolio](https://img.shields.io/badge/Portfolio-visit-7c3aed?style=for-the-badge&logo=vercel&logoColor=white)](https://portfolio-iota-pearl-81.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-connect-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/snehapoojary/)
[![Email](https://img.shields.io/badge/Email-snehapoojary2004-ea4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:snehapoojary2004@gmail.com)
[![Hashnode](https://img.shields.io/badge/Writing-Hashnode-2962ff?style=for-the-badge&logo=hashnode&logoColor=white)](https://hashnode.com/@snehapoojary)

</div>

---

## Open to work

**SDE-1 · Backend Engineer · AI Engineer**

B.E. Computer Engineering · Universal College of Engineering, University of Mumbai · 2022 – 2026

I take a service from schema design to a live URL: async API, auth, tests, CI, container, deploy. Three projects below went all the way through that loop.

---

## By the numbers

<div align="center">
<img src="assets/stats.svg" alt="LeetCode, GitHub and writing stats" width="100%"/>
</div>

---

## What I've shipped

| | Project | What it does | Stack |
|---|---|---|---|
| 1 | **[Silent Bug Predictor](https://github.com/SnehaPoojary20/Silent-Bug-Predictor)** · [live](https://silent-bug-predictor.vercel.app/) | Scores each Python file's bug risk from AST signals (LOC, function count, cyclomatic complexity) plus GitHub commit history, using an XGBoost classifier. | FastAPI, PostgreSQL, XGBoost, JWT, pytest, Docker, Render |
| 2 | **[Explain My Code](https://github.com/SnehaPoojary20/Explain-My-Code)** · [live](https://explain-my-code-two.vercel.app/) | Parses code with Python AST, then asks an LLM for function-level explanations. Falls back to an AST-only summary if the LLM call fails. | FastAPI, React, Gemini API, Pydantic v2, httpx |
| 3 | **[NibbleNote](https://github.com/SnehaPoojary20/NibbleNote)** · [live](https://nibble-note.vercel.app) | Restaurant and café review platform with weighted-relevance search, refresh-token auth and an LLM review summarizer. | MERN, JWT, MongoDB aggregation, Tailwind |
| 4 | **[Expert-call transcript analyzer](https://github.com/SnehaPoojary20/AI_Engineer_Case_Study)** | Answers an interview guide from call transcripts, pulls verbatim quotes with timestamps, finds themes and disagreements across calls. | Python, FastAPI, LLM |

### Decisions I'm proud of

- **Fail soft, not loud.** Explain My Code validates every LLM response against a strict Pydantic v2 schema, and on timeout, rate limit or bad key it still returns the AST-based summary.
- **Persist, don't recompute.** Silent Bug Predictor writes every analysis to PostgreSQL through async SQLAlchemy, so history is queryable instead of vanishing with the response.
- **Pay the write cost once.** NibbleNote stores `avgRating` and `totalReviews` on the restaurant document and recalculates them on each review write, so reads never need a join.
- **Test the ugly inputs.** 8 pytest cases cover syntax errors and nested or async functions, and they run on every push through GitHub Actions.

```mermaid
flowchart LR
    A[Repo URL] --> B[GitHub REST API<br/>commit history]
    A --> C[Python AST<br/>LOC, functions, complexity]
    B --> D[Feature vector]
    C --> D
    D --> E[XGBoost<br/>bug-risk score]
    E --> F[(PostgreSQL<br/>async SQLAlchemy)]
    F --> G[JWT-protected API<br/>rate limited]
```

<sub>Request path of Silent Bug Predictor.</sub>

---

## Stack

![Python](https://img.shields.io/badge/Python-3776ab?style=flat-square&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-ed8b00?style=flat-square&logo=openjdk&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-f7df1e?style=flat-square&logo=javascript&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=flat-square&logo=express&logoColor=white)
![React](https://img.shields.io/badge/React-20232a?style=flat-square&logo=react&logoColor=61dafb)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47a248?style=flat-square&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ed?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088ff?style=flat-square&logo=githubactions&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0a9edc?style=flat-square&logo=pytest&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-fcc624?style=flat-square&logo=linux&logoColor=black)
![XGBoost](https://img.shields.io/badge/XGBoost-337ab7?style=flat-square)
![Gemini API](https://img.shields.io/badge/Gemini_API-8e75b2?style=flat-square&logo=googlegemini&logoColor=white)

---

## Writing

I explain backend and DSA ideas the way I wish someone had explained them to me. Latest posts (refreshed automatically):

<!--POSTS:START-->
- [Two Pointers Explained: The Proof Nobody Shows You](https://dsamadesimple.hashnode.dev/two-pointers-explained-the-proof-nobody-shows-you) · Aug 20, 2026 · 7 min read
- [Sliding Window Algorithm Explained Visually](https://dsamadesimple.hashnode.dev/sliding-window-algorithm) · May 26, 2026 · 4 min read
- [From Confused to Confident in DSA](https://dsamadesimple.hashnode.dev/from-confused-to-confident-in-dsa) · Mar 21, 2026 · 3 min read
- [How Python Manages Memory: Stack vs Heap Explained](https://pythonmemory.hashnode.dev/how-python-manages-memory-stack-vs-heap-explained) · Mar 20, 2026 · 4 min read
- [What Happens When You Run a Python File?](https://snehapoojary.hashnode.dev/what-happens-when-you-run-a-python-file) · Feb 16, 2026 · 2 min read
<!--POSTS:END-->

---

## Find me

[Portfolio](https://portfolio-iota-pearl-81.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/snehapoojary/) · [LeetCode](https://leetcode.com/u/SnehaPoojary__/) · [HackerRank](https://www.hackerrank.com/profile/snehapoojary2004) · [Hashnode](https://hashnode.com/@snehapoojary) · [Email](mailto:snehapoojary2004@gmail.com)

<div align="center"><sub>Stats card and post list are rebuilt daily by a GitHub Action in this repo.</sub></div>
