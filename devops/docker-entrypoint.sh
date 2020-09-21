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

echo "- Starting gunicorn -"

cp /config/simba.conf /home/aadmin/ebs-af/aeo/conf/simba.conf

exec gunicorn -w 2 -b 0.0.0.0:80 --log-file /var/log/gunicorn.log --chdir /home/aadmin/ebs-af/api/v1 wsgi:app
exec "$@"
