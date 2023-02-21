function ansible { docker run -it --net=host --rm -w /code -v ${pwd}:/code --entrypoint /usr/local/bin/ansible ansible $args }

function ansible-playbook { docker run -it --net=host --rm -w /code -v ${pwd}:/code --entrypoint /usr/local/bin/ansible-playbook ansible $args }

function ansible-galaxy { docker run -it --net=host --rm -w /code -v ${pwd}:/code --entrypoint /usr/local/bin/ansible-galaxy ansible $args }

function ansible-vault { docker run -it --net=host --rm -w /code -v ${pwd}:/code --entrypoint /usr/local/bin/ansible-vault ansible $args }

function ansible-bash { docker run -it --net=host --rm -w /code -v ${pwd}:/code --entrypoint /bin/bash ansible $args }
