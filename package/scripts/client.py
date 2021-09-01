#!/usr/bin/env python
# -*- coding: utf-8 -*--

from resource_management import *


# 该client只是一个示例，为了讲解如何实现 “Download Client Configs” 配置文件。无实际逻辑，可自由扩展
class Client(Script):
    def install(self, env):
        Logger.info("Install complete")
        self.configure(env)

    def configure(self, env):
        Logger.info("Configuration complete")

    def status(self, env):
        raise ClientComponentHasNoStatus()


if __name__ == "__main__":
    Client().execute()
