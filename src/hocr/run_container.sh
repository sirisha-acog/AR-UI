#!/bin/bash
atk-start-container.sh -vf ar-automation.cfg
source ar-automation.cfg
docker exec -u root ${CONTAINER_NAME} chgrp -R jupyter /home/jupyter/notebooks
docker exec -u root ${CONTAINER_NAME} chmod -R g+w  /home/jupyter/notebooks
docker exec -u root ${CONTAINER_NAME} chown -R jupyter /home/jupyter/.jupyter
docker exec -u root ${CONTAINER_NAME} chgrp -R jupyter /home/jupyter/data
docker exec -u root ${CONTAINER_NAME} chmod -R g+w  /home/jupyter/data

