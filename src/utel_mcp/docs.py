UTEL_API_DOCS: dict[str, str] = {
    "intro": """# UTEL API — Introduction

## Domain & Base URL
Format: `https://api.[subdomain].utel.uz/api/v1`
- Subdomain: `[server-type][number]` (e.g. cc999, utc999)
- Server types: `cc` (Hostmaster VPS), `utc` (Uztelecom VPS)

## Headers (all requests)
```
Accept: application/json
Content-Type: application/json
Authorization: Bearer {token}
```

## Common Errors
| Code | Meaning |
|------|---------|
| 401 | Missing/invalid Bearer token |
| 422 | Validation error — check `errors` object in response |
| 500 | Server or third-party unexpected error |

422 response structure: `{ "message": string, "errors": { field: [string] } }`""",

    "auth": """# Auth

All auth endpoints.

## Login (get token)
`POST /auth/login`
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | email | Yes | User identifier |
| password | string | Yes | Password |

Response returns `result.access_token`. Tokens never auto-expire; use logout to invalidate.

## Me (current user)
`GET /auth/me`

## Change password
`POST /auth/change-password`
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| old_password | string | Yes | Current password |
| password | string | Yes | Min 6 chars |
| password_confirmation | string | Yes | Must match password |

## Logout (invalidate token)
`POST /auth/logout`""",

    "call-history": """# Call History

## List
`GET /call-history`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| per_page | integer | 20 | Records per page (1-300) |
| sort | string | `-id` | Sort field. Prefix `-` for descending. Options: id, date_time, src, dst, external_number, duration, conversation, type, status |
| filter.src | string | — | Caller number |
| filter.dst | string | — | Called number |
| filter.external_number | string | — | External number |
| filter.duration | integer | — | Call duration (seconds) |
| filter.conversation | integer | — | Talk duration (seconds) |
| filter.type | integer | — | 1=incoming, 2=outgoing, 3=internal |
| filter.status | integer | — | 1=answered, 2=not_answered |
| filter.from | datetime | — | Start time (Y-m-d H:i:s) |
| filter.to | datetime | — | End time (Y-m-d H:i:s) |

Example: `/call-history?sort=-id&filter[type]=2`""",

    "statistics": """# Statistics

All endpoints require `from` and `to` (Y-m-d or Y-m-d H:i:s). Optional `external_number` filter.

## Calls count
`GET /statistic/calls-count`
Returns counts by type (incoming/outgoing/internal) and status (answered/not_answered).

## By hour
`GET /statistic/calls-by-hour`
Calls per hour. Response groups: incoming.all, incoming.not_answered, outgoing.all, outgoing.not_answered, internal.all, internal.not_answered. Each entry: `{ date_hour, call_count }`.

## By day
`GET /statistic/calls-by-day`
Same structure as by-hour, grouped by day.

## By month
`GET /statistic/calls-by-month`
Same structure, grouped by month.

## By external number
`GET /statistic/calls-by-external-number`
By trunk external number.

## By users
`GET /statistic/calls-by-users`
Per user stats. Optional `status` filter (1=answered, 2=not_answered).
Returns: number, outgoing_count/duration/conversation, incoming_count/duration/conversation.

## By history filters
`GET /statistic/calls-count-by-history`
Uses same filters as call-history endpoint.""",

    "trunks": """# Trunk (SIP Trunk)

## List
`GET /ats/trunk`

## Create
`POST /ats/trunk`
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| number | string | Yes | Unique trunk number/name |
| title | string | No | Display name |
| server | string | Yes | SIP server address |
| login | string | No | SIP login |
| password | string | No | SIP password (max 80) |
| registrable | boolean | Yes | Whether to register |
| output | integer | No | Inbound call target module |

## Update
`PUT /ats/trunk/{id}`

## Reregister
`POST /ats/trunk/{id}/reregister`
Only works for registrable trunks.

## Delete
`DELETE /ats/trunk/{id}`""",

    "voice-messages": """# Voice Messages (Message Voice)

Voicemail audio messages left by callers.

## List
`GET /message-voice`
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| per_page | integer | 20 | 1-300 |
| sort | string | `-id` | Prefix `-` for descending |
| filter.src | string | — | Caller number |
| filter.dst | string | — | Called number |
| filter.external_number | string | — | External number |
| filter.duration | integer | — | Duration (seconds) |
| filter.status | integer | — | 1=Unread, 2=Read |
| filter.from | datetime | — | Start time |
| filter.to | datetime | — | End time |

## Unread count
`GET /message-voice/unread-count`

## Mark as read
`POST /message-voice/{id}/mark-as-a-read`

## Mark all as read
`POST /message-voice/mark-all-as-read`""",

    "sip-users": """# SIP Users (PsUser)

Extension range: 100-4999

## List
`GET /ats/ps-user`

## List contacts
`GET /ats/ps-user/contacts`

## Create
`POST /ats/ps-user`
| Field | Required | Description |
|-------|----------|-------------|
| title | Yes | Display name |
| number | Yes | Extension (100-4999) |
| password | Yes | Min 6 chars |

## Show
`GET /ats/ps-user/{id}`

## Update
`PUT /ats/ps-user/{id}`

## Delete
`DELETE /ats/ps-user/{id}`

## Update redirect delays
`POST /ats/ps-user/{id}/redirections`
| Field | Description |
|-------|-------------|
| delay1-3 | Delay in seconds (1-3200) |
| redirect1-3 | Target extension or number@external |

## User contact
`GET /ats/ps-user/{id}/contact`""",

    "ivr": """# IVR

Extension range: 5000-5199

## List
`GET /ats/ivr`

## Create
`POST /ats/ivr`
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Extension (5000-5199) |
| allow_input | boolean | Allow DTMF input |
| delay | integer | Delay before play |
| output | integer | Default action target |
| d0-d9 | integer | DTMF key targets |
| aster | integer | * key target |
| sharp | integer | # key target |
| title | string | Display name |

## Update
`PUT /ats/ivr/{id}`

## Upload audio
`POST /ats/ivr/{id}/audio`
multipart/form-data, field `audio`, max 20MB.

## Delete
`DELETE /ats/ivr/{id}`""",

    "groups": """# Group (Ring Group)

Extension range: 5200-5399

## List
`GET /ats/group`

## Create
`POST /ats/group`
| Field | Description |
|-------|-------------|
| id | Extension (5200-5399) |
| users | Comma-separated extensions |
| delay | Ring delay |
| output | Target on no answer |
| title | Display name |

## Update
`PUT /ats/group/{id}`

## Delete
`DELETE /ats/group/{id}`""",

    "queues": """# Queue

Extension range: 5400-5599

## Types
`GET /ats/queue/types`
1=Ring all, 2=Linear, 3=Least recent, 4=Random

## List
`GET /ats/queue`

## Create
`POST /ats/queue`
| Field | Description |
|-------|-------------|
| id | Extension (5400-5599) |
| ring_time | Ring time |
| type | 1-4 (see types) |
| users | Member extensions |
| ring_in_use | Also ring if in use |
| say_position | 1=uz, 2=ru, 3=en, null=off |
| say_when_change | Announce position change |
| say_freq | Position announcement frequency |
| skip_if_offline | Skip offline agents |
| skip_if_in_use | Skip busy agents |
| delay | Delay |
| output | Overflow target |
| title | Display name |

## Update
`PUT /ats/queue/{id}`

## Upload hold music
`POST /ats/queue/{id}/audio` multipart/form-data

## Delete
`DELETE /ats/queue/{id}`""",

    "time-rules": """# Time Rule

Extension range: 5600-5799

## List
`GET /ats/time-rule`

## Create
`POST /ats/time-rule`
| Field | Description |
|-------|-------------|
| id | Extension (5600-5799) |
| days | Array of 7 day definitions |
| exceptions | Array of exception dates |
| working_time | Working hours target |
| not_working_time | After-hours target |
| title | Display name |

Day object: `{ day_number (1=Mon,7=Sun), enabled, start_time (HH:mm), end_time (HH:mm) }`
Exception: `{ from (dd.mm.YYYY), to (dd.mm.YYYY), output }`

## Update
`PUT /ats/time-rule/{id}`

## Delete
`DELETE /ats/time-rule/{id}`""",

    "voicemail": """# Voicemail

Extension range: 5800-5999

## List
`GET /ats/voicemail`

## Create
`POST /ats/voicemail` multipart/form-data
| Field | Description |
|-------|-------------|
| id | Extension (5800-5999) |
| max_duration | Max message length |
| max_silence | Max silence before stop |
| beep | Play beep before recording |
| title | Display name |
| started_audio | Audio file (greeting) |
| finished_audio | Audio file (completion) |

## Update (JSON fields)
`PUT /ats/voicemail/{id}`

## Update audio files
`POST /ats/voicemail/{id}/audios` multipart/form-data

## Delete
`DELETE /ats/voicemail/{id}`""",

    "smart-redirect": """# Smart Redirect

Extension range: 6000-6199

## List
`GET /ats/smart-redirect`

## Create
`POST /ats/smart-redirect`
| Field | Description |
|-------|-------------|
| id | Extension (6000-6199) |
| title | Display name |
| exceptions | Array of exception rules |
| sources | Source integrations config |
| allow_user_redirect | Allow user to override |
| timeout | Timeout before redirect |
| output | Default target |

Source fields: `history.enabled`, `amocrm.enabled` (+ `select_if_multiple_leads_exists`: first_lead/last_lead/contact/default_user), `bitrix.enabled`, `request.enabled` (+ `url`, `timeout` 1-5s).

## Update
`PUT /ats/smart-redirect/{id}`

## Delete
`DELETE /ats/smart-redirect/{id}`""",

    "webhooks": """# Webhook

## List
`GET /integration/webhook`

## Full replace
`PUT /integration/webhook`
Send array of webhook configs:
```json
[{
  "url": "https://...",
  "call_started": true,
  "call_ended": true,
  "dial_started": true,
  "dial_answered": true,
  "dial_ended": true,
  "call_transferred": true,
  "call_saved": true
}]
```
Send `[]` to delete all webhooks.""",

    "extension-ranges": """# Extension Ranges

| Module | Range |
|--------|-------|
| SIP Users | 100-4999 |
| IVR | 5000-5199 |
| Ring Group | 5200-5399 |
| Queue | 5400-5599 |
| Time Rule | 5600-5799 |
| Voicemail | 5800-5999 |
| Smart Redirect | 6000-6199 |""",
}

