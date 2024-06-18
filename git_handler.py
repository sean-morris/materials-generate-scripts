from git import Repo, GitCommandError
import os
from github import Github
from github.GithubException import GithubException
import json
import traceback


def get_tokens(file_name):
    access_tokens = {}
    f = open(file_name)
    data = json.load(f)

    for org, token in data.items():
        access_tokens[org] = token

    f.close()
    return access_tokens


def tag_exists(repo, tag_name):
    """Check if a tag already exists in the repository."""
    return tag_name in [tag.name for tag in repo.tags]


def remove_tag(repo, tag_name):
    """Remove a tag if it exists locally and remotely."""
    try:
        tag_ref = repo.tags[tag_name]
        repo.delete_tag(tag_ref)
        print(f"Tag '{tag_name}' removed locally.")

        # Remove the tag from the remote repository
        origin = repo.remote(name='origin')
        origin.push(refspec=f":refs/tags/{tag_name}")

        origin = repo.remote(name='upstream')
        origin.push(refspec=f":refs/tags/{tag_name}")

        print(f"Tag '{tag_name}' removed from remote.")
        print(f"Tag '{tag_name}' removed from remote.")
    except GitCommandError as e:
        print(f"Error removing tag '{tag_name}': {e}")


def create_tag(repo, tag_name, tag_message):
    # Check if the repository is dirty (has uncommitted changes)
    if repo.is_dirty():
        print("The repository has uncommitted changes. Commit or stash them before tagging.")
        return

    # Get the latest commit (HEAD)
    latest_commit = repo.head.commit

    # Create the tag
    print(f"Creating tag {tag_name} on commit {latest_commit.hexsha}...")
    repo.create_tag(tag_name, message=tag_message)
    # Push the tag to the remote repository
    print(f"Pushing tag {tag_name} to remote...")
    origin = repo.remote(name='origin')
    origin.push(f"refs/tags/{tag_name}")

    upstream = repo.remote(name='upstream')
    upstream.push(f"refs/tags/{tag_name}")


def handle_local_repo(repo, repo_path):
    # Ensure the repository is not bare
    if repo.bare:
        print(f"Local Repository at {repo_path} is bare.")
        exit(1)

    # Add files to the staging area
    repo.git.add(A=True)

    com_msg = 'materials-generate-scripts update lectures and reference'
    # Commit the changes
    if repo.head.commit:
        print("No changes to commit.")
    else:
        repo.index.commit(com_msg)

    # Pull the latest changes from the remote repository
    # Push the changes to the remote repository
    origin = repo.remotes.origin
    origin.push(force=True)


def handle_pr(pr_args):
    pr_title = pr_args["pr_name"]
    pr_body = pr_args["pr_name"]
    upstream_repo = pr_args["upstream_repo"]
    upstream_repo_branch = pr_args["upstream_repo_branch"]
    forked_repo = pr_args["forked_repo"]
    forked_repo_branch = pr_args["forked_repo_branch"]
    local_repo = pr_args["local_repo"]
    pr_comm_msg = pr_args["pr_comm_msg"]

    # Create a pull request
    # Compare commits between base branch and forked repo branch
    base_ref = upstream_repo.get_branch(upstream_repo_branch)
    compare = upstream_repo.compare(base_ref.commit.sha, f"{forked_repo.owner.login}:{forked_repo_branch}")

    # Check if there are any changes to commit
    if compare.total_commits == 0:
        print("No PR needed")
    else:
        pull_request = upstream_repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=f"{forked_repo.owner.login}:{forked_repo_branch}",
            base=upstream_repo_branch
        )
        print(f"Pull request created: {pull_request.html_url}")

        # Get the pull request
        pull = upstream_repo.get_pull(pull_request.number)

        # Merge the pull request
        pull.merge(commit_message=pr_comm_msg)
        print(f"Pull request #{pull_request.number} merged successfully.")

        if tag_exists(local_repo, TAG_NAME):
            remove_tag(local_repo, TAG_NAME)
        create_tag(local_repo, TAG_NAME, TAG_MESSAGE)

        up = local_repo.remotes.upstream
        up.pull(upstream_repo_branch)

        orig = local_repo.remotes.origin
        orig.push(forked_repo_branch)


def handle_repo(org, r, pr_name):
    repo_path = f"{ROOT_PATH}/{r}"
    access_token = access_tokens[org]

    forked_repo_name = f'{FORKED_REPO_NAME}/{r}'
    forked_repo_branch = 'main'

    upstream_repo_name = f'{org}/{r}'
    upstream_repo_branch = 'main'
    print(f"{r} - start =========")
    try:
        local_repo = Repo(repo_path)
        g = Github(access_token)

        forked_repo = g.get_repo(forked_repo_name)
        upstream_repo = g.get_repo(upstream_repo_name)

        handle_local_repo(local_repo, repo_path)
        handle_pr({
                "pr_name": pr_name,
                "local_repo": local_repo,
                "forked_repo": forked_repo,
                "upstream_repo": upstream_repo,
                "forked_repo_branch": forked_repo_branch,
                "upstream_repo_branch": upstream_repo_branch,
                "pr_comm_msg": pr_name
            }
        )
    except GithubException as e:
        print(f"Error handling repo: {e.data['message']}")
    except Exception as e:
        print(traceback.format_exc())
        print(f"Unexpected error: {e}")
    print(f"{r} - done =========")


repos = {
    "data-8": [
            "materials-sp22-private",
            "materials-sp22",
            "materials-sp22-colab",
            "materials-sp22-binder",
            "materials-sp22-jupyterlite",
            "materials-sp22-no-footprint",
            "materials-sp22-colab-no-footprint",
            "materials-sp22-binder-no-footprint",
            "materials-sp22-jupyterlite-no-footprint"
    ],
    "ds-modules": [
            "materials-sp22-assets"
    ]
}

PR_COMMIT_MESSAGE = "Updates: Lecture and References"
FORKED_REPO_NAME = "sean-morris"
TAG_NAME = 'otter-4.4.1'
TAG_MESSAGE = 'otter-4.4.1'
ROOT_PATH = os.path.dirname(os.getcwd())
access_tokens = get_tokens("tokens.json")


def main(repo):
    for org, list_repos in repos.items():
        for r in list_repos:
            if not repo or r == repo:
                handle_repo(org, r, PR_COMMIT_MESSAGE)


main("materials-sp22-assets")
print("Changes pulled, committed, and pushed successfully.")
