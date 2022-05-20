import os
import sys
from github import Github
from config import (IssueTableHead, IssueTableTemplate)
# from cfig import githubToken

def get_github_token_from_command():
    try:
        return sys.argv[1]
    except Exception as ex:
        print("[Get Token Failed] ")
        # raise Exception("[Failed Getting argv] Make Sure adding para after .py")


def get_repo_from_github(token, repoUrl):
    try:
        g = Github(token)
        return g.get_repo(repoUrl)
    except Exception as ex:
        print("[Get Repo Failed] ")


def get_update_issue_from_repo(token, repo):
    try:
        g = Github(token)
        return repo.get_issues(state='open', creator='bGZoCg', sort='updated')
    except Exception as ex:
        print("[Get Issues Failed] ")


def get_comments_from_issue(token, issue):
    try:
        g = Github(token)
        return issue.get_comments()
    except Exception as ex:
        print("[Get comments Failed] ")


def format_template_str(name, date, url):
    return IssueTableTemplate.format(
        issueName=name,
        issueUpdate=date,
        issueUrl=url
    )


def write_issue_to_file(repoIssues, fileName):
    with open(fileName, "w+") as f:
        f.write(IssueTableHead)
        for issue in repoIssues:
            issueName = str(issue.title)
            issueUpdate = str(issue.updated_at)
            issueUrl = '[#' + str(issue.number) + '](' + str(issue.html_url) + ')'
            f.write(format_template_str(issueName, issueUpdate, issueUrl))

def get_open_issues_by_me(issues, repoUrl):
    g = Github(token)
    repo = g.get_repo(repoUrl)
    user = g.get_user()
    name = user.login
    issues= repo.get_issues(state='open', creator=name, sort='updated')
    for issue in issues:
        fileName='./docs/'+issue.title + '.md'
        comments=issue.get_comments()

        with open(fileName, "a+") as f:
            print('ok')
            f.write(issue.body)
            for comment in comments:
                f.write(comment.body)
        f.close()

if __name__ == '__main__':
    # config env
    fileName = 'index.md'
    repoUrl = 'bgzocg/2022'
    githubToken = get_github_token_from_command()
    # config env end
    # FIXME: how to know Github function???

    repo = get_repo_from_github(githubToken, repoUrl)
    repoIssues = get_update_issue_from_repo(githubToken, repo)

    write_issue_to_file(repoIssues, fileName)

    # for issue in repoIssues:
        # comments = get_comments_from_issue(githubToken, issue)
