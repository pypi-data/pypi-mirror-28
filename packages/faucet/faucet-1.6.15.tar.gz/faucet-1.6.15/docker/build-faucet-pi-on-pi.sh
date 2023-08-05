#!/bin/bash

# run from cron on Raspberry Pi build farm.

date
cd $(dirname $0) && \
cd .. && \
git stash && \
git checkout -q master && \
git pull 2>&1 || exit 1

TMPDIR=$(mktemp -d /tmp/$(basename $0).XXXXXX)
DOCKER_ID_USER="faucet"
DOCKER="docker"
TAGS=$(wget -q -O- 'https://registry.hub.docker.com/v2/repositories/faucet/faucet-pi/tags?page_size=1024'|jq --raw-output '."results"[]["name"]'|grep -E "^[0-9\.]+$"|sort > $TMPDIR/tags.txt)
REPOTAGS=$(git tag|grep -E "^[0-9\.]+$"|sort > $TMPDIR/repotags.txt)
MISSINGTAGS=$(diff -u $TMPDIR/tags.txt $TMPDIR/repotags.txt |grep -E "^\+[0-9]+"|sed "s/\+//g")

build_tag()
{
    tag=$1
    branch=$2
    echo "building tag $tag (branch $branch)"
    git checkout -q $branch && \
    cd docker/base && \
    $DOCKER build -t $DOCKER_ID_USER/faucet-base-pi:$tag -f Dockerfile.pi . && \
    cd ../python && \
    $DOCKER build -t $DOCKER_ID_USER/faucet-python3-pi:$tag -f Dockerfile.pi . && \
    cd ../../ && \
    $DOCKER build -t $DOCKER_ID_USER/faucet-pi:$tag -f Dockerfile.pi . && \
    $DOCKER build -t $DOCKER_ID_USER/gauge-pi:$tag -f Dockerfile.pi-gauge . && \
    $DOCKER push $DOCKER_ID_USER/faucet-base-pi:$tag && \
    $DOCKER push $DOCKER_ID_USER/faucet-python3-pi:$tag && \
    $DOCKER push $DOCKER_ID_USER/faucet-pi:$tag && \
    $DOCKER push $DOCKER_ID_USER/gauge-pi:$tag
}

# Build any tags missing from Docker Hub.
if [ "$MISSINGTAGS" != "" ] ; then
    for tag in $MISSINGTAGS ; do
	build_tag $tag $tag
    done
fi

build_tag latest master

for s in created exited ; do
    for i in `$DOCKER ps --filter status=$s -q --no-trunc` ; do
        $DOCKER rm -f $i
    done
done
for i in `$DOCKER images --filter dangling=true -q --no-trunc` ; do
    $DOCKER rmi -f $i
done

rm -rf "$TMPDIR"
