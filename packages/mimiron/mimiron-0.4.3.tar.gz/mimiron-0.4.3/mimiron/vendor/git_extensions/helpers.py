# -*- coding: utf-8 -*-
from git import Actor
from mimiron.vendor.git_extensions.util import git_failure


@git_failure
def get_ahead_behind_count(repo):
    branch = repo.active_branch

    commits_behind = repo.iter_commits('%s..origin/%s' % (branch, branch,))
    commits_behind = len(list(commits_behind))

    commits_ahead = repo.iter_commits('origin/%s..%s' % (branch, branch,))
    commits_ahead = len(list(commits_ahead))

    return commits_ahead, commits_behind


@git_failure
def get_host_author(repo):
    return Actor.author(repo.config_reader())
