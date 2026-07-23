from datetime import datetime
from Extension import Extension

def format_requests(responses) -> list[Extension]:
    extensions: list[Extension] = []
    for response in responses.get("responses", []):
        answers = response["answers"]
        assignment = retrieve_value(answers, "00000000")
        deadline = retrieve_value(answers, "00000001")
        reason = retrieve_value(answers, "00000002")
        email = response["respondentEmail"]
        date_submitted = response["lastSubmittedTime"]

        extension = Extension(
            email=email,
            assignment=assignment,
            deadline=datetime.fromisoformat(deadline),
            reason=reason,
            date_submitted=datetime.fromisoformat(date_submitted),
        )
        extensions.append(extension)

    return extensions

def retrieve_value(answers, questionId) -> str:
    return answers[questionId]["textAnswers"]["answers"][0]["value"]