#!/bin/bash

SES_NAME="adaq"
DAQ_DIR="~/Bram/grand-daq-master"
DATA_DIR="~/Bram/grand-data/data/"

ADAQ="$DAQ_DIR/Adaq/Adaq"
DAQgui="python3 $DAQ_DIR/gui/DAQgui.py"

# Check if session exists
tmux has-session -t $SES_NAME 2> /dev/null

# Create session if not exists
if [ $? != 0 ];
then
	cd $DAQ_DIR;
	tmux new-session -s $SES_NAME -d

	# Make sure we work in the first window
	tmux new-window -t $SES_NAME:1 -n "DAQ"
	tmux select-window -t $SES_NAME:1

	# Ping station
	tmux send-keys "ping 192.168.61.87 -c 5" Enter

	# Open DAQ gui next to it
	tmux send-keys "$DAQgui" Enter

	# Split screen
	tmux split-window -h -p 50
	tmux select-pane -t 1

	# Start Adaq
	tmux send-keys "cd $DAQ_DIR" Enter
	tmux send-keys "$ADAQ" Enter

	# Split screen
	tmux split-window -v -p 50
	tmux select-pane -t 3

	# Watch the data map
	tmux send-keys "cd $DATA_DIR" Enter
	tmux send-keys "watch -dc ls -lR cur/*/" Enter
fi

# Attach to session
tmux attach -t $SES_NAME
