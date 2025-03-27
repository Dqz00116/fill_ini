#!/usr/bin/env bash

if python3 fill_ini.py; then
    echo "Script executed successfully"
else
    echo "Script execution failed!"
    exit 1
fi

if [ -t 0 ]; then
    read -p "Press Enter to continue..."
fi