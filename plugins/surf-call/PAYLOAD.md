# Surf Call payload reference

POST this to your plugin's Webhook URL with `Content-Type: application/json`:

```json
{ "merge_variables": { ... } }
```

The screen is 800×480, so every text field has a **character limit**. Text over the limit is clipped. `tools/validate_payload.py` checks all of these.

| Field | Type | Max | Example | Notes |
|---|---|---|---|---|
| `run` | string | ~24 | `Morning check` | Small label at the top of the verdict box |
| `updated` | string | ~20 | `Tue 5:31 AM` | Bottom-right of the title bar |
| `cat` | enum | | `MIDLENGTH` | `LONGBOARD`, `MIDLENGTH`, `PUSH`, or `NOGO`. NOGO switches to the outlined "no go" layout. |
| `why` | string | 110 | `Clean 2.5-3 ft at 9s ESE with W wind 4-7 mph…` | The reasoning, with real numbers |
| `conf` | string | | `High` | `High` / `Medium` / `Low` |
| `trend` | string | | `Holding` | Buoy trend: `Building` / `Holding` / `Dropping`, or empty |
| `window` | string | 16 | `6:50-10:00 AM` | Best in-water window; empty on NOGO |
| `sunrise` | string | | `7:13a` | |
| `board` | board ID | | `"68"` | Board to load; empty on NOGO |
| `board_why` | string | 34 | `Clean, soft-ish 2.5-3 ft` | One-line reason |
| `alt` | board ID | | `"80"` | Second board when the call is borderline (tagged **OR**) |
| `prog` | boolean | | `true` | Progression board qualifies (tagged **TRY**). Must be a JSON boolean, not `"true"`. |
| `backup` | board ID | | `"68"` | Backup for the progression board (tagged **BACKUP** if it isn't already the LOAD board) |
| `swell` | string | 18 | `2.6 ft 9s ESE` | |
| `wind` | string | 24 | `W 4-7 → SE 11 by 11a` | Include when it turns, if it does |
| `tide` | string | 20 | `Lo 8:05a · Hi 2:20p` | |
| `water` | string | | `61°F` | |
| `suit` | string | 16 | `3/2 full` | `5/4 hood + boots` etc. |
| `hazard` | string | 64 | `Moderate rip current risk` | Shown with ⚠; empty hides the line |
| `next` | string | 60 | `Thu AM: Mid-length, 6'8 (3 ft at 9s)` | Shown in the verdict box on NOGO |
| `spots` | list | 3 | see below | Closest first. Only the first 3 show. |

Each spot:

| Field | Max | Example |
|---|---|---|
| `name` | 22 | `North Jetty` |
| `board` | board ID | `"64"` |
| `surf` | | `2.5-3` (the markup adds "ft") |
| `wind` | | `W 5` |
| `drive` | | `4 min` |

## Board IDs

Board IDs are short strings you define in the markup's quiver block (`q_ids`). The example quiver uses length-based IDs:

| ID | Board | Volume |
|---|---|---|
| `96` | 9'6 longboard | 86 L |
| `80` | 8'0 longboard | 61.7 L |
| `68` | 6'8 mid-length fish | 54.6 L |
| `72` | 7'2 fish | 51.3 L |
| `64` | 6'4 (progression board) | 48 L |

Use your own IDs. Just keep the markup's `q_ids` list, your payloads, and `validate_payload.py --boards` in sync.

## Limits from TRMNL

- **Payload size:** 2 KB (5 KB on TRMNL+). A full payload is about 850 bytes.
- **Rate:** 12 pushes per hour (30 on TRMNL+). Three a day is nothing.
- **Redraws aren't instant.** See *Gotchas* in the main README.
