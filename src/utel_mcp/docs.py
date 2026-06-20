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
| per_page | integer | 20 | Records per page (1–300) |
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
| per_page | integer | 20 | 1–300 |
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

Extension range: 100–4999

## List
`GET /ats/ps-user`

## List contacts
`GET /ats/ps-user/contacts`

## Create
`POST /ats/ps-user`
| Field | Required | Description |
|-------|----------|-------------|
| title | Yes | Display name |
| number | Yes | Extension (100–4999) |
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
| delay1–3 | Delay in seconds (1–3200) |
| redirect1–3 | Target extension or number@external |

## User contact
`GET /ats/ps-user/{id}/contact`""",

    "ivr": """# IVR

Extension range: 5000–5199

## List
`GET /ats/ivr`

## Create
`POST /ats/ivr`
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Extension (5000–5199) |
| allow_input | boolean | Allow DTMF input |
| delay | integer | Delay before play |
| output | integer | Default action target |
| d0–d9 | integer | DTMF key targets |
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

Extension range: 5200–5399

## List
`GET /ats/group`

## Create
`POST /ats/group`
| Field | Description |
|-------|-------------|
| id | Extension (5200–5399) |
| users | Comma-separated extensions |
| delay | Ring delay |
| output | Target on no answer |
| title | Display name |

## Update
`PUT /ats/group/{id}`

## Delete
`DELETE /ats/group/{id}`""",

    "queues": """# Queue

Extension range: 5400–5599

## Types
`GET /ats/queue/types`
1=Ring all, 2=Linear, 3=Least recent, 4=Random

## List
`GET /ats/queue`

## Create
`POST /ats/queue`
| Field | Description |
|-------|-------------|
| id | Extension (5400–5599) |
| ring_time | Ring time |
| type | 1–4 (see types) |
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

Extension range: 5600–5799

## List
`GET /ats/time-rule`

## Create
`POST /ats/time-rule`
| Field | Description |
|-------|-------------|
| id | Extension (5600–5799) |
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

Extension range: 5800–5999

## List
`GET /ats/voicemail`

## Create
`POST /ats/voicemail` multipart/form-data
| Field | Description |
|-------|-------------|
| id | Extension (5800–5999) |
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

Extension range: 6000–6199

## List
`GET /ats/smart-redirect`

## Create
`POST /ats/smart-redirect`
| Field | Description |
|-------|-------------|
| id | Extension (6000–6199) |
| title | Display name |
| exceptions | Array of exception rules |
| sources | Source integrations config |
| allow_user_redirect | Allow user to override |
| timeout | Timeout before redirect |
| output | Default target |

Source fields: `history.enabled`, `amocrm.enabled` (+ `select_if_multiple_leads_exists`: first_lead/last_lead/contact/default_user), `bitrix.enabled`, `request.enabled` (+ `url`, `timeout` 1–5s).

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
| SIP Users | 100–4999 |
| IVR | 5000–5199 |
| Ring Group | 5200–5399 |
| Queue | 5400–5599 |
| Time Rule | 5600–5799 |
| Voicemail | 5800–5999 |
| Smart Redirect | 6000–6199 |""",
}
