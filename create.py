from google.oauth2.credentials import Credentials
from apiclient import discovery

def create_form(form_info: dict[str, str], creds: Credentials):
    service = discovery.build('forms', 'v1', credentials=creds)

    form = {
        "info": {
            "title": form_info["title"],
            "documentTitle": form_info["documentTitle"]
        },
    }

    create_result = service.forms().create(body=form).execute()

    update = {
        "includeFormInResponse": True,
        "requests": [
        # Description
        {
            "updateFormInfo": {
                "info": {
                    "description": form_info["description"]
                },
                "updateMask": "description"
            }
        },
        # Settings
        {
            "updateSettings": {
                "settings": {
                    "emailCollectionType": 2,
                },
                "updateMask": "emailCollectionType"
            }
        },
        # Assignment Question
        {
            "createItem": {
                "item": {
                    "title": "Which assignment are you requesting an extension for?",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "DROP_DOWN",
                                "options": [{"value": assignment} for assignment in form_info["assignments"]]
                            }
                        }
                    }
                },
                "location": { "index": 0 }
            }
        },
        # Deadline Question
        {
            "createItem": {
                "item": {
                    "title": "What is the deadline you are requesting for this extension?",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "dateQuestion": {
                                "includeYear": True
                            }
                        }
                    }
                },
                "location": { "index": 1 }
            }
        },
        # Reason Question
        {
            "createItem": {
                "item": {
                    "title": "What is the reason for the extension?",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {"index": 2}
            }
        }
        ]
    }

    form_result = service.forms().batchUpdate(formId=create_result["formId"], body=update).execute()

    return form_result