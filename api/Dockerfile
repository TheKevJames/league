FROM python:3.5.2-alpine

COPY requirements.txt /src/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /src/requirements.txt

COPY setup.py /src/setup.py
COPY setup.cfg /src/setup.cfg
COPY league_utils_api /src/league_utils_api
RUN pip install /src

CMD league-utils-api