UTEL_API_REFERENCE = """# UTEL API Reference

## Overview

UTEL is a cloud IP-telephony system. Base URL: `https://api.[subdomain].utel.uz/api/v1`

Subdomain format: `[server-type][number]` (e.g., `cc999` or `utc999`).
- **cc** — Hostmaster datacenter VPS (auto-allocated on registration)
- **utc** — Uztelecom datacenter VPS (customer-provided)

Exceptions: `[organization-name].utel.uz` is also possible.

All endpoints require:
```
Authorization: Bearer {token}
Accept: application/json
Content-Type: application/json
```
Audio uploads use `multipart/form-data`.

## Extension Ranges

| Module | Range |
|--------|-------|
| Users (SIP) | 100-4999 |
| IVR | 5000-5199 |
| Ring Group | 5200-5399 |
| Queue | 5400-5599 |
| Time Rule | 5600-5799 |
| Voicemail | 5800-5999 |
| Smart Redirect | 6000-6199 |

## Auth

Tokens never auto-expire. Logout to invalidate.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/login` | Get `access_token` — body: `{email, password}` |
| GET | `/auth/me` | Current user info — returns `AuthUserResource` |
| POST | `/auth/change-password` | Change password — body: `{old_password, password, password_confirmation}` |
| POST | `/auth/logout` | Invalidate token |

Response format: `{status, code, result: {access_token}, message}`

`/auth/me` result: `AuthUserResource` — `{id, name, email, type: {number, name}, created_at}`. User types: `1=ADMIN`, `2=USER`.

## SIP Users (PsUser)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/ps-user` | List all users |
| POST | `/ats/ps-user` | Create — body: `{title, number (100-4999), password (min 6)}` |
| GET | `/ats/ps-user/{id}` | Show user |
| PUT | `/ats/ps-user/{id}` | Update — same fields as create |
| DELETE | `/ats/ps-user/{id}` | Delete |
| POST | `/ats/ps-user/{id}/redirections` | Update redirect delays — body: `{delay1-3 (1-3200s), redirect1-3}` |
| GET | `/ats/ps-user/contacts` | List all SIP device contacts (`PsContactResource`) |
| GET | `/ats/ps-user/{id}/contact` | User's SIP contact |

Redirect values: extension number (e.g., `101`, `5401`) or `number@external` (e.g., `901234567@781130590`).

`PsUserResource` fields: `id`, `title`, `username`, `password`, `redirections: {delay1-3, redirect1-3}`, `state: string[]`, `reachable`.

`PsContactResource` fields: `id`, `uri` (ip:port), `user_agent`, `expiration_time`, `webrtc` (bool), `transport` (UDP/TCP/TLS/WS/WSS).

## Trunk (SIP Trunk)

Connects UTEL to external phone networks (operator, ATC, PSTN).

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/trunk` | List trunks |
| POST | `/ats/trunk` | Create — body: `{number, title?, server, login?, password? (max 80), registrable (bool), output?}` |
| PUT | `/ats/trunk/{id}` | Update — same fields as create |
| POST | `/ats/trunk/{id}/reregister` | Re-register (registrable-only) |
| DELETE | `/ats/trunk/{id}` | Delete |

After trunk creation, Asterisk PJSIP auto-reloads. `registrable: true` triggers immediate registration.

`TrunkResource` fields: `id`, `number`, `title`, `server`, `login`, `password`, `output`, `status` (Registered/Unregistered), `reachable` (bool), `registrable` (bool), `state: string[]`.

## IVR

Auto-attendant with button mapping (0-9, *, #).

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/ivr` | List IVRs |
| POST | `/ats/ivr` | Create — body: `{id (5000-5199), title?, allow_input (bool), d0-d9?, aster?, sharp?, delay, output?}` |
| PUT | `/ats/ivr/{id}` | Update — same as create; `id` can be changed |
| POST | `/ats/ivr/{id}/audio` | Upload audio — `multipart/form-data`, field `audio`, max 20MB (mp3/wav/ogg) |
| DELETE | `/ats/ivr/{id}` | Delete |

Button fields: `d1`-`d9` (digits 1-9), `d0` (0), `aster` (*), `sharp` (#). Accepts any module number as value.

`allow_input: true` enables multi-digit extension input (1s wait between digits).

`IvrResource` fields: `id`, `title`, `file_url`, `filename`, `allow_input`, `d0`-`d9`, `aster`, `sharp`, `delay`, `output`.

## Group (Ring Group)

Multiple users ring simultaneously under one extension.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/group` | List groups |
| POST | `/ats/group` | Create — body: `{id (5200-5399), title?, users? (comma-separated, max 4095 chars), delay?, output?}` |
| PUT | `/ats/group/{id}` | Update |
| DELETE | `/ats/group/{id}` | Delete |

`users` format: `"101,102,103"` (comma-separated).

`GroupResource` fields: `id`, `title`, `users`, `delay`, `output`.

## Queue

Call queue with hold music, position announcements, and multiple dispatch strategies.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/queue` | List queues |
| GET | `/ats/queue/types` | Queue type list — `[{name, value}]` |
| POST | `/ats/queue` | Create — body: see below |
| PUT | `/ats/queue/{id}` | Update |
| POST | `/ats/queue/{id}/audio` | Upload hold music — `multipart/form-data`, field `audio`, max 20MB |
| DELETE | `/ats/queue/{id}` | Delete |

Queue types: `1=Ring all` (simultaneous), `2=Linear` (sequential), `3=Least recent`, `4=Random`.

Create body fields:
```
id (5400-5599), title?, ring_time, users? (comma-separated), type (1-4),
ring_in_use (bool), say_position? (1=uz, 2=ru, 3=en, null=off),
say_when_change (bool), say_freq (min 10s), skip_if_offline (bool),
skip_if_in_use (bool), delay (min 10s, then -> output), output?
```

`QueueResource` fields: `id`, `title`, `file_url`, `filename`, `ring_time`, `users`, `type`, `ring_in_use`, `say_position`, `say_when_change`, `say_freq`, `skip_if_offline`, `skip_if_in_use`, `delay`, `output`.

## Time Rule

Route calls based on business hours with day schedules and holiday exceptions.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/time-rule` | List time rules |
| POST | `/ats/time-rule` | Create — body: `{id (5600-5799), title?, days: [...], exceptions?, working_time?, not_working_time?}` |
| PUT | `/ats/time-rule/{id}` | Update |
| DELETE | `/ats/time-rule/{id}` | Delete |

`days` — array of exactly 7 elements (day_number 1=Mon → 7=Sun):
```
{days: [{day_number (1-7), enabled (bool), start_time (HH:mm), end_time (HH:mm)}, ...]}
```

`exceptions` — optional array for holidays:
```
{from (dd.mm.YYYY), to (dd.mm.YYYY), output?}
```

`TimeRuleResource` fields: `id`, `title`, `days[{day_number, enabled, start_time, end_time}]`, `exceptions[{from, to, output}]`, `working_time`, `not_working_time`.

## Voicemail

Record messages when users are unavailable.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/voicemail` | List voicemails |
| POST | `/ats/voicemail` | Create — `multipart/form-data`: `{id (5800-5999), title?, max_duration, max_silence, beep, started_audio?, finished_audio?}` |
| PUT | `/ats/voicemail/{id}` | Update (JSON) — fields: `title?, max_duration, max_silence, beep` |
| POST | `/ats/voicemail/{id}/audios` | Update audio files — `multipart/form-data`: `{started_audio?, finished_audio?}` |
| DELETE | `/ats/voicemail/{id}` | Delete |

- `started_audio`: greeting played before recording ("leave a message")
- `finished_audio`: played after recording ("your message was saved")
- `max_duration`: max recording length in seconds (0 = unlimited)
- `max_silence`: silence threshold before auto-stop (0 = no auto-stop)
- `beep`: play beep tone before recording

`VoicemailResource` fields: `id`, `title`, `started_audio`, `started_audio_filename`, `finished_audio`, `finished_audio_filename`, `max_duration`, `max_silence`, `beep`.

## Smart Redirect

Route incoming calls to the agent who last interacted with that caller, using history, CRM, or external lookup.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ats/smart-redirect` | List |
| POST | `/ats/smart-redirect` | Create — body: `{id (6000-6199), title, exceptions?, sources: {...}, allow_user_redirect, timeout?, output?}` |
| PUT | `/ats/smart-redirect/{id}` | Update |
| DELETE | `/ats/smart-redirect/{id}` | Delete |

`sources` object:
```json
{
  "history": {"enabled": bool},
  "amocrm": {"enabled": bool, "select_if_multiple_leads_exists?": "first_lead"|"last_lead"|"contact"|"default_user"},
  "bitrix": {"enabled": bool},
  "request": {"enabled": bool, "url"?: "...\", "timeout"?: 1-5}
}
```

External request: UTEL sends GET to `url`, expects JSON `{"extension": "101"}` or plain text `101` response.

`exceptions`: comma-separated caller prefixes to exclude (e.g., `"99890,99891"`).

`SmartRedirectResource` fields: `id`, `title`, `exceptions`, `sources{history, amocrm, bitrix, request}`, `allow_user_redirect`, `timeout`, `output`.

## Webhook

Real-time call event notifications via HTTP POST. List/create/replace via `/integration/webhook`.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/integration/webhook` | List webhooks |
| PUT | `/integration/webhook` | Full replace — send array of webhook objects. Send `[]` to delete all |

Events: `call_started`, `call_ended`, `dial_started`, `dial_answered`, `dial_ended`, `call_transferred`, `call_saved`.

Each webhook object: `{url, call_started, call_ended, dial_started, dial_answered, dial_ended, call_transferred, call_saved}` (all bool).

Payload format: `POST` with `Content-Type: application/json`, `User-Agent: UtelHttpAgent/1.0`.
```json
{"time": "HH:mm:ss", "data": {"name": "...", "domain": "...", "call": {...}, "channel": {...}}}
```
- `call_started` fields: `name`, `domain`, `call`, `channel`
- `dial_started`/`dial_answered`/`dial_ended` fields: `name`, `domain`, `call`, `callerChannel`, `destChannel`
- `call_blind_transferred` fields: `name`, `domain`, `call`, `channel`, `transferee`, `to`
- `call_attended_transferred` fields: `name`, `domain`, `call_first`, `call_second`, `channel`, `transferee`, `second_channel`, `target`
- `call_ended` fields: `name`, `domain`, `call` (with full CDR)
- `call_saved` fields: `name`, `domain`, `call_history` (full `CallHistoryIndexResource`)

Event order for inbound call: `call_started → dial_started → dial_answered → dial_ended → call_ended → call_saved`

Server must return `2xx` within 10 seconds. HTTPS recommended.

## Call History

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/call-history` | List (paginated, filterable, sortable) |

Query params: `per_page` (1-300, default 20), `sort` (prefix `-` for desc).

Sort fields: `id`, `date_time`, `src`, `dst`, `external_number`, `duration`, `conversation`, `type`, `status`.

Filter params (nested under `filter[...]`):
- `src`, `dst`, `external_number` (string)
- `duration`, `conversation` (integer, seconds)
- `type`: 1=incoming, 2=outgoing, 3=internal
- `status`: 1=answered, 2=not_answered
- `from`, `to` (datetime, `Y-m-d H:i:s`)

`CallHistoryIndexResource` fields: `id`, `call_id` (UUID), `date_time`, `src`, `dst`, `external_number|null`, `duration`, `conversation`, `type{number, name}`, `status{number, name}`, `recorded_file_url|null`, `integration[]|null`.

## Statistics

All require `from` and `to` (`Y-m-d` or `Y-m-d H:i:s`). Optional `external_number` filter.

| Endpoint | Returns |
|----------|---------|
| `GET /statistic/calls-count` | Call counts by type (incoming/outgoing/internal) and status (answered/not_answered) |
| `GET /statistic/calls-by-hour` | Calls per hour — `[{date_hour, call_count}]` per type/status |
| `GET /statistic/calls-by-day` | Calls per day — same structure as by-hour |
| `GET /statistic/calls-by-month` | Calls per month — grouped by month |
| `GET /statistic/calls-by-external-number` | By external number |
| `GET /statistic/calls-by-users` | Per user — `{number, outgoing_count, outgoing_duration, outgoing_conversation, incoming_count, incoming_duration, incoming_conversation}`. Optional `status` filter (1=Answered, 2=Not answered) |
| `GET /statistic/calls-count-by-history` | Filtered stats using call-history filters |

## Voice Messages

Voicemail recordings left by callers.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/message-voice` | List messages (same filter/sort as call-history) |
| GET | `/message-voice/unread-count` | Unread count — returns `{unread_count: int}` |
| POST | `/message-voice/{id}/mark-as-a-read` | Mark single as read |
| POST | `/message-voice/mark-all-as-read` | Mark all as read |

Message status: 1=Unread, 2=Read.

`MessageVoiceResource` fields: `id`, `date_time`, `src`, `dst`, `external_number|null`, `duration`, `status{number, name}`, `recorded_file_url|null`.

## Socket (WebRTC)

WebSocket URL: `wss://[subdomain].utel.uz:8089`

Use JSSIP or SIP.js libraries. One device per SIP user at a time — socket connection auto-configures for WebSocket, so softphone credentials on same user will conflict.

## Common Errors

| Code | Meaning |
|------|---------|
| 401 | Missing/invalid Bearer token |
| 422 | Validation error — `{message: string, errors: {field: [string]}}` |
| 500 | Server/third-party unexpected error |
"""
