#docker run -d -p 3000:3000 \
#    -v /var/lib/grafana:/var/lib/grafana \
#    -e "GF_SECURITY_ADMIN_PASSWORD=sc2015" \
#    grafana/grafana


# create /var/lib/grafana as persistent volume storage
#docker run -d -v /var/lib/grafana --name grafana-storage busybox:latest

# start grafana
#docker run \
#  -d \
#  -p 3000:3000 \
#  --name=grafana \
#  --volumes-from grafana-storage \
#  grafana/grafana

docker start influxdb
docker start grafana

docker inspect grafana  | grep '"IPAddress"' | head -n 1
docker inspect influxdb  | grep '"IPAddress"' | head -n 1

