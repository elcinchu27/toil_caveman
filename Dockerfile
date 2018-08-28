FROM leukgen/docker-cgp:v1.1

# mount the output volume as persistant
ENV OUTPUT_DIR /data
VOLUME ${OUTPUT_DIR}

# install toil_pindel
COPY . /code
RUN pip install /code && rm -rf /code

# add entry point
ENTRYPOINT ["toil_caveman"]
