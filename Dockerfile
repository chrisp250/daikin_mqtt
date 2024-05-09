ARG BUILD_FROM
FROM $BUILD_FROM

COPY rootfs /

WORKDIR /app

COPY main.py daikin.py requirements.txt . 
RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt

