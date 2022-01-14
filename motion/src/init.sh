#!/bin/sh
# init.sh

sed -i "s#{{USERNAME}}#${MOTION_USERNAME}#;s#{{PASSWORD}}#${MOTION_PASSWORD}#;s#{{IFTTT_WEBHOOK}}#${IFTTT_WEBHOOK}#" /etc/motion/motion.conf /etc/motion/conf.d/backyard_camera.conf
motion -n -c /etc/motion/motion.conf
