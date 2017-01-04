"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import boto3

dynamodb = boto3.resource('dynamodb')
client = boto3.client('cloudformation')



def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.echo-sdk-ams.app.a77d1297-2c9f-42e0-88d1-ba75e0720d9f"):
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
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
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
    if intent_name == "Status":
        print("Status")
        return status(intent, session)
    elif intent_name == "Incident":
        print("Incident")
        return incident(intent, session)
    elif intent_name == "Hello":
        print("Hello")
        return hello(intent, session)
    elif intent_name == "Failover":
        print("Failover")
        return failover(intent, session)
    elif intent_name == "Password":
        print("Password")
        return password(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
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

def status(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    speech_output = "Your datacenter status is offline, how should I proceed?"
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

# --------------- Helpers that build all of the responses ----------------------
def incident(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    speech_output = "Your I O T sensors detected fire in the datacenter," \
                    "some services are offline"
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

# --------------- Helpers that build all of the responses ----------------------
def hello(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    speech_output = "Hello, amigos da sea cred, I hope you are enjoying JP's talk so far"
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

# --------------- Helpers that build all of the responses ----------------------
def failover(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    speech_output = "Warning!, you are activating failover mode," \
                    "What's the password?"
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

# --------------- Helpers that build all of the responses ----------------------
def password(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    session_attributes = {}
    print("Entered create_cluster_from_session")
    card_title = intent['name']
    speech_output = "Password confirmed," \
                    "your failover process is being successfully executed," \
                    "Resources are being created," \
                    "Ladies and gentleman," \
                    "that, is how you fail over like an AWS cloud ninja,"
    reprompt_text = ""
    #custom_param = ['KeyName', 'useast1']
    custom_param=[
         {
            'ParameterKey': 'KeyName',
            'ParameterValue': 'useast1'
        }
    ]
    response = client.create_stack(
        StackName='Failover',
        Parameters = custom_param,
        TemplateURL='https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2/EC2InstanceWithSecurityGroupSample.template'
    )
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
