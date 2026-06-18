#!/bin/bash

# 安装依赖
sudo apt update
sudo apt install -y curl wget uuid-runtime

# 安装 V2Ray
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh) --version v5.49.0

# 启用 BBR
sudo tee /etc/sysctl.conf <<-'EOF' > /dev/null
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_fastopen = 3
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_moderate_rcvbuf = 1
net.core.somaxconn = 65535
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_timestamps = 1
EOF
sudo sysctl -p

# 配置 V2Ray
sudo mkdir -p /usr/local/etc/v2ray
PORT=18524
UUID=7047f6fb-24fd-4d20-bfc2-85c78a520eee

# 生成配置文件
sudo cat <<EOF | sudo tee /usr/local/etc/v2ray/config.json
{
  "inbounds": [
  {
    "port": $PORT,
    "protocol": "vmess",
    "settings": {
      "clients": [{
        "id": "$UUID",
        "alterId": 0
      }]
    },
    "streamSettings": {
      "network": "tcp"
      // 伪装成普通网页TCP流量，混淆特征，不设置即不伪装，性能最好，当裸奔容易被发现
      // "tcpSettings": {
      //     "header": {
      //       "type": "http"
      //     }
      // }
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  }]
}
EOF

# 启动服务
sudo systemctl start v2ray
sudo systemctl enable v2ray

echo "安装完成！"
echo "V2Ray 端口: $PORT"
echo "UUID: $UUID"
