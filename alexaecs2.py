from __future__ import print_function

import boto3

client = boto3.client('ecs')

cluster = "alexademo"
service = "mySite"


def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.ce6959f5-5da9-4b59-9376-41f73d84251d"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("INTENT_NAME: " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "Upgrade":
        print("Upgrade")
        return upgrade(intent, session)
    elif intent_name == "Downgrade":
        print("Downgrade")
        return downgrade(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------

def upgrade(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    try:
        taskDefinition = "ngnix-jp:2"
        response = client.update_service(
            cluster=cluster,
            service=service,
            taskDefinition=taskDefinition
        )
    except Exception, e:
        speech_output = str(e)
        reprompt_text = ""
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, False))

    speech_output = "Task definition sucessfully updated to %s." % taskDefinition.replace(":", " version ")
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

def downgrade(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    try:
        taskDefinition = "ngnix-jp:1"
        response = client.update_service(
            cluster=cluster,
            service=service,
            taskDefinition=taskDefinition
        )
    except Exception, e:
        speech_output = str(e)
        reprompt_text = ""
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, False))

    speech_output = "Task definition sucessfully updated to %s." % taskDefinition.replace(":", " version ")
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
