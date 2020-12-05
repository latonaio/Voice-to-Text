FROM latonaio/pylib-lite:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=speech-to-text \
    AION_HOME=/var/lib/aion

# Setup Directoties
WORKDIR ${AION_HOME}
# Setup Directoties
RUN mkdir -p $AION_HOME/$POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/

ADD . .
RUN pip3 install google-cloud-speech
RUN python3 setup.py install

CMD ["/bin/sh", "docker-entrypoint.sh"]
