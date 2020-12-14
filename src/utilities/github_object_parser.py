from github import Label, Issue, StatsCodeFrequency\
    , Commit, GitCommit, GitAuthor, CommitStats, NamedUser, IssueComment, PaginatedList


class GithubObjectParser:
    @staticmethod
    def parser_commits(commits: enumerate) -> list:
        commits_info = []
        for commit in commits:
            commits_info.append(
                GithubObjectParser.parser_commit(commit)
            )
        return commits_info

    @staticmethod
    def parser_commit(commit: Commit) -> dict:
        info = {}
        author = GithubObjectParser.parser_named_user(commit.author)
        info["author"] = author
        info['commit'] = GithubObjectParser.parser_git_commit(commit.commit)
        info['stats'] = GithubObjectParser.parser_commit_stats(commit.stats)
        return info

    @staticmethod
    def parser_stats_code_frequencies(stats_code_frequencies: list) -> list:
        code_frequencies_info = []
        for code_freq in stats_code_frequencies:
            code_frequencies_info.append(
                GithubObjectParser.parser_stats_code_frequency(code_freq)
            )
        return code_frequencies_info

    @staticmethod
    def parser_stats_code_frequency(stats_code_frequency: StatsCodeFrequency) -> dict:
        info = {}
        info["week"] = stats_code_frequency.week.strftime("%Y/%m/%d")
        info["additions"] = stats_code_frequency.additions
        info['deletion'] = stats_code_frequency.deletions
        return info

    @staticmethod
    def parser_issues(issues: list) -> list:
        issues_info = []
        for issue in issues:
            issue_info = GithubObjectParser.parser_issue(issue)
            issues_info.append(issue_info)
        return issues_info

    @staticmethod
    def parser_issue(issue: Issue) -> dict:
        info = {}
        info["title"] = issue.title
        info["labels"] = GithubObjectParser.parser_labels(issue.labels)
        info["time"] = issue.created_at.strftime('%Y/%m/%d')
        #info["comments"] = issue.get_comments
        info["comments"] = GithubObjectParser.parser_comments(issue.get_comments())
        return info

    @staticmethod
    def parser_labels(labels: list) -> list:
        labels_info = []
        for label in labels:
            label_info = GithubObjectParser.parser_label(label)
            labels_info.append(label_info)
        return labels_info

    @staticmethod
    def parser_label(label: Label) -> dict:
        info = {}
        info['name'] = label.name
        info["color"] = label.color
        return info

    @staticmethod
    def parser_comments(commentList: PaginatedList) -> list:
        comments_info = []
        for comment in commentList.get_page(0):
            comment_info = GithubObjectParser.parser_comment(comment)
            comments_info.append(comment_info)
        return comments_info

    @staticmethod
    def parser_comment(comment: IssueComment) -> dict:
        info = {}
        info['body'] = comment.body
        info["user"] = comment.user.login
        info["time"] = comment.created_at.strftime('%Y/%m/%d')
        return info


    @staticmethod
    def parser_named_user(name_user: NamedUser):
        info = {}
        info['name'] = name_user.name
        info['email'] = name_user.email
        return info

    @staticmethod
    def parser_git_commit(git_commit: GitCommit) -> dict:
        info = {}
        info["author"] = GithubObjectParser.parser_git_author(git_commit.author)
        info["message"] = git_commit.message
        info['html_url'] = git_commit.html_url
        info['url'] = git_commit.url
        return info

    @staticmethod
    def parser_git_author(git_author: GitAuthor) -> dict:
        info = {}
        info['name'] = git_author.name
        info['email'] = git_author.email
        info["date"] = git_author.date.strftime("%Y/%m/%d, %H:%M:%S")
        return info

    @staticmethod
    def parser_commit_stats(commit_stats: CommitStats):
        info = {}
        info["additions"] = commit_stats.additions
        info['deletions'] = commit_stats.deletions
        info['total'] = commit_stats.total
        return info