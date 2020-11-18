from github import Label
from github import Issue


class GitObjectParser:

    @staticmethod
    def parser_issues(issues: list):
        issues_info = []
        for issue in issues:
            issue_info = GitObjectParser.parser_issue(issue)
            issues_info.append(issue_info)
        return issues_info

    @staticmethod
    def parser_issue(issue: Issue):
        info = {}
        info["name"] = issue.title
        info["labels"] = GitObjectParser.parser_labels(issue.labels)
        info["url"] = issue.url
        return info

    @staticmethod
    def parser_labels(labels: list) -> list:
        labels_info = []
        for label in labels:
            label_info = GitObjectParser.parser_label(label)
            labels_info.append(label_info)
        return labels_info

    @staticmethod
    def parser_label(label: Label) -> dict:
        info = {}
        info['name'] = label.name
        info["color"] = label.color
        return info