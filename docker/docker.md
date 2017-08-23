## Install instructions on Ubuntu

https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository


Error:
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.30/containers/create: dial unix /var/run/docker.sock: connect: permission denied.

https://undebugable.wordpress.com/2017/04/10/docker-run-docker-without-sudo/

Installing Influx
http://davidanguita.name/articles/simple-data-visualization-stack-with-docker-influxdb-and-grafana/

## Operation

Get IPs
docker inspect grafana  | grep '"IPAddress"' | head -n 1 (172.17.0.3)
docker inspect influxdb  | grep '"IPAddress"' | head -n 1 (172.17.0.2)





