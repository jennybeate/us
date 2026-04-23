# Us — Results screen redesign

Two files, drop-in replacements for the originals:

- `styles.py` — global styles + small component helpers (`meta`, `badge`, `score_bar`, `action_list`, `insight_card`, `divider`)
- `results.py` — the rewritten Results view

## How to apply

From your repo root:

```bash
cp us-app-redesign/styles.py   us-app/styles.py
cp us-app-redesign/results.py  us-app/results.py
streamlit run us-app/app.py
```

Then walk through the flow and look at the Results screen.

## Back-compat

`styles.py` keeps every public name the other views depend on:
`COLORS` (with all old keys — `rose`, `gold`, `sage`, `amber`, `green`, `partner1`, `partner2`, `muted`, `divider`), `inject`, `divider`, `badge`, `action_bullet`, `insight_card`, `card_open`, `card_close`. New helpers (`meta`, `score_bar`, `action_list`) are additive.

The old class names (`us-card`, `us-pillar-card`, `us-pillar-card-attention`, `us-pillar-card-good`, `us-insight-card`) still exist — they're restyled to the new hairline look, so views that use them (e.g. `checkin.py`, `pillar_definition.py`) will pick up the new aesthetic automatically, without breaking.

## What changed visually

| | Before | After |
|---|---|---|
| Accent | Rose + gold gradient | Single clay (`#B4704D`) |
| Partner 2 | Sage | Muted evergreen + dashed radar line |
| Display font | Playfair italic | Fraunces, upright, medium weight |
| Meta labels | None / sentence case | JetBrains Mono tiny-caps |
| Cards | Drop-shadowed rounded boxes | Hairline-topped rows |
| CTAs | Rose→gold gradient pill | Solid ink rectangle + ghost |
| Insights | Gradient panel + 💡 emoji | Hairline panel, Fraunces display |
| Radar | Filled rose + sage | Hairline grid, small polygons, dashed line on partner 2 |
| Actions | Bulleted (✦) Inter | Numbered (01, 02…) Fraunces serif |

## Caveats

1. **Action copy is still template-based.** `analysis.get_actions` still pulls from `config.ACTION_TEMPLATE_SETS`. To make the "in your own words" label fully honest, update `pillar_definition.py` to collect 5 concrete examples per pillar and have `get_actions` return those instead of templates. Happy to do that pass next.

2. **Plotly radar.** It's still Plotly under the hood — styled to blend in, but if it ever feels like a foreign object, a pure-SVG radar (like the mockup) is a ~30-line swap.

3. **No changes to other views.** Welcome, context questions, questionnaire, pillar definition, waiting, and check-in all inherit the new fonts / buttons / inputs from the shared CSS, but their copy and layout are untouched.
