# Github Fingerprint (ALPHA)

Query GitHub APIs to gather information about repositories and generate a summary report. 

This is still a young, hacky project.

# Usage

1. **Requires** Python 3
2. `pip install -r requirements.txt`
3. Edit main.py to set the API `TOKEN` variable
4. `python main.py > out.html`

# TODO

1. Sparkline for commit activity
2. Match github's style of displaying languages
3. Cleaner CSS style
4. Look for and report on common files: TravisCI, (NPM) package.json, docker, etc.
5. Extract head of README. Get projects to use standard README header
6. Have standard locations for docs and planning materials
7. Have standard dev. env. deployment script
