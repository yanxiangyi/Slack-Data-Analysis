# Network Analysis API for SNA4Slack

## Count

Return Type: **A number.**

### Member

**Get team member count:**
`/team_account_num/<team_id>`

**Get channel member count:**
`/channel_account_num/<team_id>/<channel_id>`

### Message

**Get team message count:**
`/team_message_num/<team_id>/<from_time>/<to_time>`

**Get channel message count:**
`/channel_message_num/<team_id>/<channel_id>/<from_time>/<to_time>`

### Mention

**Get team mention count:**
`/team_mention_num/<team_id>/<from_time>/<to_time>`

**Get channel mention count:**
`/channel_mention_num/<team_id>/<channel_id>/<from_time>/<to_time>`

## Text Sentiment

Return Type: **JSON**

```json
{
  "sentiment":
    {"positive": 0.88156098127365, "negative":0.11843907088041},
  "history":
    [
      {"user": "U1CNBS8F9", "timestamp": 1512481249, "text": "Cool!"},
      {"user": "U83RD1CBE", "timestamp": 1512039064, "text": "cool! thanks!"}
    ]
}
```


**Get channel message sentiment:**
`/sentiment/<team_id>/<channel_id>/<from_time>/<to_time>/<length>/<offset>`

`length` and `offset` are used to limit output.
The default value of `offset` is 0.
If `length` is not specified, no message will be returned.
Both `from` and `to` are optional.
Count of messages are also returned even if `length` and `offset` are missing.

## D3.js

Return Type: **JSON**

### Network visualization (Force-Directed Graph)

**Get team force_directed graph:**
`/force_directed/<team_id>/<from_time>/<to_time>`

### Message Frequency Graph

**Get message frequency in one channel:**
`/channel-frequency/<team_id>/<channel_id>/<from_time>/<to_time>`

**Get message frequency in one team:**
`/team-frequency/<team_id>/<from_time>/<to_time>`

### User Frequency Graph (Line Chart)

**Get user chat frequency in one channel:**
`/user-frequency/<team_id>/<channel_id>/<user_id>/<from_time>/<to_time>`

### Channel Activity (Bubble chart)

**Get channel activity in one team:**
`/channel-activity/<team_id>/<from_time>/<to_time>`

Note that times are in Unix epoch format with unit `second`.
