#!/bin/bash
#
# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

NODEPOOL_KEY=$HOME/.ssh/id_nodepool
NODEPOOL_KEY_NAME=root
NODEPOOL_PUBKEY=$HOME/.ssh/id_nodepool.pub
NODEPOOL_INSTALL=$HOME/nodepool-venv
NODEPOOL_CACHE_GET_PIP=/opt/stack/cache/files/get-pip.py

# Install shade from git if requested. If not requested
# nodepool install will pull it in.
function install_shade {
    if use_library_from_git "shade"; then
        GITREPO["shade"]=$SHADE_REPO_URL
        GITDIR["shade"]=$DEST/shade
        GITBRANCH["shade"]=$SHADE_REPO_REF
        git_clone_by_name "shade"
        # Install shade globally, because the job config has LIBS_FROM_GIT
        # and if we don't install it globally, all hell breaks loose
        setup_dev_lib "shade"
        # BUT - install shade into a virtualenv so that we don't have issues
        # with OpenStack constraints affecting the shade dependency install.
        # This particularly shows up with os-client-config
        $NODEPOOL_INSTALL/bin/pip install -e $DEST/shade
    fi
}

function install_diskimage_builder {
    if use_library_from_git "diskimage-builder"; then
        GITREPO["diskimage-builder"]=$DISKIMAGE_BUILDER_REPO_URL
        GITDIR["diskimage-builder"]=$DEST/diskimage-builder
        GITBRANCH["diskimage-builder"]=$DISKIMAGE_BUILDER_REPO_REF
        git_clone_by_name "diskimage-builder"
        setup_dev_lib "diskimage-builder"
        $NODEPOOL_INSTALL/bin/pip install -e $DEST/diskimage-builder
    fi
}

function install_glean {
    if use_library_from_git "glean"; then
        GITREPO["glean"]=$GLEAN_REPO_URL
        GITDIR["glean"]=$DEST/glean
        GITBRANCH["glean"]=$GLEAN_REPO_REF
        git_clone_by_name "glean"
        setup_dev_lib "glean"
        $NODEPOOL_INSTALL/bin/pip install -e $DEST/glean
    fi
}


# Install nodepool code
function install_nodepool {
    virtualenv $NODEPOOL_INSTALL
    install_shade
    install_diskimage_builder
    install_glean

    setup_develop $DEST/nodepool
    $NODEPOOL_INSTALL/bin/pip install -e $DEST/nodepool
}

# requires some globals from devstack, which *might* not be stable api
# points. If things break, investigate changes in those globals first.

function nodepool_create_keypairs {
    if [[ ! -f $NODEPOOL_KEY ]]; then
        ssh-keygen -f $NODEPOOL_KEY -P ""
    fi

    cat > /tmp/ssh_wrapper <<EOF
#!/bin/bash -ex
sudo -H -u stack ssh -o StrictHostKeyChecking=no -i $NODEPOOL_KEY root@\$@

EOF
    sudo chmod 0755 /tmp/ssh_wrapper
}

function nodepool_write_elements {
    sudo mkdir -p $(dirname $NODEPOOL_CONFIG)/elements/nodepool-setup/install.d
    sudo mkdir -p $(dirname $NODEPOOL_CONFIG)/elements/nodepool-setup/root.d
    cat > /tmp/01-nodepool-setup <<EOF
sudo mkdir -p /etc/nodepool
# Make it world writeable so nodepool can write here later.
sudo chmod 777 /etc/nodepool
EOF
    cat > /tmp/50-apt-allow-unauthenticated <<EOF
if [ -d "\$TARGET_ROOT/etc/apt/apt.conf.d" ]; then
    echo "APT::Get::AllowUnauthenticated \"true\";" | sudo tee \$TARGET_ROOT/etc/apt/apt.conf.d/95allow-unauthenticated
fi
EOF
    sudo mv /tmp/01-nodepool-setup \
        $(dirname $NODEPOOL_CONFIG)/elements/nodepool-setup/install.d/01-nodepool-setup
    sudo chmod a+x \
        $(dirname $NODEPOOL_CONFIG)/elements/nodepool-setup/install.d/01-nodepool-setup
    sudo mv /tmp/50-apt-allow-unauthenticated \
        $(dirname $NODEPOOL_CONFIG)/elements/nodepool-setup/root.d/50-apt-allow-unauthenticated
    sudo chmod a+x \
        $(dirname $NODEPOOL_CONFIG)/elements/nodepool-setup/root.d/50-apt-allow-unauthenticated
    sudo mkdir -p $NODEPOOL_DIB_BASE_PATH/images
    sudo mkdir -p $NODEPOOL_DIB_BASE_PATH/tmp
    sudo mkdir -p $NODEPOOL_DIB_BASE_PATH/cache
    sudo chown -R stack:stack $NODEPOOL_DIB_BASE_PATH
}

