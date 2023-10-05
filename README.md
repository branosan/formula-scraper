## About this app
This is my semestral project for the course Information retrieval taught at Slovak University of technology in Bratislava Faculty of Informatics and Information Technology.
## Setup
### LINUX/MACOS
1. If there is no virtual environment you'll need to create one using:
<pre>
python -m venv <venvname>
</pre>

2. Enter virtual environment:
<pre>
source <venvname>/bin/activate
</pre>

3. Install all necessary packages. (has to be written when virtual env is active)
<pre>
pip install -r requirements.txt
</pre>

4. To deactivate virtual environment
<pre>
deactivate
</pre>

### Windows
Please refer to guide [How To Set Up a Virtual Python Environment (Windows)](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html).

### How to run this project
To run this app write this command while the <abbr title="Virtual environmnet">venv</abbr> is running:
<pre>
python -m src <domain> <max_depth>
</pre>