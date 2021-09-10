# -*- coding: utf-8 -*-
import json
from resource_management import *


class Master(Script):

    def install(self, env):
        import params
        env.set_params(params)

        Logger.info("安装开始")

        # 删除旧的安装文件(Nifi不存储数据)
        Execute(format("rm -rf {nifi_install_dir}"))

        # 删除残留的pid文件夹
        Execute(format("rm -rf {nifi_pid_dir}"))

        # 下载安装包
        # Execute(format("wget {nifi_download} -O nifi.tar.gz"))

        # 创建安装目录
        Execute(format("mkdir -p {nifi_install_dir}"))

        # nifi解压到指定的目录
        Execute(format("cd /root && tar -zxvf nifi.tar.gz -C {nifi_install_dir}"))

        # 删除Nifi安装包
        # Execute("rm -rf nifi.tar.gz")

        Logger.info("安装完成!")

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)

        Logger.info("配置开始")

        # 修改nifi.properties配置
        File(format("{nifi_install_dir}/conf/nifi.properties"),
             content=Template("nifi.properties.j2", configurations=params))

        # 修改state-management.xml配置
        File(format("{nifi_install_dir}/conf/state-management.xml"),
             content=Template("state-management.xml.j2", configurations=params))

        # 创建pid文件
        Directory([params.nifi_pid_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.nifi_user,
                  group=params.nifi_group,
                  create_parents=True
                  )

        # 修改nifi文件夹权限
        Execute(format("chown -R {nifi_user}:{nifi_group} {nifi_install_dir} {nifi_pid_dir}"))

        Logger.info("配置结束")

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        Logger.info("启动开始")

        # 启动前的配置
        self.configure(env)

        # 为非ambari-server节点的ambari-agent获取Java环境变量
        Execute("source /etc/profile", user=params.nifi_user)

        # Nifi启动
        Execute(format("{nifi_install_dir}/bin/nifi.sh start"), user=params.nifi_user)

        Execute(
            "ps -ef | grep " + params.nifi_install_dir + "/bin/nifi.sh | grep -v grep | awk '{print $2}' > " + params.nifi_pid_file,
            user=params.nifi_user)

        Logger.info("启动结束")

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        Logger.info("停止开始")

        # 为非ambari-server节点的ambari-agent获取Java环境变量
        Execute("source /etc/profile", user=params.nifi_user)

        # Nifi停止
        Execute(format("{nifi_install_dir}/bin/nifi.sh stop"), user=params.nifi_user)

        # Nifi的pid目录删除
        Execute(format("rm -rf {nifi_pid_dir}"))

        Logger.info("停止结束")

    def status(self, env):
        import params
        env.set_params(params)

        check_process_status(params.nifi_pid_file)

    def restart(self, env):
        import params
        env.set_params(params)

        Logger.info("重启开始")

        # 为非ambari-server节点的ambari-agent获取Java环境变量
        Execute("source /etc/profile", user=params.nifi_user)

        # Nifi的pid目录删除
        Execute(format("rm -rf {nifi_pid_dir}"))

        # 创建pid文件
        Directory([params.nifi_pid_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.nifi_user,
                  group=params.nifi_group,
                  create_parents=True
                  )

        # Nifi重启
        Execute(format("{nifi_install_dir}/bin/nifi.sh restart"), user=params.nifi_user)

        Execute(
            "ps -ef | grep " + params.nifi_install_dir + "/bin/nifi.sh | grep -v grep | awk '{print $2}' > " + params.nifi_pid_file,
            user=params.nifi_user)

        Logger.info("重启结束")

    def alone_to_cluster(self, env):
        import params
        env.set_params(params)

        Logger.info("单机转集群开始")

        self.stop(env)

        self.configure(env)

        self.start(env)

        Logger.info("单机转集群完成")

    def cluster_to_alone(self, env):
        import alone
        env.set_params(alone)

        Logger.info("集群转单机开始")

        # 为非ambari-server节点的ambari-agent获取Java环境变量
        Execute("source /etc/profile", user=alone.nifi_user)

        # Nifi停止
        Execute(format("{nifi_install_dir}/bin/nifi.sh stop"), user=alone.nifi_user)

        # Nifi的pid目录删除
        Execute(format("rm -rf {nifi_pid_dir}"))

        # 修改nifi.properties配置
        File(format("{nifi_install_dir}/conf/nifi.properties"),
             content=Template("nifi.properties.j2", configurations=alone))

        # 修改state-management.xml配置
        File(format("{nifi_install_dir}/conf/state-management.xml"),
             content=Template("state-management.xml.j2", configurations=alone))

        # 创建pid文件
        Directory([alone.nifi_pid_dir],
                  mode=0755,
                  cd_access='a',
                  owner=alone.nifi_user,
                  group=alone.nifi_group,
                  create_parents=True
                  )

        # 修改nifi文件夹权限
        Execute(format("chown -R {nifi_user}:{nifi_group} {nifi_install_dir} {nifi_pid_dir}"))

        # 为非ambari-server节点的ambari-agent获取Java环境变量
        Execute("source /etc/profile", user=alone.nifi_user)

        # Nifi启动
        Execute(format("{nifi_install_dir}/bin/nifi.sh start"), user=alone.nifi_user)

        Execute(
            "ps -ef | grep " + alone.nifi_install_dir + "/bin/nifi.sh | grep -v grep | awk '{print $2}' > " + alone.nifi_pid_file,
            user=alone.nifi_user)

        Logger.info("集群转单机结束")


if __name__ == "__main__":
    Master().execute()
