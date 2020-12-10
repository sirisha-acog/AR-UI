FROM aganitha/base-jupyterlab-gpu:py37-appmode

ARG PIP_EXTRA_INDEX_URL=https://pypi.own3.aganitha.ai/simple
ENV PIP_EXTRA_INDEX_URL ${PIP_EXTRA_INDEX_URL}



USER jupyter
COPY custom_steps.txt /home/jupyter/
USER root
WORKDIR /home/jupyter
RUN if which pip 2>/dev/null; then echo "pip found" && pip install --upgrade pip; fi
RUN rm -rf /opt/conda/lib/python3.6/site-packages/yaml 2>/dev/null
RUN rm -rf /opt/conda/lib/python3.6/site-packages/PyYAML-* 2>/dev/null
RUN rm -rf /opt/conda/lib/python3.6/site-packages/certifi* 2>/dev/null
RUN pip install certifi==2018.4.16
RUN pip install PyYAML==5.1
RUN apt -y update
RUN apt -y install libgl1-mesa-glx
USER jupyter
COPY requirements.txt /home/jupyter/
USER root
WORKDIR /home/jupyter
RUN pip install -r requirements.txt
RUN pip install matplotlib
RUN pip install opencv-python

USER jupyter


WORKDIR /home

USER root

RUN echo "umask 0002" >> /home/jupyter/.bashrc
RUN if grep -q "::" /etc/group || grep -q "^" /etc/group ; then echo "Group with id  or with name  already exists"; else groupadd  -g ; fi
# RUN usermod -aG jupyter

USER jupyter

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh", "/home"]

CMD ["jupyter", "notebook", "--ip=*", "--no-browser"]
