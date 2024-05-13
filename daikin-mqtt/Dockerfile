ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /app
COPY app/requirements.txt .

RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt

COPY app/ .

COPY docker/run.sh /app/run.sh
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
