# Surf check prompt (template)

This is the prompt behind the Surf Call screen. Paste it into any AI agent that can **search the web, run code, and run on a schedule**. I run it as three Claude scheduled tasks: a morning check, a midday check, and a nightly outlook. Each run sends a phone-friendly message, then pushes the summary to TRMNL.

**Fill in everything in `{{CURLY_BRACES}}`.** Then pick one of the three *Run type* blocks below, and append [`trmnl-push-step.md`](trmnl-push-step.md) to the end.

> **Network note for hosted agents:** the agent's sandbox has to be allowed to reach `trmnl.com` or the push will fail. In Claude that's **Settings → Capabilities → allowed domains**. Other platforms have a similar allowlist.

---

## Suggested schedule

| Run | When (local) | Forecast window |
|---|---|---|
| Morning check | ~5:30 AM | Sunrise to ~1 PM today |
| Midday check | ~12:00 PM | Now to sunset |
| Nightly outlook | ~11:00 PM | Tomorrow, first light to ~1 PM |

Avoid scheduling exactly on the hour: shared schedulers get busy at :00.

---

## Run type (pick one)

**Morning:**
> You are running my MORNING surf check. Today's forecast window is sunrise through about 1 PM ({{TIMEZONE}}).

**Midday:**
> You are running my MIDDAY surf check. Today's forecast window is now through sunset ({{TIMEZONE}}). Focus on afternoon and evening sessions, watch for the afternoon sea breeze, and check live buoy and observed conditions, not just the forecast.

**Nightly:**
> You are running my NIGHTLY surf outlook. It runs around 11 PM ({{TIMEZONE}}). Forecast TOMORROW MORNING (the next calendar day, from first light through about 1 PM) so I can decide tonight whether to set an alarm and which board to load in the car. Also look at tonight's buoy trend (building, holding, or dropping) to judge whether the forecast is likely to hold.

---

## The prompt

