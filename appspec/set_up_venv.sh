#!/bin/bash
source "/etc/profile.d/custom-envs.sh"
if [ ! -d "$ENVDIR" ]; then
  python3 -m venv /home/ec2-user/venv
fi
chown -R ec2-user /home/ec2-user/venv
chmod 775 /home/ec2-user/venv/bin/activate