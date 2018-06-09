### Dependency
Python Slacker: https://github.com/os/slacker

### Slack Test Token 
URL: https://api.slack.com/docs/oauth-test-tokens

### Requirement
```
# required
success      : BOOL true or false
success_title: STRING title for successful message
title_link   : STRING URL_link
error_msg    : STRING text or empty string

# optional
key1: value1
key2: value2
...

### Run Commands
```shell
# on Jenkins
python slack/slack.py ${SLACK_PYTHON_TOKEN} ${SLACK_CHANNEL} 'json/file/path'
# or
python slack/slack.py ${SLACK_PYTHON_TOKEN} ${SLACK_CHANNEL} 'properties/file/path'

# on terminal
python slack/slack.py xoxp-... '#build' 'json/file/path'
# or
python slack/slack.py xoxp-... '#build' 'properties/file/path'
```

### .json File
```json
{
	"success": true,
	"success_title": "Release successful",
	"title_link": "https://...",
	"error_msg": "",
	"version": "3.151",
	"name": "NAME"
}
```

### .peroperties file
```properties
# required
success=true
success_title=Release successful
title_link=https://...
error_msg=

# optional
version=3.151
name=NAME
```