SYSTEMD_SCRIPT_DIR=$( cd  $(dirname "${BASH_SOURCE:=$0}") && pwd)
cp -f "$SYSTEMD_SCRIPT_DIR/noolite_mtrf_mqtt.service" /lib/systemd/system
chown root:root /lib/systemd/system/noolite_mtrf_mqtt.service

systemctl daemon-reload
systemctl enable noolite_mtrf_mqtt.service