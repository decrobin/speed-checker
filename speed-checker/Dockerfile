# https://hub.docker.com/, argon is the LTS version of node (4.6)
FROM python:2.7

# Timezone because docker is strange
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Create App Directory
ENV workDir /usr/src/speed-checker
RUN mkdir -p ${workDir}
WORKDIR ${workDir}

#install app dependencies
RUN pip install speedtest-cli
RUN apt-get update && apt-get --yes --force-yes install cron
RUN apt-get --yes --force-yes install postgresql-client

#move things, permissions
COPY crontab ${workDir}
COPY speed-checker.sh ${workDir}
COPY .pgpass /root

RUN chmod 0600 ~/.pgpass
RUN chmod 777 ${workDir}/speed-checker.sh
ADD crontab /etc/cron.d/speed-checker-cron
RUN chmod 0644 /etc/cron.d/speed-checker-cron

#set up log file
RUN touch /usr/src/speed-checker/speed.log
RUN echo "Date, Time, Ping (ms), Download (Mbit), Upload (Mbit)" >> /usr/src/speed-checker/speed.log

#Run
CMD cron && tail -f /usr/src/speed-checker/speed.log
