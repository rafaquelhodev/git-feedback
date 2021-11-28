from typing import List
from abc import ABC, abstractmethod

from app.domain.model import Feedback, GitRepo


class GitRepoRepository(ABC):
    @abstractmethod
    def get(self, git_repo_id: int) -> GitRepo:
        pass

    @abstractmethod
    def list_user_repos(self, user_id: int) -> List[GitRepo]:
        pass

    @abstractmethod
    def list_feedbacks(self, git_repo_id: int) -> List[Feedback]:
        pass

    @abstractmethod
    def add_feedback(self, git_repo_id: int, giver_id: int):
        pass

    @abstractmethod
    def import_repo(self, user_id: int, name: str, url: str) -> str:
        pass


class GitRepositoryMemory(GitRepoRepository):
    def __init__(self) -> None:
        self.__git_repos: List[GitRepo] = list()

    def get(self, git_repo_id) -> GitRepo:
        git_repo = next((r for r in self.__git_repos if r.id == git_repo_id), None)

        return git_repo

    def list_feedbacks(self, git_repo_id) -> List[Feedback]:
        git_repo = self.get(git_repo_id)

        if not git_repo:
            return []

        return git_repo.get_feedbacks()

    def add_feedback(self, git_repo_id: int, message: str, giver_id: int):
        feedback = Feedback(message=message, giver_id=giver_id)

        git_repo = self.get(git_repo_id)
        if not git_repo:
            return

        git_repo.receive_feedback(feedback)
        return

    def import_repo(self, user_id: int, name: str, url: str) -> str:
        git_repo = GitRepo(name=name, url=url, user_id=user_id)
        self.__git_repos.append(git_repo)
        return git_repo.id

    def list_user_repos(self, user_id: int) -> List[GitRepo]:
        user_repos = [repo for repo in self.__git_repos if repo.user_id == user_id]
        return user_repos
