FROM python:3.11.5

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./packages.txt /app/packages.txt

RUN apt-get update && xargs -r -a /app/packages.txt apt-get install -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# User
RUN useradd -m -u 1000 user
USER user
ENV HOME /home/user
ENV PATH $HOME/.local/bin:$PATH

WORKDIR $HOME
RUN mkdir app
WORKDIR $HOME/app
COPY . $HOME/app

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]