```text
{{RUN_TYPE_BLOCK_FROM_ABOVE}}

About me: {{SKILL_LEVEL, e.g. beginner-intermediate}} surfer, about {{WEIGHT_LB}} lb ({{WEIGHT_KG}} kg), based near {{HOME_AREA — a town or cross streets is enough}}. I don't want to miss any chance to be in the water when conditions are favorable.

My quiver (more volume = easier paddling and wave-catching; liters per kg of my body weight in brackets):
- {{BOARD_1, e.g. 9'6 longboard — 9'6" x 23" x 3 1/8", 86 L [1.15 L/kg]. The cruiser for the smallest, weakest, mushiest days.}}
- {{BOARD_2, e.g. 8'0 longboard — 61.7 L [0.82 L/kg]. Small days with a bit more push; my "safe" pick on borderline, bumpy, or crowded days.}}
- {{BOARD_3, e.g. 6'8 mid-length fish — 54.6 L [0.73 L/kg]. Paddles easiest of my shorter boards; best on clean, softer days.}}
- {{BOARD_4, e.g. 7'2 fish — 51.3 L [0.68 L/kg]. More length and rail; steadier on steeper, faster, or bigger waves.}}
- {{BOARD_5, e.g. 6'4 — 48 L [0.64 L/kg]. My progression board; floats me but paddles slower, so it needs waves with some push.}}

Cold-water rule: when the water calls for a 5/4 or thicker wetsuit with boots, gloves, or a hood (roughly under 50°F water), the extra rubber weighs me down and tires my paddle. When choosing between two boards, lean toward the higher-volume one, and only suggest the progression board at the top of its range.

1. Find the current surf forecast for every surf spot within about a {{MAX_DRIVE_MINUTES}}-minute drive of {{HOME_AREA}}. Likely candidates include {{LIST_OF_LOCAL_BREAKS}} — confirm drive times and add or drop spots as appropriate. Use web search on sources like Surfline, surf-forecast.com, {{REGIONAL_SOURCES}}, NOAA/NDBC buoys {{BUOY_IDS}}, and the NWS marine forecast for {{COASTAL_ZONE}}. Cross-check at least two sources.
2. For each spot, gather for the forecast window: wave/surf height, primary swell (height, period, direction), wind speed and direction hour by hour (look for a glassy or offshore window before the wind turns), sunrise time, tide times, water temp, and any hazards (rip current statement, small craft advisory).
3. Favorable wind (required for every category): offshore (roughly {{OFFSHORE_DIRECTIONS, e.g. W, WNW, NW for east-facing beaches}}) or light (under ~8–10 mph) from any direction. Strong onshore ({{ONSHORE_DIRECTIONS, e.g. E/SE/NE}} over ~10 mph) is not favorable. Note if a jetty or inlet gives a spot shelter from a given wind.
4. Classify each spot into one category and pick a board:
   - LONGBOARD DAY: about 1–2.5 ft, rideable (not flat or closing out on the sand), favorable wind, period roughly 6s+. Board: {{BIGGEST_BOARD}} for 1–1.5 ft, weak/mushy waves, or a high tide that fattens the waves; {{SECOND_BOARD}} for 1.5–2.5 ft with a bit more push or a little bump.
   - MID-LENGTH DAY: about 2.5–4 ft with favorable wind, period 7s+. Board: {{SOFT_DAY_MIDLENGTH}} for 2.5–3.5 ft clean, softer waves; {{STEEP_DAY_MIDLENGTH}} for 3–4 ft, or steeper, faster, bumpier waves, or a longer paddle-out. In the 2–3 ft crossover, choose between {{SECOND_BOARD}} (soft, fat, or slightly bumpy waves) and {{SOFT_DAY_MIDLENGTH}} (clean with some push), and say why.
   - PROGRESSION PICK (optional add-on, not its own category): suggest {{PROGRESSION_BOARD}} only on clean, well-shaped, punchy 2.5–3.5 ft waves with offshore or glassy wind, a period of 8s+, and no strong rip current (and apply the cold-water rule). Never on mushy, weak, choppy, or 4 ft+ days. When you suggest it, name a backup board to bring in case it's a struggle.
   - PUSH DAY (4–5 ft): ONLY when it's truly a "can't miss" day — clean, well-groomed waves, offshore or glassy wind (offshore under ~12 mph or under ~5 mph any direction), long-ish period (about 9s+), no small craft advisory, and the wave shape at that spot is forgiving (peeling or shouldering, not dumping or closing out). Board: {{PUSH_DAY_BOARD}} only. Pick the spot(s) with the most forgiving shape, and include a short safety note (rip risk, crowds, paddle-out channel, sets). If 4–5 ft but any of these isn't met, it is NOT a push day.
   - NO GO: anything else — flat/under ~1 ft, unfavorable wind, over 5 ft, or 4–5 ft without can't-miss conditions.
5. Estimate the driving distance and time from {{HOME_AREA}} to each spot that is not NO GO.

Then send me ONE message:
- Headline with the best category available: "🏄 Go surf — Longboard day", "🏄 Go surf — Mid-length day", "⚡ Push day — 4–5 ft, can't miss", or "No go". If different spots fall in different categories, say so.
- Immediately below the headline, a "Why:" line of 1–2 sentences explaining why that category was chosen — name the actual numbers against the criteria above. Add a confidence note (high / medium / low) based on how well the sources agree.
- If any spots qualify: a "Board:" line naming the board to bring and a one-line reason; if borderline between two boards, name both. If the progression board qualifies, add a "Progression pick" line with its reason and backup board. Then the best time window (nightly: an "Alarm" line with when to be in the water and when the window likely closes, plus sunrise). Then each qualifying spot, closest first: spot name, category, best board for that spot, parking/beach access, a Google Maps link (https://www.google.com/maps/search/?api=1&query=...), drive time, wave height, swell, wind, tide, water temp and suggested wetsuit, and any hazards.
- If no spots qualify: after the Why line, keep it to 2–3 more lines — general size and wind, and the next day/time in the forecast that looks like it will qualify (with its category and board), if any.

Keep it phone-friendly and scannable. End with a short Sources list of the forecast pages used.
```

## Tuning tips

- **The categories are the product.** Change the size, period and wind thresholds to match your level and your breaks. The screen only cares about the four category names.
- **Make it cite numbers.** Requiring the "Why" line to quote the actual numbers against the criteria is what keeps the call honest and easy to sanity-check.
- **Two sources minimum.** Single-source forecasts swing a lot, especially on short-period windswell.
- **Keep the safety rules strict.** The "PUSH DAY only when *every* box is ticked" rule exists so the agent never talks a newer surfer into overhead closeouts.
