from app.adapters.repository import GitRepoRepository


class GiveFeedback:
    def __init__(
        self,
        giver_id: int,
        git_repo_id: int,
        message: str,
        repository: GitRepoRepository,
    ) -> None:
        self.giver_id = giver_id
        self.git_repo_id = git_repo_id
        self.message = message
        self.repository = repository

    def execute(self):
        self.repository.add_feedback(
            git_repo_id=self.git_repo_id,
            message=self.message,
            giver_id=self.giver_id,
        )
