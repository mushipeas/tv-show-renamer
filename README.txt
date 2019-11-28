Initialising project:

Recommended:
In root dir of project, run:
python -m venv .venv
This should create a virtual environment

To activate the environment:
.\.venv\Scripts\activate (Windows)
source env/bin/activate (UNIX)

To install required packages:
pip install -r requirements.txt
ffmpeg must also be installed and be in PATH.


For dev:
Once packages are installed and applied, using pip freeze will output all installed packages.
pip freeze

See:
https://pip.pypa.io/en/latest/user_guide/#requirements-files

test commands: