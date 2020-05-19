FROM python:alpine3.11
RUN apk update && \
    apk upgrade && \
    apk add alpine-sdk postgresql-dev libffi-dev iptables ip6tables openrc
RUN python3 -m pip install --upgrade pip && python3 -m pip install --upgrade setuptools gunicorn
WORKDIR /app_dir/
COPY ./req.txt /app_dir/req.txt
RUN pip install -r req.txt

COPY . /app_dir
RUN dos2unix /app_dir/init.ash && \
    chmod +x /app_dir/init.ash
ENV PYTHONPATH=/app_dir


EXPOSE 8000

ENTRYPOINT ["./init.ash"]