import os
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from github import Github

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

    con_id = args.get("consultation_id")

    # read json
    content = {}
    if con_id:
        json_path = os.path.join("fedlex", f"{con_id}.json")
        with open(json_path) as f:
            content = json.loads(f.read())

    return render_template('index.html', consultation_id=con_id, content=content)

@app.route('/submit_consultation', methods=['POST'])
def submit_calendar():
    response = {"status": "success"}
    data = request.get_json()
    print(data)

        # filename = data['municipality'].replace(' ', '_').replace('.', '').lower()
        # repo_path = f"csv/{filename}.csv"

        # br_id = str(uuid.uuid4())
        # branch = f"{filename}-{br_id}"

        # create_branch(branch)
        # add_csv_to_branch(branch, fp, repo_path)
        # create_pull_request(branch, f"New data for {data['municipality']}", "Please check")

    return jsonify(response)


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
def add_csv_to_branch(branch_name, csv_file, repo_path):
    # Replace with the name of your repository and the owner's username
    REPO_NAME = 'govtech24_kommentator2000'
    OWNER_NAME = 'metaodi'

    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the branch object
    branch = repo.get_branch(branch_name)

    # Read the contents of the CSV file
    contents = csv_file.read()
    print(contents)

    # Create the new file in the repository
    repo.create_file(
        path=repo_path,
        message='Add consultation version',
        content=contents,
        branch=branch_name
    )

    # Print a success message
    print('File added to branch.')

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

if __name__ == '__main__':
    app.run()

