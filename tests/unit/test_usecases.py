from app.adapters.repository import GitRepositoryMemory
from app.domain.model import User
from app.usecases.give_feedback import GiveFeedback
from app.usecases.import_git_repo import ImportGitRepo
from app.usecases.list_repo_feedbacks import ListRepoFeedbacks
from app.usecases.list_user_repos import ListUserRepos


class TestImportGitRepo:
    def test_user_should_import_git_repo(self):
        git_repo_repository = GitRepositoryMemory()

        user = User(id=1, name="John", email="john@test.com")

        import_git_repo = ImportGitRepo(
            user_id=user.id,
            name="repo-name",
            url="https://www.gitlab.com/test",
            repository=git_repo_repository,
        )

        import_git_repo.execute()

        get_user_git_repositories = ListUserRepos(
            user_id=user.id, repository=git_repo_repository
        )
        user_repos = get_user_git_repositories.execute()

        assert len(user_repos) == 1


class TestGiveFeedBack:
    def test_user_gives_feedback(self):
        git_repo_repository = GitRepositoryMemory()

        user = User(id=1, name="Mary", email="mary@test.com")

        import_git_repo = ImportGitRepo(
            user_id=user.id,
            name="repo-name",
            url="https://www.gitlab.com/test",
            repository=git_repo_repository,
        )

        git_repo_id = import_git_repo.execute()

        giver = User(id=2, name="John", email="john@test.com")

        give_feedback = GiveFeedback(
            giver_id=giver.id,
            git_repo_id=git_repo_id,
            message="awesome repo",
            repository=git_repo_repository,
        )

        give_feedback.execute()

        list_feedbacks = ListRepoFeedbacks(
            git_repo_id=git_repo_id,
            repository=git_repo_repository,
        )
        feedbacks = list_feedbacks.execute()
        assert len(feedbacks) == 1


class TestListRepoFeedbacks:
    def test_list_feedbacks(self):
        git_repo_repository = GitRepositoryMemory()

        list_feedbacks = ListRepoFeedbacks(
            git_repo_id=1,
            repository=git_repo_repository,
        )
        feedbacks = list_feedbacks.execute()

        assert len(feedbacks) == 0