function nodepool_write_config {
    sudo mkdir -p $(dirname $NODEPOOL_CONFIG)
    sudo mkdir -p $(dirname $NODEPOOL_SECURE)
    local dburi=$(database_connection_url nodepool)

    cat > /tmp/logging.conf <<EOF
[formatters]
keys=simple

[loggers]
keys=root,nodepool,shade,kazoo,keystoneauth,novaclient

[handlers]
keys=console

[logger_root]
level=WARNING
handlers=console

[logger_nodepool]
level=DEBUG
handlers=console
qualname=nodepool
propagate=0

[logger_shade]
level=DEBUG
handlers=console
qualname=shade
propagate=0

[logger_keystoneauth]
level=DEBUG
handlers=console
qualname=keystoneauth
propagate=0

[logger_novaclient]
level=DEBUG
handlers=console
qualname=novaclient
propagate=0

[logger_kazoo]
level=INFO
handlers=console
qualname=kazoo
propagate=0

[handler_console]
level=DEBUG
class=StreamHandler
formatter=simple
args=(sys.stdout,)

[formatter_simple]
format=%(asctime)s %(levelname)s %(name)s: %(message)s
datefmt=
EOF

    sudo mv /tmp/logging.conf $NODEPOOL_LOGGING

    cat > /tmp/secure.conf << EOF
[database]
# The mysql password here may be different depending on your
# devstack install, you should double check it (the devstack var
# is MYSQL_PASSWORD and if unset devstack should prompt you for
# the value).
dburi: $dburi
EOF
    sudo mv /tmp/secure.conf $NODEPOOL_SECURE

    if use_library_from_git "glean"; then
        git --git-dir=$DEST/glean/.git checkout -b devstack
        DIB_GLEAN_INSTALLTYPE="DIB_INSTALLTYPE_simple_init: 'repo'"
        DIB_GLEAN_REPOLOCATION="DIB_REPOLOCATION_glean: '$DEST/glean'"
        DIB_GLEAN_REPOREF="DIB_REPOREF_glean: 'devstack'"
    fi

    if [ -f $NODEPOOL_CACHE_GET_PIP ] ; then
        DIB_GET_PIP="DIB_REPOLOCATION_pip_and_virtualenv: file://$NODEPOOL_CACHE_GET_PIP"
    fi
    if [ -f /etc/ci/mirror_info.sh ] ; then
        source /etc/ci/mirror_info.sh

        DIB_DISTRIBUTION_MIRROR_CENTOS="DIB_DISTRIBUTION_MIRROR: $NODEPOOL_CENTOS_MIRROR"
        DIB_DISTRIBUTION_MIRROR_DEBIAN="DIB_DISTRIBUTION_MIRROR: $NODEPOOL_DEBIAN_MIRROR"
        DIB_DISTRIBUTION_MIRROR_FEDORA="DIB_DISTRIBUTION_MIRROR: $NODEPOOL_FEDORA_MIRROR"
        DIB_DISTRIBUTION_MIRROR_UBUNTU="DIB_DISTRIBUTION_MIRROR: $NODEPOOL_UBUNTU_MIRROR"
        DIB_DEBOOTSTRAP_EXTRA_ARGS="DIB_DEBOOTSTRAP_EXTRA_ARGS: '--no-check-gpg'"
    fi

    cat > /tmp/nodepool.yaml <<EOF
# You will need to make and populate this path as necessary,
# cloning nodepool does not do this. Further in this doc we have an
# example element.
elements-dir: $(dirname $NODEPOOL_CONFIG)/elements
images-dir: $NODEPOOL_DIB_BASE_PATH/images
# The mysql password here may be different depending on your
# devstack install, you should double check it (the devstack var
# is MYSQL_PASSWORD and if unset devstack should prompt you for
# the value).
dburi: '$dburi'

zookeeper-servers:
  - host: localhost
    port: 2181

gearman-servers:
  - host: localhost
    port: 8991
zmq-publishers: []
# Need to have at least one target for node allocations, but
# this does not need to be a jenkins target.
targets:
  - name: dummy
    assign-via-gearman: True

cron:
  cleanup: '*/1 * * * *'
  check: '*/15 * * * *'

labels:
  - name: centos-7
    image: centos-7
    min-ready: 1
    providers:
      - name: devstack
  - name: debian-jessie
    image: debian-jessie
    min-ready: 1
    providers:
      - name: devstack
  - name: fedora-26
    image: fedora-26
    min-ready: 1
    providers:
      - name: devstack
  - name: opensuse-423
    image: opensuse-423
    min-ready: 1
    providers:
      - name: devstack
  - name: ubuntu-trusty
    image: ubuntu-trusty
    min-ready: 1
    providers:
      - name: devstack
  - name: ubuntu-xenial
    image: ubuntu-xenial
    min-ready: 1
    providers:
      - name: devstack

providers:
  - name: devstack
    region-name: '$REGION_NAME'
    cloud: devstack
    api-timeout: 60
    # Long boot timeout to deal with potentially nested virt.
    boot-timeout: 600
    launch-timeout: 900
    max-servers: 5
    rate: 0.25
    images:
      - name: centos-7
        min-ram: 1024
        name-filter: 'nodepool'
        username: devuser
        private-key: $NODEPOOL_KEY
        config-drive: true
        key-name: $NODEPOOL_KEY_NAME
      - name: debian-jessie
        min-ram: 512
        name-filter: 'nodepool'
        username: devuser
        private-key: $NODEPOOL_KEY
        config-drive: true
        key-name: $NODEPOOL_KEY_NAME
      - name: fedora-26
        min-ram: 1024
        name-filter: 'nodepool'
        username: devuser
        private-key: $NODEPOOL_KEY
        config-drive: true
        key-name: $NODEPOOL_KEY_NAME
      - name: opensuse-423
        min-ram: 1024
        name-filter: 'nodepool'
        username: devuser
        private-key: $NODEPOOL_KEY
        config-drive: true
        key-name: $NODEPOOL_KEY_NAME
      - name: ubuntu-trusty
        min-ram: 512
        name-filter: 'nodepool'
        username: devuser
        private-key: $NODEPOOL_KEY
        config-drive: true
        key-name: $NODEPOOL_KEY_NAME
      - name: ubuntu-xenial
        min-ram: 512
        name-filter: 'nodepool'
        username: devuser
        private-key: $NODEPOOL_KEY
        config-drive: true
        key-name: $NODEPOOL_KEY_NAME

diskimages:
  - name: centos-7
    pause: $NODEPOOL_PAUSE_CENTOS_7_DIB
    rebuild-age: 86400
    elements:
      - centos-minimal
      - vm
      - simple-init
      - devuser
      - openssh-server
      - nodepool-setup
    env-vars:
      TMPDIR: $NODEPOOL_DIB_BASE_PATH/tmp
      DIB_CHECKSUM: '1'
      DIB_IMAGE_CACHE: $NODEPOOL_DIB_BASE_PATH/cache
      DIB_DEV_USER_AUTHORIZED_KEYS: $NODEPOOL_PUBKEY
      $DIB_DISTRIBUTION_MIRROR_CENTOS
      $DIB_GET_PIP
      $DIB_GLEAN_INSTALLTYPE
      $DIB_GLEAN_REPOLOCATION
      $DIB_GLEAN_REPOREF
  - name: debian-jessie
    pause: $NODEPOOL_PAUSE_DEBIAN_JESSIE_DIB
    rebuild-age: 86400
    elements:
      - debian-minimal
      - vm
      - simple-init
      - devuser
      - openssh-server
      - nodepool-setup
    release: jessie
    env-vars:
      TMPDIR: $NODEPOOL_DIB_BASE_PATH/tmp
      DIB_CHECKSUM: '1'
      DIB_IMAGE_CACHE: $NODEPOOL_DIB_BASE_PATH/cache
      DIB_APT_LOCAL_CACHE: '0'
      DIB_DISABLE_APT_CLEANUP: '1'
      DIB_DEV_USER_AUTHORIZED_KEYS: $NODEPOOL_PUBKEY
      DIB_DEBIAN_COMPONENTS: 'main'
      $DIB_DISTRIBUTION_MIRROR_DEBIAN
      $DIB_DEBOOTSTRAP_EXTRA_ARGS
      $DIB_GET_PIP
      $DIB_GLEAN_INSTALLTYPE
      $DIB_GLEAN_REPOLOCATION
      $DIB_GLEAN_REPOREF
  - name: fedora-26
    pause: $NODEPOOL_PAUSE_FEDORA_26_DIB
    rebuild-age: 86400
    elements:
      - fedora-minimal
      - vm
      - simple-init
      - devuser
      - openssh-server
      - nodepool-setup
    release: 26
    env-vars:
      TMPDIR: $NODEPOOL_DIB_BASE_PATH/tmp
      DIB_CHECKSUM: '1'
      DIB_IMAGE_CACHE: $NODEPOOL_DIB_BASE_PATH/cache
      DIB_DEV_USER_AUTHORIZED_KEYS: $NODEPOOL_PUBKEY
      $DIB_DISTRIBUTION_MIRROR_FEDORA
      $DIB_GET_PIP
      $DIB_GLEAN_INSTALLTYPE
      $DIB_GLEAN_REPOLOCATION
      $DIB_GLEAN_REPOREF
  - name: opensuse-423
    pause: $NODEPOOL_PAUSE_OPENSUSE_423_DIB
    rebuild-age: 86400
    elements:
      - opensuse-minimal
      - vm
      - simple-init
      - devuser
      - openssh-server
      - nodepool-setup
    release: 42.3
    env-vars:
      TMPDIR: $NODEPOOL_DIB_BASE_PATH/tmp
      DIB_CHECKSUM: '1'
      DIB_IMAGE_CACHE: $NODEPOOL_DIB_BASE_PATH/cache
      DIB_DEV_USER_AUTHORIZED_KEYS: $NODEPOOL_PUBKEY
      $DIB_GET_PIP
      $DIB_GLEAN_INSTALLTYPE
      $DIB_GLEAN_REPOLOCATION
      $DIB_GLEAN_REPOREF
  - name: ubuntu-trusty
    pause: $NODEPOOL_PAUSE_UBUNTU_TRUSTY_DIB
    rebuild-age: 86400
    elements:
      - ubuntu-minimal
      - vm
      - simple-init
      - devuser
      - openssh-server
      - nodepool-setup
    release: trusty
    env-vars:
      TMPDIR: $NODEPOOL_DIB_BASE_PATH/tmp
      DIB_CHECKSUM: '1'
      DIB_IMAGE_CACHE: $NODEPOOL_DIB_BASE_PATH/cache
      DIB_APT_LOCAL_CACHE: '0'
      DIB_DISABLE_APT_CLEANUP: '1'
      DIB_DEV_USER_AUTHORIZED_KEYS: $NODEPOOL_PUBKEY
      DIB_DEBIAN_COMPONENTS: 'main,universe'
      $DIB_DISTRIBUTION_MIRROR_UBUNTU
      $DIB_DEBOOTSTRAP_EXTRA_ARGS
      $DIB_GET_PIP
      $DIB_GLEAN_INSTALLTYPE
      $DIB_GLEAN_REPOLOCATION
      $DIB_GLEAN_REPOREF
  - name: ubuntu-xenial
    pause: $NODEPOOL_PAUSE_UBUNTU_XENIAL_DIB
    rebuild-age: 86400
    elements:
      - ubuntu-minimal
      - vm
      - simple-init
      - devuser
      - openssh-server
      - nodepool-setup
    release: xenial
    env-vars:
      TMPDIR: $NODEPOOL_DIB_BASE_PATH/tmp
      DIB_CHECKSUM: '1'
      DIB_IMAGE_CACHE: $NODEPOOL_DIB_BASE_PATH/cache
      DIB_APT_LOCAL_CACHE: '0'
      DIB_DISABLE_APT_CLEANUP: '1'
      DIB_DEV_USER_AUTHORIZED_KEYS: $NODEPOOL_PUBKEY
      DIB_DEBIAN_COMPONENTS: 'main,universe'
      $DIB_DISTRIBUTION_MIRROR_UBUNTU
      $DIB_DEBOOTSTRAP_EXTRA_ARGS
      $DIB_GET_PIP
      $DIB_GLEAN_INSTALLTYPE
      $DIB_GLEAN_REPOLOCATION
      $DIB_GLEAN_REPOREF
EOF

    sudo mv /tmp/nodepool.yaml $NODEPOOL_CONFIG
    cp /etc/openstack/clouds.yaml /tmp
    cat >>/tmp/clouds.yaml <<EOF
cache:
  max_age: 3600
  class: dogpile.cache.dbm
  arguments:
    filename: $HOME/.cache/openstack/shade.dbm
  expiration:
    floating-ip: 5
    server: 5
    port: 5
EOF
    sudo mv /tmp/clouds.yaml /etc/openstack/clouds.yaml
    mkdir -p $HOME/.cache/openstack/
}

