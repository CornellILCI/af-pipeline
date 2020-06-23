#!/bin/bash


if [ ! -d "/var/run/munge" ]; then
        mkdir -p /var/run/munge
        chown -R munge:munge /var/run/munge
fi

if [ ! -d "/var/spool/slurmd" ]; then
        mkdir -p /var/spool/slurmd
        chown -R  slurm:slurm /var/spool/slurmd
fi

if [ ! -d "/var/run/slurm-llnl" ]; then
        mkdir -p /var/run/slurm-llnl
        chown -R slurm:slurm /var/run/slurm-llnl
fi




#chown slurm:slurm /var/spool/slurmd /var/run/slurmd /var/lib/slurmd /var/log/slurm

echo "- Starting all Slurm processes under supervisord"
/usr/bin/supervisord --configuration /etc/supervisord.conf

exec "$@"
