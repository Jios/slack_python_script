#!/usr/bin/python

import sys
from slacker import Slacker
import datetime
import os
import json


########################################################################


def get_field_dict(key, value):
	''' return a dictionary for slack field '''

	d = {'short': True, 'title': key, 'value': value}
	return d

def get_fields_from_dict(field_dict):
	''' unload keys and values from dictionary '''

	fields = []
	for key in sorted(field_dict.iterkeys()):
		field = get_field_dict(key, field_dict[key])
		fields.append(field.copy())

	return fields


########################################################################


def get_slack_attachments(success, success_title, title_link, error_msg):
	''' slack attachments '''

	print "[SLACK] preparing attachments"

	title  	 = '<' + title_link + '|ReferenceError>' + error_msg
	fallback = 'ReferenceError - ' + error_msg + ': ' + title_link
	color	 = 'danger'

	# define success payload for Slack
	if success:
		title 	   = success_title
		fallback   = title + ' ' + title_link
		color 	   = 'good'

	attachments = [{'color': 	  color,
					'fallback':   fallback,
					'title': 	  title,
					'title_link': title_link}]
	return attachments

def send_slack(token, channel, attachments):
	''' send slack message '''

	print "[SLACK] sending slack message"

	slack = Slacker(token)
	slack.chat.post_message(channel, '', username='srvm', attachments=attachments) 
	# '' is text
	# as_user=False sending as a bot_message


########################################################################


def load_json_file(file_path):
	''' 
	load json file to dictionary 
	'''

	print "[SLACK] loading json file"

	field_dict = {}

	with open(file_path) as data_file:
		field_dict = json.load(data_file)

	return field_dict

def load_properties(file_path, sep='=', comment_char='#'):
    '''
    Read the file passed as parameter as a properties file.
    '''
    
    print "[SLACK] loading properties file"

    props_dict = {}
    with open(file_path, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value       = l.split(sep)
                key             = key_value[0].strip()
                value           = sep.join(key_value[1:]).strip('" \t') 
                props_dict[key] = value 
    return props_dict


########################################################################


def parse_argv_list(argvs):
	
	print "[SLACK] parsing argvs"

	token     = argvs[0] 	# string: get oauth test token from https://api.slack.com/docs/oauth-test-tokens
	channel   = argvs[1] 	# string: #build
	file_path = argvs[2]	# json or properties file path

	# convert data file to dictionary
	field_dict = {}
	if file_path.endswith('.json'):
		field_dict = load_json_file(file_path)
	elif file_path.endswith('.properties'):
		field_dict = load_properties(file_path)
	else:
		print '[slack] Error: argument contains unsupported file format.'
		sys.exit(0)

	return (token, channel, field_dict)

def main(argvs):
	"""
	main function
	"""
	(token, channel, field_dict) = parse_argv_list(argvs)

	success       = field_dict.pop('success', None)        # bool: true or false 
	title_link    = field_dict.pop('title_link', None)     # string: URL string
	success_title = field_dict.pop('success_title', None)  # string: URL string
	error_msg     = field_dict.pop('error_msg', None)      # string: error message or empty string, ''

	fields      = get_fields_from_dict(field_dict)
	attachments = get_slack_attachments(success, success_title, title_link, error_msg)

	attachments[0].update({'fields': fields})

	send_slack(token, channel, attachments)

	print "[SLACK] done."


########################################################################


if __name__ == "__main__":
	''' main '''

	if len(sys.argv) != 4:
		print("python slack/slack.py ${SLACK_PYTHON_TOKEN} ${SLACK_CHANNEL} json|properties/file/path")
		sys.exit(0)

	argvs = sys.argv[1:]	# stdin argument value list 

	main(argvs)

