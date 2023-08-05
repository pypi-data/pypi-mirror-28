#!/bin/bash -ex

NODEPOOL_INSTALL=${NODEPOOL_INSTALL:-/opt/stack/new/nodepool-venv}
NODEPOOL_CONFIG=${NODEPOOL_CONFIG:-/etc/nodepool/nodepool.yaml}
NODEPOOL_SECURE=${NODEPOOL_SECURE:-/etc/nodepool/secure.conf}
NODEPOOL="$NODEPOOL_INSTALL/bin/nodepool -c $NODEPOOL_CONFIG -s $NODEPOOL_SECURE"

# Flags to control which images we build.
# NOTE(pabelanger): Be sure to also update devstack/settings if you change the
# defaults.
NODEPOOL_PAUSE_CENTOS_7_DIB=${NODEPOOL_PAUSE_CENTOS_7_DIB:-true}
NODEPOOL_PAUSE_DEBIAN_JESSIE_DIB=${NODEPOOL_PAUSE_DEBIAN_JESSIE_DIB:-true}
NODEPOOL_PAUSE_FEDORA_26_DIB=${NODEPOOL_PAUSE_FEDORA_26_DIB:-true}
NODEPOOL_PAUSE_OPENSUSE_423_DIB=${NODEPOOL_PAUSE_OPENSUSE_423_DIB:-true}
NODEPOOL_PAUSE_UBUNTU_TRUSTY_DIB=${NODEPOOL_PAUSE_UBUNTU_TRUSTY_DIB:-false}
NODEPOOL_PAUSE_UBUNTU_XENIAL_DIB=${NODEPOOL_PAUSE_UBUNTU_XENIAL_DIB:-true}

function sshintonode {
    name=$1
    state='ready'

    node=`$NODEPOOL list | grep $name | grep $state | cut -d '|' -f11 | tr -d ' '`
    /tmp/ssh_wrapper $node ls /
}

function waitforimage {
    name=$1
    state='ready'

    while ! $NODEPOOL image-list | grep $name | grep $state; do
        $NODEPOOL image-list > /tmp/.nodepool-image-list.txt
        $NODEPOOL list > /tmp/.nodepool-list.txt
        sudo mv /tmp/.nodepool-image-list.txt $WORKSPACE/logs/nodepool-image-list.txt
        sudo mv /tmp/.nodepool-list.txt $WORKSPACE/logs/nodepool-list.txt
        sleep 10
    done
}

function waitfornode {
    name=$1
    state='ready'

    while ! $NODEPOOL list | grep $name | grep $state; do
        $NODEPOOL image-list > /tmp/.nodepool-image-list.txt
        $NODEPOOL list > /tmp/.nodepool-list.txt
        sudo mv /tmp/.nodepool-image-list.txt $WORKSPACE/logs/nodepool-image-list.txt
        sudo mv /tmp/.nodepool-list.txt $WORKSPACE/logs/nodepool-list.txt
        sleep 10
    done
}

if [ $NODEPOOL_PAUSE_CENTOS_7_DIB = 'false' ]; then
    # check that image built
    waitforimage centos-7
    # check image was bootable
    waitfornode centos-7
    # check ssh for root user
    sshintonode centos-7
fi

if [ $NODEPOOL_PAUSE_DEBIAN_JESSIE_DIB = 'false' ]; then
    # check that image built
    waitforimage debian-jessie
    # check image was bootable
    waitfornode debian-jessie
    # check ssh for root user
    sshintonode debian-jessie
fi

if [ $NODEPOOL_PAUSE_FEDORA_26_DIB = 'false' ]; then
    # check that image built
    waitforimage fedora-26
    # check image was bootable
    waitfornode fedora-26
    # check ssh for root user
    sshintonode fedora-26
fi

if [ $NODEPOOL_PAUSE_OPENSUSE_423_DIB = 'false' ]; then
    # check that image built
    waitforimage opensuse-423
    # check image was bootable
    waitfornode opensuse-423
    # check ssh for root user
    sshintonode opensuse-423
fi

if [ $NODEPOOL_PAUSE_UBUNTU_TRUSTY_DIB = 'false' ]; then
    # check that image built
    waitforimage ubuntu-trusty
    # check image was bootable
    waitfornode ubuntu-trusty
    # check ssh for root user
    sshintonode ubuntu-trusty
fi

if [ $NODEPOOL_PAUSE_UBUNTU_XENIAL_DIB = 'false' ]; then
    # check that image built
    waitforimage ubuntu-xenial
    # check image was bootable
    waitfornode ubuntu-xenial
    # check ssh for root user
    sshintonode ubuntu-xenial
fi

set -o errexit
# Show the built nodes
$NODEPOOL list

# Try to delete the nodes that were just built
$NODEPOOL delete --now 1

# show the deleted nodes (and their replacements may be building)
$NODEPOOL list
