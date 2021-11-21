from __future__ import annotations
from uuid import uuid4

from app.domain.exceptions import InvalidFeedback


class User:
    def __init__(self, name: str, email: str, id: str = None) -> None:
        self.name = name
        self.email = email
        self.id = uuid4() if not id else id

    def give_feedback(self, git_repo: GitRepo, message: str, private: bool):
        feedback = Feedback(message=message, giver_id=self.id, private=private)
        git_repo.receive_feedback(feedback)


class GitRepo:
    def __init__(self, name: str, url: str, user_id: str, id: str = None) -> None:
        self.id = uuid4() if not id else id
        self.name = name
        self.url = url
        self.user_id = user_id
        self._feedbacks = list()

    def receive_feedback(self, feedback: Feedback):
        if feedback.giver_id == self.user_id:
            raise InvalidFeedback(
                "Invalid operation: a feedback must be sent by a different user"
            )

        self._feedbacks.append(feedback)

    def get_feedbacks(self):
        return self._feedbacks


class Feedback:
    def __init__(self, message: str, giver_id: str, private: bool = False) -> None:
        self.message = message
        self.private = private
        self.giver_id = giver_id
