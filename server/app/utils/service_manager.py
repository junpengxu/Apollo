import time

from random import choice
from redis import StrictRedis

from app.utils.Singleton import singleton


class NoValidNodeError(OSError):
    pass


class NodeExistError(OSError):
    pass


@singleton
class ServiceManager:
    def __init__(self, host="localhost", post=3367, db=0):
        self.cli = StrictRedis(decode_responses=True)
        self.__node_keys = "services_registe_keys"
        self.__lock_key = "service_manage_lock"
        self.__lock_expire_time = 2
        self.__node_alive_time = 3  # 默认存活时间
        self.__operate_expire_time = 1  # 1s足够很多redis操作
        self.__LOCK = "1"
        self.__UNLOCK = "0"
        self.__acquir_lock_interval = 0.01
        self.__listen_interval = 1

    def __acquir_lock(self):
        # 每一步锁的操作都有return 返回, 如果不return， 会按照默认的None，当False 处理
        # 没有获取到锁，就创建
        st = time.time()
        while True:
            if self.cli.get(self.__lock_key) is None:
                self.cli.setex(self.__lock_key, self.__lock_expire_time, self.__LOCK)
                return True
            # 锁被持有
            elif self.cli.get(self.__lock_key) == self.__LOCK:
                time.sleep(self.__acquir_lock_interval)
            # 获取到锁就更新时间并且修改锁的状态或者删除掉锁
            elif self.cli.get(self.__lock_key) == self.__UNLOCK:
                self.cli.setex(self.__lock_key, self.__lock_expire_time, self.__LOCK)
                return True
            elif time.time() - st > self.__operate_expire_time:
                raise TimeoutError

    def __release_lock(self):
        # 0 代表锁被释放
        self.cli.setex(self.__lock_key, self.__lock_expire_time, self.__UNLOCK)

    def __get_service_node(self):
        if self.__acquir_lock():
            nodes = self.cli.smembers(self.__node_keys)
            if not nodes:
                self.__release_lock()
                raise NoValidNodeError
            # node = self.cli.srandmember(self.__node_keys)  # 并非真随机
            node_info = self.cli.hgetall(choice(list(nodes)))
            if not node_info or self.__node_expire(node_info):
                # 节点信息不一致, 删除多余节点
                self.__remove_service_node(node_info=node_info)
            self.__release_lock()
            return node_info

    def __add_service_node(self, node_info):

        node_name = node_info["node_name"]
        if self.__acquir_lock():
            # if self.cli.hkeys(node_name):
            #     self.__release_lock()
            #     # 如果存在, 是否要覆盖, 执行覆盖逻辑
            #     raise NodeExistError
            self.cli.sadd(self.__node_keys, node_name)
            for key, val in node_info.items():
                self.cli.hset(name=node_name, key=key, value=val)
            self.__release_lock()

    def __remove_service_node(self, node_name):
        try:
            self.cli.srem(self.__node_keys, node_name)
            self.cli.delete(node_name)
            return True
        except Exception as e:
            print("删除节点失败", e)
            return False

    def __get_all_node_keys(self):
        return self.cli.smembers(self.__node_keys) or []

    def __get_node_info_by_node_name(self, node_name):
        return self.cli.hgetall(node_name)

    def __node_expire(self, node_info):
        """
        判断node是否已经过期
        :param node_info:
        :return: True: 过期, False: 未过期
        """
        if time.time() - float(node_info["node_register_time"]) > self.__node_alive_time:
            return True
        return False

    def __service_listen(self):
        while True:
            for node_name in self.__get_all_node_keys():
                node_info = self.__get_node_info_by_node_name(node_name)
                if self.__node_expire(node_info):
                    try:
                        if self.__acquir_lock():
                            print("删除节点:{}".format(node_info))
                            self.__remove_service_node(node_info)
                    except:
                        print("未获取到锁，删除节点失败")
                        pass
            else:
                time.sleep(self.__listen_interval)

    def service_register(self, node):
        print("开始注册")
        try:
            self.__add_service_node(node)
            return True
        except Exception as e:
            print("注册失败")
            return False

    def service_destroy(self, node_name):
        return self.__remove_service_node(node_name)

    def get_all_service(self):
        result = []
        node_names = self.__get_all_node_keys()
        for node_name in node_names:
            result.append(self.__get_node_info_by_node_name(node_name))
        return result

    def exit(self):
        self.cli.flushall()


if __name__ == '__main__':
    sm = ServiceManager()
    sm.get_all_service()
    node1_info = {
        "node_name": "node_name1",
        "node_host": "node_host1",
        "node_port": 80,
        "node_register_time": time.time()
    }
    node2_info = {
        "node_name": "node_name2",
        "node_host": "node_host2",
        "node_port": 80,
        "node_register_time": time.time()
    }
    node3_info = {
        "node_name": "node_name3",
        "node_host": "node_host3",
        "node_port": 80,
        "node_register_time": time.time()
    }
    node4_info = {
        "node_name": "node_name4",
        "node_host": "node_host4",
        "node_port": 80,
        "node_register_time": time.time()
    }
    sm.service_register(node1_info)
    sm.service_register(node2_info)
    sm.service_register(node3_info)
    sm.service_register(node4_info)
    node1_cnt = 0
    node2_cnt = 0
    node3_cnt = 0
    node4_cnt = 0
    for i in range(10000):
        res = sm.service_destroy()
        if res["node_host"] == "node_host1":
            node1_cnt += 1
        elif res["node_host"] == "node_host2":
            node2_cnt += 1
        elif res["node_host"] == "node_host3":
            node3_cnt += 1
        else:
            node4_cnt += 1
    print(node1_cnt, node2_cnt, node3_cnt, node4_cnt)
    sm.exit()
