#!/bin/bash

# 安装依赖
sudo apt update
sudo apt install -y curl wget uuid-runtime

# 安装 V2Ray
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)

# 启用 BBR
sudo tee /etc/sysctl.conf <<-'EOF' > /dev/null
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF
sudo sysctl -p

# 配置 V2Ray
sudo mkdir -p /usr/local/etc/v2ray
PORT=18524
UUID=$(uuidgen)

# 生成配置文件
sudo cat <<EOF | sudo tee /usr/local/etc/v2ray/config.json
{
  "inbounds": [{
    "port": $PORT,
    "protocol": "vmess",
    "settings": {
      "clients": [{
        "id": "$UUID",
        "alterId": 64
      }]
    },
    "streamSettings": {
      "network": "tcp"
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
