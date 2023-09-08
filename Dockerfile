FROM python:3
USER root
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . /backend/
RUN chmod +x ./entrypoint-web.sh
RUN chmod +x ./entrypoint-worker.sh
# ENTRYPOINT [ "./entrypoint-web.sh" ]