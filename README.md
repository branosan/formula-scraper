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
Entities will be structured in the resulting `.csv` file as follows:
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

## How to run this project
1. This project is supposed to run in a dev container. If you don't have dev container extension installed or set up in your IDE please install it. [Download for Dev Containers for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2.  Dev container configuration is already set up in the project in the folder `./.devcontainer`.
3. If you are running this project in Visual Studio Code press `CTRL+SHIFT+P` and type in `"Open folder in dev container"`. Then select this project folder.
4. To run this app write this command while the <abbr title="Virtual environmnet">venv</abbr> is running:
<pre>
python -m src
</pre>

## User manual
### Before using queries
1. User menu
<pre>
=========================Menu===========================
[c] Launch crawler "c [max_depth] [url]"
[s] Full text search "s [string]"
--------------------Called only once--------------------
[p] Create PyLucene index
[j] Join data from csv and json files                
[e] Create csv file with entities              
[q] Quit
</pre>
2. First you should start by crawling data from [pitwall.app](https://pitwall.app/seasons). As you can see this can be done by typing command `c <max_depth> <url>` where you set your desired depth for BFS and target url
3. Then you should create entity csv file from the crawled data by calling command `e`. This will automatically create all folders in the `data` folder which is also created automatically open starting the app.
4. Pylucene indexes data crawled which is joined with wikipedia data. Due to this you have to launch the Pyspark parser application first.
5. Indexing can be launched by typing command `p`. This will launch Pylucene indexer.
### Search using queries
1. To search using my queries type command `s`. You will be presented with a sub menu like this:
<pre>
[1] Find when two pilots met in a grand prix
[2] Find GPs with bad weather and count DNFs
[3] Find the most controversial GPs and pilots
[4] Basic search
</pre>
2. To pick any of the options type in the number associated with the query name. After that follow prompts which will appear on the screen.
3. If in any part of this process you want to go back press `ENTER`