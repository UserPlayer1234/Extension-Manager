from google.oauth2.credentials import Credentials
from googleapiclient import discovery

class Form:
    def __init__(self, creds: Credentials):
        self.service = discovery.build('forms', 'v1', credentials=creds)


    def create_form(self, form_info: dict[str, str]):
        form = {
            "info": {
                "title": form_info["title"],
                "documentTitle": form_info["documentTitle"]
            },
        }

        create_result = self.service.forms().create(body=form).execute()
        self.formId = create_result["formId"]

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
                                "questionId": "00000000",
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
                                "questionId": "00000001",
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
                                "questionId": "00000002",
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

        form_result = self.service.forms().batchUpdate(formId=create_result["formId"], body=update).execute()
        
        return form_result

    def retrieve_form(self):
        responses = self.service.forms().responses().list(formId=self.formId).execute()
        return responses