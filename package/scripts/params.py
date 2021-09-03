# -*- coding: utf-8 -*-
from resource_management import *

config = Script.get_config()

# 获取nifi-env.xml中的nifi_user用户变量
nifi_user = config['configurations']['nifi-env']['nifi_user']

# 获取nifi-env.xml中的nifi_group用户组变量
nifi_group = config['configurations']['nifi-env']['nifi_group']

# 获取nifi-env.xml中的nifi安装路径
nifi_install_dir = config['configurations']['nifi-env']['nifi_dir']

# 获取nifi-env.xml的Nifi pid文件夹
nifi_pid_dir = config['configurations']['nifi-env']['nifi_pid_dir']

# 获取nifi-env.xml的Nifi pid文件
nifi_pid_file = format("{nifi_pid_dir}/nifi.pid")

# 获取nifi的服务端口
server_port = config['configurations']['nifi-config']['server_port']

# 获取nifi集群协议端口
node_port = config['configurations']['nifi-config']['node_port']

# 获取nifi集群平衡端口
balance_port = config['configurations']['nifi-config']['balance_port']

# 是否是集群节点
cluster_node = "true"

# 获取本机主机名称
host = config['agentLevelParams']['hostname']

# 获取zookeeper集群列表
zk_server_list = config['clusterHostInfo']['zookeeper_server_hosts']

# 获取zookeeper集群端口
zk_port = config['configurations']['zoo.cfg']['clientPort']

# 拼接zookeeper集群地址
zk_list = ""
for zk in zk_server_list:
    zk_list = format("{zk_list}{zk}:{zk_port},")

if zk_list is not None:
    zk_list = zk_list[:-1]

# 获取nifi的下载文件路径
if config.get('repositoryFile'):
    baseUrl = config['repositoryFile']['repositories'][0]['baseUrl']
    nifi_download = format("{baseUrl}/nifi/nifi-1.9.2-bin.tar.gz")
