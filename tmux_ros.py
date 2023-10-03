#!/usr/bin/env python3
# coding: utf-8

###############################################################################
# tmux_ros.py
#
# Script to create a multi-window, multi-pane setup in tmux. Configured for 
# my preferences for a layout. This assumes that you are calling it from the
# root folder of a ROS workspace and already have built the workspace. It will
# still create the layout if not, but you will need to manually source ROS in
# each of the tmux panes.
#
# I put this in the /usr/local/bin directory, but it could be anywhere on your
# path (or even run from with the workspace root). I make it executable and 
# put it in /usr/local/bin so I could run it from anywhere by just typing
#
#    tmux_ros.py
#
# If you wanted it to be cleaner, you could remove the .py extension from the
# filename and just have to type tmux_ros
#
# Based on:
#    * https://github.com/CRAWlab/RoboBoat-2019/blob/master/Settings%20Files/raspi_tmux.sh
#    * https://gist.github.com/fisadev/044af2854ba38bcd6ef8
#
# Created: 08/24/23
#   - Joshua Vaughan
#   - vaughanje@ornl.gov
#   - @doc_vaughan, @doc_vaughan@mastodon.social
#   - https://userweb.ucs.louisiana.edu/~jev9637/
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import time
from os import system


def tmux(command):
    system('tmux %s' % command)


def tmux_shell(command):
    tmux('send-keys "%s" "C-m"' % command)


# Start tmux
tmux('new-session -s "main" -d')

# First window for main ROS terminals
# Layout - numbers are resulting pane number
# +---------+---------+
# |         |         |
# |    0    |    2    |
# |         |         |
# +---------+---------+
# |         |    3    |
# |    1    +---------+
# |         |    4    |
# +---------+---------+

# first column
tmux('select-window -t 0')
tmux('rename-window "main"')

# second column
tmux('split-window -h')
tmux('split-window -v')
tmux('split-window -v')

# Back to first column
tmux('select-pane -t 0')
tmux('split-window -v')

# We need a small sleep to let the windows and panes be created
time.sleep(0.05)

# Now source ROS everywhere
tmux('select-pane -t 0')
tmux_shell("source devel/setup.bash")

tmux('select-pane -t 1')
tmux_shell("source devel/setup.bash")

tmux('select-pane -t 2')
tmux_shell("source devel/setup.bash")

tmux('select-pane -t 3')
tmux_shell("source devel/setup.bash")

tmux('select-pane -t 4')
tmux_shell("source devel/setup.bash")


# Create a second window for the webui
# Layout - numbers are resulting pane number
# +---------+---------+
# |         |         |
# |         |         |
# |         |         |
# |    0    |    1    |
# |         |         |
# |         |         |
# |         |         |
# +---------+---------+
tmux('new-window')
tmux('select-window -t 1')
tmux('rename-window "GUI"')

# second column
tmux('split-window -h')
tmux('select-pane -t 0')

# Go back to the first pane in the first window
tmux('select-window -t 0')
tmux('select-pane -t 0')

# Finally, open the created session
tmux('-2 attach-session -d')
