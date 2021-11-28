from app.adapters.repository import GitRepoRepository


class ImportGitRepo:
    def __init__(
        self, user_id: int, name: str, url: str, repository: GitRepoRepository
    ) -> None:
        self.user_id = user_id
        self.name = name
        self.url = url
        self.repository = repository

    def execute(self) -> str:
        repo_id = self.repository.import_repo(self.user_id, self.name, self.url)
        return repo_id
