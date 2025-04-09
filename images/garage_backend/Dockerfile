FROM python:3.11-slim AS build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set initial working directory
WORKDIR /app

# Install build dependencies and clean up
RUN apt-get update && \
    apt-get install -y \
      gcc \
      default-libmysqlclient-dev \
      pkg-config \
      curl \
      netcat-openbsd && \
    apt-get remove -y \
      gcc \
      pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

# Copy and prepare entrypoint scripts
COPY entrypoint.sh .
COPY start-server.sh .

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN sed -i 's/\r$//g' /app/start-server.sh
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/start-server.sh

# Set up app directories
RUN mkdir -p /home/app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

# Copy project files to /home/app/web
COPY . $APP_HOME

# Set working directory to where manage.py is
WORKDIR $APP_HOME

# Define HOST_PORT (fix the undefined variable warning)
EXPOSE $HOST_PORT

FROM build AS local

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/app/start-server.sh"]

ENV START_COMMAND="0.0.0.0:${HOST_PORT}"