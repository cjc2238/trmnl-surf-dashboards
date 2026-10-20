# TRMNL push step (append to the surf check prompt)

Add this as the final step. Replace `{{RUN_LABEL}}` with `Morning check`, `Midday check` or `Nightly outlook`, and replace the board IDs with the ones from your markup's `q_ids`.

**Don't commit your real Webhook URL.** Paste it into your agent's prompt (or an environment variable) only.

```text
6. After sending the message, push a compact version of the same call to my TRMNL e-ink display.
   Write a Python script that builds this JSON with json.dump (so quotes and apostrophes like 9'6 are escaped correctly) and saves it to trmnl.json. Keep the whole payload under 2 KB and stay within every character limit — the screen is small and longer text gets cut off.

   Board IDs (use these exact strings in every board field): "96" = 9'6 longboard, "80" = 8'0 longboard, "68" = 6'8 mid-length fish, "72" = 7'2 fish, "64" = 6'4 progression board.

   {"merge_variables": {
     "run": "{{RUN_LABEL}}",
     "updated": "<weekday + time this ran, e.g. Tue 5:31 AM>",
     "cat": "<exactly one of LONGBOARD, MIDLENGTH, PUSH, NOGO: the best category in the message>",
     "why": "<the Why line condensed, max 110 chars>",
     "conf": "<High, Medium or Low>",
     "trend": "<buoy trend: Building, Holding or Dropping; empty if not checked>",
     "window": "<best in-water window, max 16 chars, e.g. 6:50-10:00 AM; empty if NOGO>",
     "sunrise": "<e.g. 7:13a>",
     "board": "<board ID to load; empty if NOGO>",
     "board_why": "<one-line reason for that board, max 34 chars>",
     "alt": "<board ID of the second board if the call is borderline between two; otherwise empty>",
     "prog": <true if the progression pick qualifies, else false — a JSON boolean, not a string>,
     "backup": "<board ID of the backup board when prog is true; otherwise empty>",
     "swell": "<primary swell, max 18 chars, e.g. 2.6 ft 9s ESE>",
     "wind": "<wind and how it changes, max 24 chars, e.g. W 4-7 → SE 11 by 11a>",
     "tide": "<next two tides, max 20 chars, e.g. Lo 8:05a · Hi 2:20p>",
     "water": "<water temp, e.g. 61°F>",
     "suit": "<wetsuit, max 16 chars, e.g. 3/2 full or 5/4 hood + boots>",
     "hazard": "<most important hazard, max 64 chars; empty if none>",
     "next": "<if NOGO: next qualifying day/time with category and board, max 60 chars; otherwise empty>",
     "spots": [ up to 3 qualifying spots, closest first; [] if none:
       {"name": "<max 22 chars>", "board": "<board ID best for that spot>", "surf": "<ft range, e.g. 1.5-2>", "wind": "<e.g. WNW 5>", "drive": "<e.g. 4 min>"} ]
   }}

   Then send it with:
   curl -sS -X POST -H "Content-Type: application/json" --data @trmnl.json "{{YOUR_TRMNL_WEBHOOK_URL}}"
   If the push fails (network blocked, rate limited, any error), note it in one short line and move on. Never retry more than once, and never let it hold up or change the message above.
```

## Why it's written this way

- **`json.dump` instead of hand-written JSON:** board sizes like `9'6` and `8'0"` are full of quotes, and models writing JSON by hand break on them.
- **Hard character limits:** the model will happily write a 300-character "why". The screen fits about 110.
- **Board IDs instead of names:** "8'0 Walden Magic Model" won't fit in a 160 px tile, so IDs keep the payload small and the markup in control of the display names.
- **"Never let it hold up the message":** the phone message is the primary output, and the screen is a bonus.
