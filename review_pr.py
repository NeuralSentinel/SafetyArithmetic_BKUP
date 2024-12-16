import os
import openai
from github import Github
import git
import textwrap

# Approximate chunk size to avoid token/size limits
TOKEN_LIMIT_CHARS = 12000

def get_file_content(file_path):
    """
    Reads the content of a file and returns it as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_changed_files(pr):
    """
    Clones the PR's repository and fetches all changed file contents in the PR.
    Returns a dict of { 'file_path': 'file_content' }.
    """
    # Clone the PR branch into ./repo
    repo = git.Repo.clone_from(pr.base.repo.clone_url, to_path='./repo', branch=pr.head.ref)

    # Compare base branch vs PR branch to find changed files
    base_ref = f"origin/{pr.base.ref}"
    head_ref = f"origin/{pr.head.ref}"
    diff_output = repo.git.diff(base_ref, head_ref, name_only=True).strip()

    if not diff_output:
        print("No files changed or diff is empty.")
        return {}

    changed_files = {}
    for file_path in diff_output.split('\n'):
        file_path = file_path.strip()
        if not file_path:
            continue
        try:
            full_path = os.path.join('./repo', file_path)
            changed_files[file_path] = get_file_content(full_path)
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
    return changed_files

def send_to_openai(files):
    """
    Sends changed file contents to OpenAI for code review.
    Returns a single string containing the aggregated review.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY', '')

    # Combine all file contents into one big string
    code_concat = "\n".join(files.values())

    # Break code into smaller chunks
    chunks = textwrap.wrap(code_concat, TOKEN_LIMIT_CHARS)
    
    reviews = []
    for chunk in chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Or "gpt-3.5-turbo" if you don't have GPT-4 access
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior code reviewer. "
                            "Your responsibility is to review the provided code, "
                            "offer detailed recommendations for improvement, highlight potential issues, "
                            "and evaluate the overall code quality."
                        )
                    },
                    {
                        "role": "user",
                        "content": chunk
                    }
                ],
            )
            ai_review = response.choices[0].message.content
            reviews.append(ai_review)
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            reviews.append(f"**OpenAI Error**: {e}")

    # Combine chunk reviews into a single text
    return "\n\n---\n\n".join(reviews)

def post_comment(pr, comment):
    """
    Posts a comment on the pull request with the AI-generated review.
    """
    pr.create_issue_comment(comment)

def get_pr_number(repo, branch_name):
    """
    Fetches the pull request number associated with the given branch.
    """
    try:
        pulls = repo.get_pulls(state='open')
        for pr in pulls:
            if pr.head.ref == branch_name:
                return pr.number
    except Exception as e:
        print(f"ERROR: Could not fetch pull requests. Error: {e}")
    return None

def main():
    """
    Main flow to auto-detect CHANGE_ID dynamically.
    """
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPO', '').replace('.git', '')
    branch_name = os.getenv('BRANCH_NAME', '')  # Passed dynamically by CI/CD or detected locally

    if not github_token or not repo_name or not branch_name:
        print("ERROR: Missing required environment variables: GITHUB_TOKEN, GITHUB_REPO, BRANCH_NAME.")
        return

    try:
        gh = Github(github_token)
        repo = gh.get_repo(repo_name)
        print(f"Connected to repository: {repo.full_name}")
    except Exception as e:
        print(f"ERROR: Could not connect to repository '{repo_name}'. Error: {e}")
        return

    # Dynamically detect PR number based on branch
    pr_number = get_pr_number(repo, branch_name)
    if pr_number is None:
        print(f"ERROR: No open pull request found for branch '{branch_name}'.")
        return

    print(f"Detected PR Number: {pr_number}")

    try:
        pr = repo.get_pull(pr_number)
        print(f"Fetched PR #{pr_number}: {pr.title}")
        # Add further processing logic here...
    except Exception as e:
        print(f"ERROR: Could not fetch PR #{pr_number}. Error: {e}")

if __name__ == "__main__":
    main()



# import os
# import openai
# from github import Github
# import git
# import json
# import textwrap

# # Load OpenAI API key from environment
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Set the maximum token limit for GPT-4
# TOKEN_LIMIT = 4000

# def get_file_content(file_path):
#     """
#     This function reads the content of a file.

#     Args:
#         file_path (str): The path to the file.

#     Returns:
#         str: The content of the file.
#     """
#     with open(file_path, 'r') as file:
#         return file.read()

# def get_changed_files(pr):
#     """
#     This function fetches the files that were changed in a pull request.

#     Args:
#         pr (PullRequest): The pull request object.

#     Returns:
#         dict: A dictionary containing the file paths as keys and their content as values.
#     """
#     # Clone the repository and checkout the PR branch
#     repo = git.Repo.clone_from(pr.base.repo.clone_url, to_path='./repo', branch=pr.head.ref)

#     # Get the difference between the PR branch and the base branch
#     base_ref = f"origin/{pr.base.ref}"
#     head_ref = f"origin/{pr.head.ref}"
#     diffs = repo.git.diff(base_ref, head_ref, name_only=True).split('\n')

#     # Initialize an empty dictionary to store file contents
#     files = {}
#     for file_path in diffs:
#         try:
#             # Fetch each file's content and store it in the files dictionary
#             files[file_path] = get_file_content('./repo/' + file_path)
#         except Exception as e:
#             print(f"Failed to read {file_path}: {e}")

#     return files

# def send_to_openai(files):
#     """
#     This function sends the changed files to OpenAI for review.

#     Args:
#         files (dict): A dictionary containing the file paths as keys and their content as values.

#     Returns:
#         str: The review returned by OpenAI.
#     """
#     # Concatenate all the files into a single string
#     code = '\n'.join(files.values())

#     # Split the code into chunks that are each within the token limit
#     chunks = textwrap.wrap(code, TOKEN_LIMIT)

#     reviews = []
#     for chunk in chunks:
#         # Send a message to OpenAI with each chunk of the code for review
#         message = openai.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": "You are assigned as a code reviewer. Your responsibility is to review the provided code and offer recommendations for enhancement. Identify any problematic code snippets, highlight potential issues, and evaluate the overall quality of the code you review:\n" + chunk
#                 }
#             ],
#         )

#         # Add the assistant's reply to the list of reviews
#         reviews.append(message.choices[0].message.content)

#     # Join all the reviews into a single string
#     review = "\n".join(reviews)

#     return review

# def post_comment(pr, comment):
#     """
#     This function posts a comment on the pull request with the review.

#     Args:
#         pr (PullRequest): The pull request object.
#         comment (str): The comment to post.
#     """
#     # Post the OpenAI's response as a comment on the PR
#     pr.create_issue_comment(comment)

# def main():
#     """
#     The main function orchestrates the operations of:
#     1. Fetching changed files from a PR
#     2. Sending those files to OpenAI for review
#     3. Posting the review as a comment on the PR
#     """
#     # Get the pull request event JSON
#     with open(os.getenv('GITHUB_EVENT_PATH')) as json_file:
#         event = json.load(json_file)
    
#     # Instantiate the Github object using the Github token
#     # and get the pull request object
#     pr = Github(os.getenv('GITHUB_TOKEN')).get_repo(event['repository']['full_name']).get_pull(event['number'])

#     # Get the changed files in the pull request
#     files = get_changed_files(pr)

#     # Send the files to OpenAI for review
#     review = send_to_openai(files)

#     # Post the review as a comment on the pull request
#     post_comment(pr, review)

# if __name__ == "__main__":
#     main()  # Execute the main function
