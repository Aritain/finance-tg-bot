FROM    alpine:3.14
COPY    bot/requirements.txt /bot/requirements.txt

RUN apk --no-cache upgrade && \
    apk --no-cache add python3 py3-pip py3-cryptography && \
    pip3 install --no-cache-dir -r /bot/requirements.txt

COPY    bot/ /bot

ENTRYPOINT ["python3", "/bot/main.py"]