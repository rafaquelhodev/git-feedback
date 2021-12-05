from app.domain import model


def test_can_insert_user(session):
    session.add(model.User(name="Mary", email="mary@test.com", password="123"))
    session.commit()

    [user] = session.execute(
        "SELECT * FROM users WHERE id=:id",
        dict(id=1),
    )

    assert user.name == "Mary"
    assert user.email == "mary@test.com"
    assert user.password == "123"


def test_can_query_user(session):
    session.execute(
        "INSERT INTO users (name, email, password) VALUES "
        '("Mary", "mary@test.com", "123")'
    )

    session.add(model.User(name="Mary", email="mary@test.com", password="123"))
    session.commit()

    user = session.query(model.User).all()[0]

    assert user.name == "Mary"
    assert user.email == "mary@test.com"
    assert user.password == "123"


def test_can_insert_git_repo(session):
    session.add(model.GitRepo(name="api-foo", url="github.com/api-foo", user_id=1))
    session.commit()

    [git_repo] = session.execute(
        "SELECT * FROM git_repos WHERE id=:id",
        dict(id=1),
    )

    assert git_repo.name == "api-foo"
    assert git_repo.url == "github.com/api-foo"
    assert git_repo.user_id == 1


def test_query_git_feedbacks(session):
    session.execute(
        "INSERT INTO git_repos (name, url, user_id) VALUES "
        '("api-foo", "github.com/api-foo", 1)'
    )
    session.execute(
        "INSERT INTO feedbacks (message, giver_id, git_repo_id, private) VALUES "
        '("cool repo", 2, 1, False)'
    )

    git_repo = session.query(model.GitRepo).all()[0]

    feebacks = git_repo.get_feedbacks()
    assert len(feebacks) == 1
    assert feebacks[0].message == "cool repo"
    assert feebacks[0].private == False


def test_insert_git_feedbacks(session):
    session.execute(
        "INSERT INTO git_repos (name, url, user_id) VALUES "
        '("api-foo", "github.com/api-foo", 1)'
    )

    feedback = model.Feedback(message="cool repo :)", giver_id=2)
    git_repo = session.query(model.GitRepo).all()[0]
    git_repo.receive_feedback(feedback)
    session.commit()

    [res_feedback] = session.execute("SELECT * FROM feedbacks")

    assert res_feedback.message == "cool repo :)"
    assert res_feedback.private == False


def test_can_query_git_repo(session):
    session.execute(
        "INSERT INTO git_repos (name, url, user_id) VALUES "
        '("api-foo", "github.com/api-foo", 10),'
        '("api-bar", "gitlab.com/api-bar", 20),'
        '("api-foo-bar", "github.com/api-foo-bar", 30)'
    )

    git_repos = session.query(model.GitRepo).all()

    assert len(git_repos) == 3
