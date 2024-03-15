import os
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from github import Github
import uuid

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Replace with your GitHub access token
ACCESS_TOKEN = os.getenv('GITHUB_PAT')


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def home():
    args = request.args

    sr_id = args.get("sr_id")

    # read json
    content = {'_metadata': {}, 'lines': {}}
    if sr_id:
        json_path = os.path.join("fedlex", f"{sr_id}.json")
        with open(json_path) as f:
            content = json.loads(f.read())

    return render_template('index.html', sr_id=sr_id, content=content['lines'], **content['_metadata'])

@app.route('/submit_consultation', methods=['POST'])
def submit_consultation():
    sr_id = request.form['sr_id']

    # read json
    json_path = os.path.join("fedlex", f"{sr_id}.json")
    with open(json_path) as f:
        content = json.loads(f.read())

    keys = request.form.getlist('keys')
    for key in keys:
        content['lines'][key]['text'] = request.form[f"{key}_text"]
        content['lines'][key]['comment'] = request.form[f"{key}_comment"]
    content_text = json.dumps(content, indent=4)

    repo_path = f"fedlex/{sr_id}.json"
    br_id = str(uuid.uuid4())
    branch = f"{sr_id}-{br_id}"
    create_branch(branch)
    update_file_in_branch(branch, content_text, repo_path)

    pr_url = create_pull_request(branch, f"New consultation for {content['_metadata']['short']}", "Please add your comments")

    return render_template('consultation.html', pr_url=pr_url, content=content)


# function to create new branch (wiring to app still missing)
def create_branch(new_branch_name):

    REPO_NAME = 'govtech24_kommentator2000'
    OWNER_NAME = 'metaodi'

    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the default branch name
    default_branch = repo.default_branch

    # Create a new branch based on the default branch
    new_branch = repo.create_git_ref(
        f"refs/heads/{new_branch_name}",
        repo.get_branch(default_branch).commit.sha
    )

    # Print the URL of the new branch
    print(f"New branch created: {new_branch.url}")


# function to add file to branch
def update_file_in_branch(branch_name, content, repo_path):
    # Replace with the name of your repository and the owner's username
    REPO_NAME = 'govtech24_kommentator2000'
    OWNER_NAME = 'metaodi'

    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the branch object
    branch = repo.get_branch(branch_name)

    # get current file
    contents = repo.get_contents(repo_path)

    # Read the contents of the CSV file
    print(contents)

    # Create the new file in the repository
    repo.update_file(
        path=repo_path,
        message='Add consultation version',
        sha=contents.sha,
        content=content,
        branch=branch_name
    )

    # Print a success message
    print('File updated in branch.')

# function to create pull request
def create_pull_request(branch_name, title, description):
    # Replace with the name of your repository and the owner's username
    REPO_NAME = 'govtech24_kommentator2000'
    OWNER_NAME = 'metaodi'
    
    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the main branch object
    main_branch = repo.get_branch(repo.default_branch)

    # Create a new pull request object
    pull_request = repo.create_pull(
        title=title,
        body=description,
        head=branch_name,
        base=main_branch.name
    )

    # Print a success message with the pull request URL
    print(f"Pull request created successfully: {pull_request.html_url}")
    return pull_request.html_url

if __name__ == '__main__':
    app.run()

