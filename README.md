# Network Analysis API for SNA4Slack

## Count

Return Type: **A number.**

### Member

**Get team member count:**
`/team_account_num/<team_id>`

Example:

http://10.21.55.77:5000/team_account_num/T09NY5SBT

**Get channel member count:**
`/channel_account_num/<team_id>/<channel_id>`

Example:

http://10.21.55.77:5000/channel_account_num/T09NY5SBT/C09NXKJKA

### Message

**Get team message count:**
`/team_message_num/<team_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/team_message_num/T09NY5SBT/1483228800/1514160000

**Get channel message count:**
`/channel_message_num/<team_id>/<channel_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/channel_message_num/T09NY5SBT/C09NXKJKA/1483228800/1514160000

### Mention

**Get team mention count:**
`/team_mention_num/<team_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/team_mention_num/T09NY5SBT/1483228800/1514160000

**Get channel mention count:**
`/channel_mention_num/<team_id>/<channel_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/channel_mention_num/T09NY5SBT/C09NXKJKA/1483228800/1514160000

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

Example:

http://10.21.55.77:5000/sentiment/T09NY5SBT/C09NXKJKA/1483228800/1514160000/10/0

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

Example:

http://10.21.55.77:5000/force_directed/T09NY5SBT/1483228800/1514160000

### Message Frequency Graph

**Get message frequency in one channel:**
`/channel-frequency/<team_id>/<channel_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/channel-frequency/T09NY5SBT/C09NXKJKA/1483228800/1514160000

**Get message frequency in one team:**
`/team-frequency/<team_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/team-frequency/T09NY5SBT/1483228800/1514160000

### User Frequency Graph (Line Chart)

**Get user chat frequency in one channel:**
`/user-frequency/<team_id>/<channel_id>/<user_id>/<from_time>/<to_time>`


### Channel Activity (Bubble chart)

**Get channel activity in one team:**
`/channel-activity/<team_id>/<from_time>/<to_time>`

Example:

http://10.21.55.77:5000/channel-activity/T09NY5SBT/1483228800/1514160000

Note that times are in Unix epoch format with unit `second`.
