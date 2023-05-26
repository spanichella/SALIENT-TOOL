# Identifying Safety-Critical Concerns in Unmanned Aerial Vehicle (UAV) Software Platforms with SALIENT

SALIENT is a machine learning (ML)-enabled tool which analyzes individual sentences composing the issue reports of UAVs and automatically recognizes those describing a safety-related concern. The assessment of the classification performance of the tool on the issues of three popular open-source UAV-related projects demonstrates that SALIENT represents a viable solution to assist developers in timely identifying and triaging safety-critical UAV issues.

## Table of Contents

- [Architecture Overview](#Architecture-Overview)
- [HOW TO USE SALIENT](#HOW-TO-USE-SALIENT)
- [Setup](#Setup)
  - [Local Development Environment with GUI](#Local-Development-Environment-with-GUI)
  - [Using Docker](#Using-Docker)
- [Command Line Interface](#Command-Line-Interface)
- [Graphical User Interface](#Graphical-User-Interface)
- [License](#License)
- [References](#References)
- [Contacts](#Contacts) 

## Architecture Overview

As shown in the Figure below, SALIENT supports two main usage modes thanks to its CLI and its GUI. 
![SALIENT’s Architecture](./SalientFlow.jpg)
The GUI is designed for general users (not necessarily developers), while the CLI is useful for UAV developers interested in automating the issue management process toward safety-related issues. Both the CLI and GUI are designed to allow developers/users to select issues as well as write and edit issues. Then, specific CLI commands and specific GUI events support the developers/users in the automated identification (or classification) of sentences in issues concerning safety-related aspects of UAVs. The CLI and the GUI of SALIENT enable the aforementioned steps by leveraging (or interacting with) two components: the GitHub Issue Parser and the ML Component. The users/developers (i) interact with the GitHub Issue Parser via the CLI or the GUI, with the component able to preprocess issues downloaded from Github in different formats (explained in later sections) and preprocess them (e.g., splitting the issue text logically in sentences) for the next analysis. Once the data are pre-processed, (ii) the users/developers interact with the ML Component via the CLI (or the GUI) of SALIENT. which allows them to identify sentences with safety-related implications. Specifically, in this process, the data pre-processed by the GitHub Issue Parser are then provided as input to the SALIENT ’s ML Component which identifies (or classifies) the individual sentences that are safety-related. To support developers/users during the issue management process, the ML Component uses a model we trained in our previous work (reference mentioned in this repository) to classify safety-related sentences in newly reported UAV issues in GitHub. The training, tuning, and accuracy of the ML model employed by SALIENT are detailed in our previous work (reference mentioned in this repository).

## HOW TO USE SALIENT 
Demonstration Video:

[add the video here]

## Setup

1. Clone this repository

`git clone https://github.com/spanichella/SALIENT-TOOL.git`

### Local Development Environment (With GUI)

2. Make sure you have all the Requirements

- Python 3.9
- [Docker](https://docs.docker.com/get-docker/)
- [Poetry](https://python-poetry.org/docs/#installation)  
- [tkinter](https://docs.python.org/3/library/tkinter.html)

```
apt-get update
sudo apt-get install tk # on macosx pip3 install tk
```

3. Install the requirements usint poetry:

```
poetry install
cat requirements.txt | xargs -I % sh -c 'poetry add "%"'
pip install -r requirements.txt
```

4. Install fasttext:

`pip install fasttext==0.9.1`

5. `cd salient_src`

6. Open the [GUI](#graphical-user-interface-gui):

`python salient_gui_tkinter.py`

7. Run the [CLI](#command-line-interface-cli):

`python Fasttext-Model-prediction-on-safety-unseen-data.py --infile config.json`

  <!-- (<https://realpython.com/dependency-management-python-poetry/>) then     - add it to your Home path (e.g., in Macos with "```export PATH="$HOME/.local/bin:$PATH"```")
    - check if all is fine from the command line, with  "```poetry --version```"
    - in case of issue try " ```curl -sSL https://install.python-poetry.org | python3 - \ & export PATH="$HOME/.local/bin:$PATH"  & poetry --version``` "
    - to update (or add) dependencies to poetry (assuming requirements.txt has been generated, e.g., by pypreqs): ```cat requirements.txt | xargs poetry add``` (If you do have version numbers you could modify this with ```cat requirements.txt | xargs -I % sh -c 'poetry add "%"'``` )
  <!-- - Install [XQuartz](https://www.xquartz.org/), relevant to run the SALIENT GUI in MacOsX, other version of the GUI are planned to support also Windows OS  (see [X11 for Windows and Mac](https://kb.thayer.dartmouth.edu/article/336-x11-for-windows-and-mac)) -->
<!-- with GUI:

5. Run XQuartz
  - ``` open -a XQuartz ```

6. Set your Mac (or Linux) IP address
  - ``` IP=$(/usr/sbin/ipconfig getifaddr en0) ```

7. Allow connections from Mac (or Linux) to XQuartz
  - ``` /opt/X11/bin/xhost + "$IP" ``` -->

<!-- 3. To run the SALIENT-TOOL GUI you need to run the following command on your (Mac on Linux machine) machine (**non interactive mode**):
  - ``` docker run -it -e DISPLAY="${IP}:0" -v /tmp/.X11-unix:/tmp/.X11-unix salient_tool ``` -->

<!-- 8. In case you want to run SALIENT-TOOL in an interactive way (this gives you access to both the SALIENT-TOOL GUI and the command line tool version):

- to run the SALIENT-TOOL GUI in an **"interative mode"**:
  - execute ``` docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw salient_tool bash ```
  - then **execute the GUI** within the container
    - ``` cd salient_src ```
    - ``` python salient_gui_tkinter.py ```
  - then **execute the command line** within the container
    - ``` cd salient_src ```
    - ``` python Fasttext-Model-prediction-on-safety-unseen-data.py --infile config.json ``` -->

### Using Docker
<!-- 2) In case a container with the same name is already running and you want to remove it (stop container with):

- ```docker container ls```
- ```docker container stop $(docker container ls -aq)```
- ```docker system prune```
- ```docker container ls``` -->

2. Build and tag the docker image:

`docker build . -t salient_tool` # in macosx can require "sudo": sudo docker build . -t salient_tool

<!-- 4) Check that the image is among the available images with the docker images command:

- ``` sudo docker images ``` -->
3. Run the container and open bash:
<!-- without GUI: -->
`docker run -it salient_tool bash`

4. Start using the [CLI](#command-line-interface-cli):

```python Fasttext-Model-prediction-on-safety-unseen-data.py --infile config.json```

 (Optional) In case a container with the same name is already running and you want to remove it (i.e., stop container): 
```shell script
docker container ls
docker container stop $(docker container ls -aq)	
docker system prune
docker container ls
```

## Command Line Interface

SALIENT can be used as a Python command-line utility, which needs proper setup and configurations for execution. To simplify this process, we have included a Dockerfile that sets up all the requirements, runs the container, and opens the bash to interact with the tools, as reported in previous steps. To invoke SALIENT within (and outside) the container, with the configuration file config.json, SALIENT provides the following interfaces:

1. ```python Fasttext-Model-prediction-on-safety-unseen-data.py --infile config.json```

As demonstrated in the video and detailed in our repository, SALIENT’s config.json file contains different arguments as summarized in Table II (see figure below), which allows specifying the required inputs (i.e., the issue data), with the command above, to proceed with the analysis/classification of issues data and store the results in the specified file (with the file config.json). It is important to note that, if multiple Input types (see Table II) are provided as input with the config.json file, all of them are analyzed/classified and stored in the specified output file.

![SALIENT arguments and expected "Input types"](./TableTwo.png)

The CLI also allows storing the results locally. SALIENT provides different options to output the results with its GUI and its CLI. It is important to note that given as input issue data, the output of SALIENT corresponds to a structured file (in CSV format) containing the sentence ID, the text of the sentence classified, the label assigned to the sentence ("Yes" or "No", depending on the fact that the sentence concerns safety aspects), and the probability that the predicted label is actually correct: 
```
Sentence,Predicted_Label,Probability_of_Predicted_Label
0,AP_Arming: pre-arm check if compass1 is disabled but 2 or 3 are enabled.,"('__label__YES',)",0.670190691947937
...
```

## Graphical User Interface

Users can access the GUI with the following command:`python salient_gui_tkinter.py`

![SALIENT GUI](./gui-salient2.png)

As described before, to activate the GUI, it is sufficient to run `python salient_gui_tkinter.py`
The GUI is designed for general users (not necessarily developers) to allow developers/users to select issues as well as write and edit issues.
As demonstrated in the video (before in this repository), the SALIENT’s GUI allows to upload a text file (or CSV file) containing the text of the UAV issue (point 1in the figure), or the users/developers can directly copy and paste the text of the issue (point 2) in the GUI’s form (see image before). 

With the GUI it is possible to classify text of issues concerning safety aspects automatically (point 3), with relevant sentences highlighted in the specified color (default it is orange color). The GUI also allows storing the results locally. As described in previous paragraphs, SALIENT provides different options to output the results with its GUI (point 4) and its CLI (see previous paragraphs). It is important to note that given as input issue data, the output of SALIENT corresponds to a structured file (in CSV format) containing the sentence ID, the text of the sentence classified, the label assigned to the sentence ("Yes" or "No", depending on the fact that the sentence concerns safety aspects), and the probability that the predicted label is actually correct: 
```
Sentence,Predicted_Label,Probability_of_Predicted_Label
0,AP_Arming: pre-arm check if compass1 is disabled but 2 or 3 are enabled.,"('__label__YES',)",0.670190691947937
...
```

## License

```{code-block} text
SALIENT tool for the automated identification of Safety Concerns Reported in UAV Software Platforms.
Copyright (C) 2022  Sebastiano Panichella

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

The software we developed is distributed under GNU GPL license. See the
[LICENSE.md](https://github.com/spanichella/SALIENT-TOOL/LICENSE.md) file.

## References

If you use this tool in your research, please cite the following paper(s):

- Andrea Di Sorbo, Fiorella Zampetti, Corrado A. Visaggio, Massimiliano Di Penta, and Sebastiano Panichella: Automated Identification and Qualitative Characterization of Safety Concerns Reported in UAV Software Platforms. Transactions on Software Engineering and Methodology. 2022.

```{code-block} bibtex
@article{UAV:2022,
   author = {Di Sorbo, Andrea and Zampetti, Fiorella and Visaggio, Aaron and Di Penta, Massimiliano and Panichella, Sebastiano},
   title = {Automated Identification and Qualitative Characterization of Safety Concerns Reported in UAV Software Platforms},
   year = {2023},
   publisher = {Association for Computing Machinery},
   volume = {32},
   number = {3},
   doi = {10.1145/3564821},
   journal = {ACM Trans. Softw. Eng. Methodol.},
   articleno = {67},
   numpages = {37}
}
```

## Contacts

- **Dr. Sebastiano Panichella**
  - Zurich University of Applied Sciences (ZHAW), Switzerland - <panc@zhaw.ch> and <spanichella@gmail.com>
- Sajad Khatiri
  - Zurich University of Applied Sciences (ZHAW), Switzerland - <mazr@zhaw.ch>
- Dr. Andrea Di Sorbo:
  - University of Sannio, Italy - <disorbo@unisannio.it>
