# Recipe Review

A multi-agent recipe review assistant built on the Anthropic API. A "head barista" coordinator delegates to two specialist subagents — a **nutritionist** and a **coffee/cooking technique reviewer** — and synthesises their feedback into a single review.

## How it works

`main.py` runs an agentic loop with Claude Haiku 4.5 as the coordinator. The coordinator has two tools available:

- `nutrition_calculator` — analyses calories, macros, vitamins, and overall healthiness (`agents/nutrition.py`)
- `technique_reviewer` — analyses method, steps, timing, temperature, and technique quality (`agents/technique.py`)

Each tool is itself a Claude call with a specialist system prompt. The coordinator decides which to invoke (often both, in parallel), then merges the results.

## Install

Requires Python 3.10+ and an Anthropic API key.

```powershell
cd C:\practice\recipe_review
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

## Run

```powershell
python main.py
```

You'll get an interactive prompt. Type `quit`, `exit`, or `q` to leave.

## Example

```
Recipe Review Assistant — type 'quit' to exit.

Enter your recipe or question: V60 pour-over: 15g coffee, medium grind,
250g water at 95°C. Bloom with 30g for 30s, then pour to 250g in slow
spirals. Total brew time ~3 minutes.

Reviewing...

Here's a combined review of your V60 recipe:

Nutrition: A standard 250g black V60 is essentially calorie-free
(~2 kcal), with trace amounts of magnesium and potassium and roughly
100mg of caffeine. No concerns from a nutritional standpoint.

Technique: Your 1:16.6 ratio and 95°C water are well within the
specialty-coffee sweet spot. The 30g / 30s bloom is appropriate for
15g of coffee. One suggestion: split the main pour into two or three
stages (e.g. up to 150g, pause, then up to 250g) rather than one
continuous spiral — this gives more even extraction. A 3-minute total
brew time is on target for a medium grind.
```

## Project layout

```
recipe_review/
├── main.py              # coordinator + agentic loop
├── agents/
│   ├── nutrition.py     # nutrition_calculator subagent
│   └── technique.py     # technique_reviewer subagent
└── requirements.txt
```
