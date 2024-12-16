import os
import openai
import git
import textwrap
import subprocess

# Load OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set the maximum token limit for GPT-4
TOKEN_LIMIT = 4000

def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_changed_files(repo_path):
    repo = git.Repo(repo_path)
    print("Current branch:", repo.active_branch.name)
    repo.git.fetch()
    print("Remote branches:", repo.git.branch('-r'))

    # Try a more general diff if specifics fail
    result = repo.git.diff('--name-only')
    print("Diff result:", result)
    changed_files = result.splitlines()

    files = {}
    if not changed_files:
        print("Debug: No files listed from git diff.")

    for file_path in changed_files:
        full_path = os.path.join(repo_path, file_path)
        if os.path.isfile(full_path):
            try:
                files[file_path] = get_file_content(full_path)
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

    return files



def send_to_openai(files):
    code = '\n'.join(files.values())
    chunks = textwrap.wrap(code, TOKEN_LIMIT)
    reviews = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "Review this code:\n" + chunk}
            ],
        )
        reviews.append(response.choices[0].message.content)
    return '\n'.join(reviews)

def post_comment(review):
    print("OpenAI Code Review Output:")
    print(review)

def main():
    repo_path = os.getenv("WORKSPACE", "/workspace")
    github_repo = os.getenv("GITHUB_REPO")
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token or not github_repo:
        raise ValueError("Environment variables GITHUB_TOKEN and GITHUB_REPO are required.")

    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"Cloning repository {github_repo} to {repo_path}...")
        git.Repo.clone_from(f"https://{github_token}@github.com/{github_repo}.git", repo_path)

    repo = git.Repo(repo_path)
    repo.git.fetch()

    files = get_changed_files(repo_path)
    if not files:
        print("No changed files to review.")
        return

    review = send_to_openai(files)
    post_comment(review)

if __name__ == "__main__":
    main()




# import os
# import openai
# from github import Github
# import git
# import textwrap

# # Load OpenAI API key from environment
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Set the maximum token limit for GPT-4
# TOKEN_LIMIT = 4000

# def get_file_content(file_path):
#     """
#     Reads the content of a file.

#     Args:
#         file_path (str): The path to the file.

#     Returns:
#         str: The content of the file.
#     """
#     with open(file_path, 'r') as file:
#         return file.read()

# def get_changed_files(repo_path):
#     """
#     Fetches the list of changed files in the repository.

#     Args:
#         repo_path (str): The local path to the repository.

#     Returns:
#         dict: A dictionary containing file paths and their content.
#     """
#     repo = git.Repo(repo_path)
#     changed_files = [item.a_path for item in repo.index.diff(None)]
#     files = {}

#     for file_path in changed_files:
#         try:
#             files[file_path] = get_file_content(os.path.join(repo_path, file_path))
#         except Exception as e:
#             print(f"Failed to read {file_path}: {e}")
#     return files

# def send_to_openai(files):
#     """
#     Sends the changed files to OpenAI for review.

#     Args:
#         files (dict): A dictionary containing file paths and their content.

#     Returns:
#         str: The review returned by OpenAI.
#     """
#     code = '\n'.join(files.values())
#     chunks = textwrap.wrap(code, TOKEN_LIMIT)

#     reviews = []
#     for chunk in chunks:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": (
#                         "You are a code reviewer. Review the provided code, identify "
#                         "issues, and suggest improvements:\n" + chunk
#                     )
#                 }
#             ],
#         )
#         reviews.append(response.choices[0].message.content)

#     return '\n'.join(reviews)

# def post_comment(review):
#     """
#     Prints the review to stdout (Jenkins console output).

#     Args:
#         review (str): The review content.
#     """
#     print("OpenAI Code Review Output:")
#     print(review)

# def main():
#     """
#     Main function to orchestrate the code review.
#     """
#     # Fetch environment variables
#     repo_path = os.getenv("WORKSPACE", "/workspace")
#     github_repo = os.getenv("GITHUB_REPO")
#     github_token = os.getenv("GITHUB_TOKEN")

#     if not github_token or not github_repo:
#         raise ValueError("Environment variables GITHUB_TOKEN and GITHUB_REPO are required.")

#     # Clone the repository if it's not already cloned
#     if not os.path.exists(os.path.join(repo_path, ".git")):
#         print(f"Cloning repository {github_repo} to {repo_path}...")
#         git.Repo.clone_from(f"https://{github_token}@github.com/{github_repo}.git", repo_path)

#     # Get the changed files
#     files = get_changed_files(repo_path)

#     if not files:
#         print("No changed files to review.")
#         return

#     # Send the changed files to OpenAI
#     review = send_to_openai(files)

#     # Post the review
#     post_comment(review)

# if __name__ == "__main__":
#     main()




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
