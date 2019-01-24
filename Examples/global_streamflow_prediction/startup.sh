#!/bin/bash
cd /lf
./Microsoft.LocalForwarder.ConsoleHost noninteractive &
python /app/fuse/file_mounter.py
/usr/bin/supervisord