# SALIENT-TOOL


## A tool for the automated identification of "Safety Concerns" reported in UAV Software Platforms

## Requirements
- Python 3.9
- Docker
- Install [Poetry](https://python-poetry.org/)  (https://realpython.com/dependency-management-python-poetry/) then
  -  add it to your Home path (e.g., in Macos with "```export PATH="$HOME/.local/bin:$PATH"```")
  	-  check if all is fine from the command line, with  "```poetry --version```"
  - in case of issue try " ```curl -sSL https://install.python-poetry.org | python3 - \ & export PATH="$HOME/.local/bin:$PATH"  & poetry --version``` "
  - to update (or add) dependencies to poetry (assuming requirements.txt has been generated, e.g., by pypreqs): ```cat requirements.txt | xargs poetry add ``` (If you do have version numbers you could modify this with ```cat requirements.txt | xargs -I % sh -c 'poetry add "%"' ``` )
- Install [XQuartz](https://www.xquartz.org/), relevant to sun the SALIENT GUI in MacOsX, other version of the GUI are planned to support also Windows OS  (see [X11 for Windows and Mac](https://kb.thayer.dartmouth.edu/article/336-x11-for-windows-and-mac))

## How to SALIENT-TOOL GUI & The SALIENT-TOOL command line Version:
- 1) Clone this repository
- 2) In case a container with the same name is already running and you want to remove it (stop container with):
  - ```docker container ls```
  - ```docker container stop $(docker container ls -aq)	```
  - ```docker system prune```
  - ```docker container ls```
- 3) Build the image and name it:
  - ``` sudo docker build -t salient_tool . ```
- 4) Check that the image is among the available images with the docker images command:
  - ``` sudo docker images ```
- 5) Run XQuartz
  - ``` open -a XQuartz ```

- 6) Set your Mac (or Linux) IP address
  - ``` IP=$(/usr/sbin/ipconfig getifaddr en0) ```

- 7) Allow connections from Mac (or Linux) to XQuartz
  - ``` /opt/X11/bin/xhost + "$IP" ```

- 8) To run the SALIENT-TOOL GUI you need to run the following command on your (Mac on Linux machine) machine (non **interactive mode**):
  - ``` docker run -it -e DISPLAY="${IP}:0" -v /tmp/.X11-unix:/tmp/.X11-unix salient_tool ```
- 9) In case you want to run SALIENT-TOOL in an interactive way (this gives you access to both the SALIENT-TOOL GUI and the command line tool version):
    - to run the SALIENT-TOOL GUI in an **"interative mode"**:
      - execute ``` docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw salient_tool bash ```
      - then **execute the GUI** within the container 
        - ``` cd salient_src ```
        - ``` python salient_gui_tkinter.py ```
      - then **execute the command line** within the container 
        - ``` cd salient_src ```
        - ``` python Fasttext-Model-prediction-on-safety-unseen-data.py --infile config.json ``` 

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

* Andrea Di Sorbo, Fiorella Zampetti, Corrado A. Visaggio, Massimiliano Di Penta, and Sebastiano Panichella: Automated Identification and Qualitative Characterization of Safety Concerns Reported in UAV Software Platforms. Transactions on Software Engineering and Methodology. 2022.

```{code-block} bibtex
@article{UAV:2022,
  title={Automated Identification and Qualitative Characterization of Safety Concerns Reported in UAV Software Platforms},
  author={Andrea Di Sorbo and Fiorella Zampetti and  Corrado A. Visaggio  and Massimiliano Di Penta and Sebastiano Panichella},
  journal={Transactions on Software Engineering and Methodology},
  year={2022},
  publisher={Elsevier}
}
```

## Contacts
* Dr. Sebastiano Panichella
    * Zurich University of Applied Sciences (ZHAW), Switzerland - panc@zhaw.ch
* Sajad Khatiri
    * Zurich University of Applied Sciences (ZHAW), Switzerland - mazr@zhaw.ch
* Dr. Andrea Di Sorbo:
    * University of Sannio, Italy - disorbo@unisannio.it
