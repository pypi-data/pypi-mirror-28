import json

from canaryd.packages.check_output import CalledProcessError, check_output


def _make_container(data):
    blank_container = {
        'environment': [],
        'names': [],
        'ips': [],
    }

    blank_container.update(data)

    return blank_container


def get_docker_containers():
    containers = {}

    try:
        output = check_output(
            'docker inspect `docker ps -qa`',
            shell=True,
        )

    # Either Docker is down or there are no containers
    except CalledProcessError:
        return containers

    data = json.loads(output)

    for container in data:
        container_data = {
            'runtime': 'docker',
            'running': container['State']['Running'],
            'command': ' '.join(container['Config']['Cmd']),
            'environment': container['Config']['Env'],
            'image': container['Config']['Image'],
            'id': container['Id'],
        }

        # Figure out the name(s)
        if 'Names' in container:
            container_data['names'] = container['Names']

        elif 'Name' in container:
            container_data['names'] = [container['Name']]

        # If running, get the PID
        if container_data['running']:
            container_data['pid'] = container['State']['Pid']

        container_id = container['Id'][:6]
        container_key = 'docker/{0}'.format(container_id)

        containers[container_key] = _make_container(container_data)

    return containers


def get_lxc_containers():
    output = check_output(
        'lxc list --fast --format json',
        shell=True,
    )

    data = json.loads(output)
    containers = {}

    for container in data:
        container_data = {
            'runtime': 'lxc',
            'names': [container['name']],
            'running': container['status'] == 'Running',
        }

        container_key = 'lxc/{0}'.format(container['name'])
        containers[container_key] = _make_container(container_data)

    return containers


def get_openvz_containers():
    output = check_output(
        'vzlist -a -j',
        shell=True,
    )
    combined_json = ''.join(output)

    data = json.loads(combined_json)
    containers = {}

    for container in data:
        container_data = {
            'runtime': 'openvz',
            'ips': container['ip'],
            'image': container['ostemplate'],
            'running': container['status'] == 'running',
        }

        container_key = 'openvz/{0}'.format(container['ctid'])
        containers[container_key] = _make_container(container_data)

    return containers


def get_virsh_containers():
    output = check_output(
        'virsh list --all',
        shell=True,
    )
    containers = {}

    for line in output.splitlines()[2:]:
        bits = line.split()

        if len(bits) != 3:
            continue

        id, name, state = bits

        container_data = {
            'runtime': 'virsh',
            'names': [name],
            'running': state == 'running',
        }

        container_key = 'virsh/{0}'.format(name)
        containers[container_key] = _make_container(container_data)

    return containers
