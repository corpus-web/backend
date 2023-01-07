FROM python:3.8

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's|security.debian.org/debian-security|mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list

RUN apt-get update --fix-missing \
#    && apt-get install -y build-essential libmariadb-dev \
    && pip3 install -r requirements.txt \
#    && apt-get remove -y build-essential \
    && apt-get autoclean -y \
    && apt-get autoremove -y

COPY academic_exchange /app/academic_exchange
COPY config /app/config
COPY corpus_content /app/corpus_content
COPY corpus_web /app/corpus_web
COPY course_construction /app/course_construction
COPY dist /app/dist
COPY home /app/home
COPY media /app/media
COPY message /app/message
COPY pkg /app/pkg
COPY team_style /app/team_style
COPY user /app/user
COPY manage.py /app/
COPY entrypoint.sh /app/
EXPOSE 8100
ENTRYPOINT ["sh", "/app/entrypoint.sh"]