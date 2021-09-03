# -*- coding: utf-8 -*-
from resource_management import *

config = Script.get_config()

# 获取nifi-env.xml中的nifi_user用户变量
nifi_user = config['configurations']['nifi-env']['nifi_user']

# 获取nifi-env.xml中的nifi_group用户组变量
nifi_group = config['configurations']['nifi-env']['nifi_group']

# 获取nifi-env.xml的Nifi pid文件夹
nifi_pid_dir = config['configurations']['nifi-env']['nifi_pid_dir']

# 获取nifi-env.xml的Nifi pid文件
nifi_pid_file = format("{nifi_pid_dir}/nifi.pid")

# 获取nifi的服务端口
server_port = config['configurations']['nifi-config']['server_port']

# 获取nifi集群协议端口
node_port = ""

# 是否是集群节点
cluster_node = "false"

# 获取本机主机名称
host = config['agentLevelParams']['hostname']

# 拼接zookeeper集群地址
zk_list = ""
