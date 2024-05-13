ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt

COPY main.py daikin.py config.py run.sh /app/
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
