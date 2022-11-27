
FROM python:3.9 AS poetry

COPY /salient_src/ /salient_src
COPY /salient_src/main.py ./
COPY pyproject.toml poetry.lock README.md requirements.txt ./ 


# start installing things with poetry
RUN pip install poetry
RUN pip install fasttext==0.9.1
RUN poetry install
RUN cat requirements.txt | xargs -I % sh -c 'poetry add "%"'
RUN pip install -r requirements.txt

CMD ["python", "/salient_src/main.py"]

#Tkinter required dependencies
# Download Package Information
RUN apt-get update -y
# Install Tkinter
RUN apt-get install tk -y

# Commands to run Tkinter application
CMD ["python", "/salient_src/salient_gui_tkinter.py"]
