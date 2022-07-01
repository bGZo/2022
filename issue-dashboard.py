import os
import re
import sys
from github import Github

def write_issue_to_file(issues, file):
    with open(file, "w+") as f:
        for issue in issues:
            f.write ('# ' + issue.title + ' Updated at ' + 
                    issue.updated_at.strftime("%Y-%m-%d") + '\n')
            if issue.body is not None:
                f.write (issue.body + '\n')
                f.write ('[⚓ Anchor of above parts](' + issue.html_url + ')\n\n')
            comments=issue.get_comments()
            for comment in comments:
                f.write(comment.body + '\n\n')
                f.write('[⚓ Anchor of above parts](' + comment.html_url + ')\n\n')
            f.write ('\n\n')
            print('Finished with ' + issue.title)
    f.close()

if __name__ == '__main__':
    file = 'readme.md'
    repoUrl = 'bgzo/2022'

    token = sys.argv[1]
    g = Github(token)
    repo = g.get_repo(repoUrl)
    name = g.get_user().login
    issues = repo.get_issues( labels=['api'],
                             state='open',
                             creator=name,
                             sort='updated')

    write_issue_to_file(issues, file)

    tablen = 4 # via: https://github.com/zhouie/github-md-toc/blob/master/github-md-toc.py
    with open(file, 'r') as f:
        lines = f.readlines()

    #FIXME: is there more effective way???
    with open(file, 'w') as f:
        for line in lines:
            matches = re.findall(r'(^#{1,6}) (.*)', line)
            if matches:
                h_level = len(matches[0][0])
                h_title = matches[0][1].strip()
                indent = ' ' * (tablen * (h_level - 1))
                md_link = re.sub(r' ', '-', re.sub(r'[^\d\w ]', '', h_title)).lower()
                f.write(('%s- [%s](#%s)') % (indent, h_title, md_link)+'\n')
        f.write('\n\n')
        for line in lines:
            f.write(line)
    f.close()