# Initialize database
# Create configs
# Setup custom flavor
function configure_nodepool {
    # build a dedicated keypair for nodepool to use with guests
    nodepool_create_keypairs

    # write the nodepool config
    nodepool_write_config

    # write the elements
    nodepool_write_elements

    # builds a fresh db
    recreate_database nodepool

}

function start_nodepool {
    # build a custom flavor that's more friendly to nodepool
    local available_flavors=$(nova flavor-list)
    if [[ ! ( $available_flavors =~ 'nodepool-512' ) ]]; then
        nova flavor-create nodepool-512 64 512 0 1
    fi
    if [[ ! ( $available_flavors =~ 'nodepool-1024' ) ]]; then
        nova flavor-create nodepool-1024 128 1024 0 1
    fi

    # build sec group rules to reach the nodes, we need to do this
    # this late because nova hasn't started until this phase.
    if [[ -z $(openstack security group rule list --protocol tcp default | grep '65535') ]]; then
        openstack --os-project-name demo --os-username demo security group rule create --ingress --protocol tcp --dst-port 1:65535 --remote-ip 0.0.0.0/0 default

        openstack --os-project-name demo --os-username demo security group rule create --ingress --protocol udp --dst-port 1:65535 --remote-ip 0.0.0.0/0 default

    fi

    # create root keypair to use with glean for devstack cloud.
    nova --os-project-name demo --os-username demo \
        keypair-add --pub-key $NODEPOOL_PUBKEY $NODEPOOL_KEY_NAME

    export PATH=$NODEPOOL_INSTALL/bin:$PATH

    # start gearman server
    run_process geard "$NODEPOOL_INSTALL/bin/geard -p 8991 -d"

    # run a fake statsd so we test stats sending paths
    export STATSD_HOST=localhost
    export STATSD_PORT=8125
    run_process statsd "/usr/bin/socat -u udp-recv:$STATSD_PORT -"

    run_process nodepool "$NODEPOOL_INSTALL/bin/nodepoold -c $NODEPOOL_CONFIG -s $NODEPOOL_SECURE -l $NODEPOOL_LOGGING -d"
    run_process nodepool-builder "$NODEPOOL_INSTALL/bin/nodepool-builder -c $NODEPOOL_CONFIG -l $NODEPOOL_LOGGING -d"
    :
}

function shutdown_nodepool {
    stop_process nodepool
    :
}

function cleanup_nodepool {
    :
}

# check for service enabled
if is_service_enabled nodepool; then

    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of service source
        echo_summary "Installing nodepool"
        install_nodepool

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configuring nodepool"
        configure_nodepool

    elif [[ "$1" == "stack" && "$2" == "test-config" ]]; then
        # Initialize and start the nodepool service
        echo_summary "Initializing nodepool"
        start_nodepool
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down nodepool services
        # no-op
        shutdown_nodepool
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        cleanup_nodepool
    fi
fi
