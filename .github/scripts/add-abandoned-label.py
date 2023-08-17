from datetime import datetime, timedelta
import requests
import os


REPO_OWNER = 'maxcelant'
REPO_NAME = 'workflow-pg'
GH_TOKEN = 'token ' + os.environ['GH_TOKEN']
HEADERS = {
    'Authorization': GH_TOKEN,
    'Accept': 'application/vnd.github.v3+json'
}
API_BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"


def get_column_id(column_name):
    projects = requests.get(f"{API_BASE_URL}/projects", headers=HEADERS).json()
    for project in projects:
        columns = requests.get(project['columns_url'], headers=HEADERS).json()
        for column in columns:
            if column['name'] == column_name:
                return column['id']
    return None


def get_issues_from_column(column_id):
    cards = requests.get(
        f"https://api.github.com/projects/columns/{column_id}/cards", headers=HEADERS).json()
    return [card['content_url'].split('/')[-1] for card in cards if 'content_url' in card]


def add_abandoned_label(issue_number):
    data = {"labels": ["abandoned"]}
    requests.post(f"{API_BASE_URL}/issues/{issue_number}/labels",
                  headers=HEADERS, json=data)


def main():
    column_id = get_column_id("In Progress")
    if not column_id:
        print("Column 'In-Progress' not found.")
        return

    issue_numbers = get_issues_from_column(column_id)
    for issue_number in issue_numbers:
        issue = requests.get(
            f"{API_BASE_URL}/issues/{issue_number}", headers=HEADERS).json()
        updated_at = datetime.strptime(
            issue["updated_at"], '%Y-%m-%dT%H:%M:%SZ')
        if (datetime.utcnow() - updated_at) > timedelta(days=10):
            add_abandoned_label(issue_number)


if __name__ == "__main__":
    main()
