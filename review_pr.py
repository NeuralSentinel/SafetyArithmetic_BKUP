import os
import openai
from github import Github
import git

# Constants
TOKEN_LIMIT_CHARS = 12000

def get_changed_files(repo, pr_number):
    """
    Fetch changed files in a pull request.
    """
    pr = repo.get_pull(pr_number)
    changed_files = {}
    for file in pr.get_files():
        try:
            content = repo.get_contents(file.filename, ref=pr.head.ref)
            changed_files[file.filename] = content.decoded_content.decode('utf-8')
        except Exception as e:
            print(f"Failed to fetch {file.filename}: {e}")
    return changed_files

def send_to_openai(files):
    """
    Sends changed file contents to OpenAI for code review.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    code_concat = "\n".join(files.values())
    chunks = [code_concat[i:i+TOKEN_LIMIT_CHARS] for i in range(0, len(code_concat), TOKEN_LIMIT_CHARS)]
    reviews = []
    for chunk in chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a code reviewer. Provide feedback on the given code."},
                    {"role": "user", "content": chunk}
                ],
            )
            reviews.append(response.choices[0].message.content)
        except Exception as e:
            reviews.append(f"Error: {e}")
    return "\n\n---\n\n".join(reviews)

def post_comment(repo, pr_number, comment):
    """
    Post a comment to a pull request.
    """
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)

def main():
    """
    Main function to handle the workflow.
    """
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPO')
    
    if not github_token or not repo_name:
        print("Missing GITHUB_TOKEN or GITHUB_REPO.")
        return

    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    
    pr_number = os.getenv('CHANGE_ID')
    if not pr_number:
        print("CHANGE_ID is not set.")
        return
    
    changed_files = get_changed_files(repo, int(pr_number))
    if not changed_files:
        print("No changed files detected.")
        return

    review = send_to_openai(changed_files)
    post_comment(repo, int(pr_number), review)

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
