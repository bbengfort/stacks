#!/bin/bash

# turn on bash's job control
set -m

# run the API server in the background
stacks serve -a 0.0.0.0:5000 &

# edit the port in the nginx config
sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf

# Run nginx and leave it running
nginx -g 'daemon off;'