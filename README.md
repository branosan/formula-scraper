## About this app
This is my semestral project for the course Information retrieval taught at Slovak University of technology in Bratislava Faculty of Informatics and Information Technology.
## Entity structure
The aim of this project is to look up information from freely accessible websites about formula 1. Entities for this project will be:
- Grand prix
- Drivers/Pilots
- Team they are driving for
- Position they finished the race at
- Their nationality
- Points after the race
Entities will be structured in the resulting `.tsv` file as follows:
<pre>
GRAND PRIX | POSITION | DRIVER NAME | TEAM | | NATIONALITY | POINTS
</pre>
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
python -m src
</pre>