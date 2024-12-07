#!/bin/bash
script_dir="$(dirname "$0")"

if grep -q nfs /proc/mounts; then
    rsync -ahv ${script_dir}/photo/ /mnt/nfs/photo/
    rsync -ahv ${script_dir}/video/ /mnt/nfs/video/
fi
