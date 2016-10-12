FROM python:2.7

# Timezone because docker is strange
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Create App Directory
ENV workDir /usr/src/speed-checker-flask
RUN mkdir -p ${workDir}
WORKDIR ${workDir}

#install app dependencies
RUN pip install Flask 
RUN pip install pygal
RUN pip install psycopg2

#copy code across
COPY templates/ ${workDir}/templates/
COPY app.py ${workDir}
COPY test.py ${workDir}
COPY .pgpass /root/

#permissions
RUN chmod 0600 /root/.pgpass

#Ports
EXPOSE 5000

#start
CMD python ${workDir}/app.py