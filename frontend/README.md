
# Apprenticeship TDD Safari Project

This repository contains my TDD Safari project work for the apprenticeship, including the code, tests, supporting evidence, and instructions for running the app.

## Supporting Evidence

Supporting evidence can be found in the **Supporting Evidence** folder. These are saved as PDFs and a Markdown file.

**Note for VS Code users:** PDFs do not automatically render in VS Code so to view them directly in the editor, install the [VS Code PDF plugin](https://marketplace.visualstudio.com/items?itemName=tomoki1207.pdf).  

## BDD Tests
I have used Morelia for my BDD tests and these can be found in the `tests` directory.

## Running the App Locally


To run the app locally:

1. Make sure you have Python installed (Python 3.10+ recommended).
2. Install the project dependencies:

```bash
pip install -r requirements.txt
```

3. Open a terminal in the project folder.

4. Run the Flask app:

```bash
flask run 
```

The app will start and you can view it at:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)


## AWS Deployed Version

The app is deployed on an AWS EC2 instance in the Made Tech sandbox.

**Important notes:**

- The deployment is HTTP only, so if you click on a link starting with `https://`, remove the `s`.
- The sandbox is cleared every Friday, so a new AWS IAM role will need to be created and added to the GitHub repo secrets, and the app will need to be redeployed by re-running the GitHub workflow, if it has been removed from the sandbox.
