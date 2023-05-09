
FROM python:3.9 AS poetry
RUN pip install poetry
#Tkinter required dependencies
# Download Package Information
RUN apt-get update -y
# Install Tkinter
RUN apt-get install tk -y

COPY pyproject.toml poetry.lock README.md requirements.txt /src/
COPY /salient_src/ /src/salient_src/
# start installing things with poetry
WORKDIR /src/
RUN poetry install
RUN cat requirements.txt | xargs -I % sh -c 'poetry add "%"'
RUN pip install -r requirements.txt
RUN pip install fasttext==0.9.1

# Commands to run Tkinter application
WORKDIR /src/salient_src/
# CMD ["python", "/src/salient_src/salient_gui_tkinter.py"]
