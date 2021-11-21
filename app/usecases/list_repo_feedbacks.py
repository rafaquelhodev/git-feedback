from app.adapters.repository import GitRepoRepository


class ListRepoFeedbacks:
    def __init__(self, git_repo_id, repository: GitRepoRepository) -> None:
        self.git_repo_id = git_repo_id
        self.repository = repository

    def execute(self):
        feedbacks = self.repository.list_feedbacks(self.git_repo_id)
        return feedbacks
