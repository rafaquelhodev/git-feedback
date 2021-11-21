from app.adapters.repository import GitRepoRepository


class ListUserRepos:
    def __init__(self, user_id: str, repository: GitRepoRepository) -> None:
        self.user_id = user_id
        self.repository = repository

    def execute(self):
        feedbacks = self.repository.list_user_repos(self.user_id)
        return feedbacks
