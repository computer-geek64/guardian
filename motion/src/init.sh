#!/bin/sh
# init.sh

./populate_configs.py
motion -n -c /etc/motion/motion.conf
