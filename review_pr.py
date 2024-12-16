import os
import openai
from github import Github
import git
import textwrap

# Load OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
TOKEN_LIMIT = 4000  # character-based approximation

def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_changed_files(pr):
    repo = git.Repo('.')
    base_ref = f"origin/{pr.base.ref}"
    head_ref = 'HEAD'
    diffs = repo.git.diff(base_ref, head_ref, name_only=True).split('\n')
    files = {}
    for file_path in diffs:
        fpath = file_path.strip()
        if fpath:
            try:
                files[fpath] = get_file_content(fpath)
            except Exception as e:
                print(f"Failed to read {fpath}: {e}")
    return files

def send_to_openai(files):
    code = '\n'.join(files.values())
    chunks = textwrap.wrap(code, TOKEN_LIMIT)
    reviews = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are a code reviewer. Review the provided code and offer recommendations for enhancement. "
                        "Identify problematic snippets, highlight potential issues, and evaluate the overall quality:\n"
                        + chunk
                    )
                }
            ],
        )
        reviews.append(response.choices[0].message.content)
    return "\n".join(reviews)

def post_comment(pr, comment):
    pr.create_issue_comment(comment)

def main():
    pr_number = os.getenv('CHANGE_ID')
    repo_name = os.getenv('GITHUB_REPO')
    if not pr_number or not repo_name:
        raise ValueError("CHANGE_ID and GITHUB_REPO must be set.")

    github_token = os.getenv('GITHUB_TOKEN')
    g = Github(github_token)
    pr = g.get_repo(repo_name).get_pull(int(pr_number))

    files = get_changed_files(pr)
    review = send_to_openai(files)
    post_comment(pr, review)

    with open('review_output.txt', 'w') as f:
        f.write(review)

if __name__ == "__main__":
    main()

#tes
