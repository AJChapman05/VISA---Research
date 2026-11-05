# Lab 19 — Legend Investor Panel

This is the standalone Lab 19 project. It contains the full five-year SEC 10-K
screen, Buffett, Cathie Wood, and Michael Burry panels, three saved memos, skills,
and offline tests.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python run_analysis.py V
streamlit run app.py
```

