import pytest
from app.domain.exceptions import InvalidFeedback
from app.domain.model import Feedback, User, GitRepo


class TestFeedback:
    def test_user_should_import_git_repo(self):
        user = User(name="John", email="john@test.com")
        git_repo = GitRepo(
            name="repo-name", url="https://www.gitlab.com/test", user_id=user.id
        )

        assert len(git_repo.get_feedbacks()) == 0

    def test_user_gives_feedback(self):
        receiver = User(name="John", email="john@test.com")
        git_repo = GitRepo(
            name="repo-name", url="https://www.gitlab.com/test", user_id=receiver.id
        )

        giver = User(name="Marry", email="marry@test.com")
        giver.give_feedback(git_repo, "your repo is great!", True)

        assert len(git_repo.get_feedbacks()) == 1

    def test_same_user_cannot_give_feedback_for_own_repo(self):
        receiver = User(name="John", email="john@test.com")
        git_repo = GitRepo(
            name="repo-name", url="https://www.gitlab.com/test", user_id=receiver.id
        )

        feedback = Feedback("my repo is awesome", receiver.id)

        with pytest.raises(InvalidFeedback) as error:
            git_repo.receive_feedback(feedback)
            assert (
                "Invalid operation: a feedback must be sent by a different user"
                in str(error.value)
            )
