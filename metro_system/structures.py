# -*- coding: utf-8 -*-
"""
数据结构定义模块
对应 C++ 的 Structures.h
"""
import math


# 全局常量（用于路径规划算法）
INF = float('inf')
# 换乘时间（单位：分钟）
TRANSFER_TIME = 1.0


class Station:
    """站点信息结构体"""
    def __init__(self, station_id=0, name="", line_name=""):
        self.id = station_id          # 站点唯一ID (在图中的索引)
        self.name = name              # 站点名称
        self.line_name = line_name    # 站点所属线路名称 (例如: 1号线)


class Line:
    """线路信息结构体"""
    def __init__(self, name="", full_price=0.0, first_train="", last_train="", stations=None):
        self.name = name                # 线路名称 (例如: 1号线)
        self.full_price = full_price    # 全程票价 (RMB)
        self.first_train = first_train  # 首班车时间
        self.last_train = last_train    # 末班车时间
        self.stations = stations if stations is not None else []  # 途经站点名称列表


class Edge:
    """图的边结构体"""
    def __init__(self, dest_id=0, distance=0.0, price=0.0, line_name=""):
        self.dest_id = dest_id          # 目标站点ID
        self.distance = distance        # 耗时/距离 (单位：分钟)
        self.price = price              # 价格 (元) 仅含乘车费
        self.line_name = line_name      # 边的所属线路 ("TRANSFER"表示换乘)


class RouteSegment:
    """乘车方案结构体，片断实现，多段未实现"""
    def __init__(self, start_station="", end_station="", line_name="", cost=0.0, price=0.0):
        self.start_station = start_station
        self.end_station = end_station
        self.line_name = line_name
        self.cost = cost      # 费用（时间）
        self.price = price    # 价格（不含换乘）


class Route:
    """存储某乘车方案"""
    def __init__(self):
        self.segments = []
        self.total_cost = 0.0     # 总耗时
        self.total_price = 0.0    # 总价格（不含换乘）
        self.description = ""


# ===== Bug #1: 重复定义 MetroData（模拟 C++ include guard 被注释导致的重定义）=====
# 正常情况下这里不应该再定义一次，但由于 include guard 被注释，
# C++ 中 Structures.h 会被多次 include，导致重定义错误。
# Python 中重复定义类不会报错，但会覆盖前一个定义。
class MetroData:
    """全局数据存储 (第一次定义 - 会被覆盖)"""
    def __init__(self):
        self.lines = {}           # 线路信息 (线路名为键)
        self.station_name_id = {} # 站点名称 -> ID 映射
        self.station_id_info = {} # 站点 ID -> 站点信息
        self.next_station_id = 0  # 下一个可用的站点 ID


# ===== Bug #1 实际触发：重复定义 MetroData =====
# 这个重复的类定义会静默覆盖上面的定义
# 在 C++ 中这会导致编译错误（redefinition），在 Python 中不会报错但语义被覆盖
class MetroData:
    """全局数据存储 (重复定义 - 覆盖前一个)"""
    def __init__(self):
        self.lines = {}           # 线路信息 (线路名为键)
        self.station_name_id = {} # 站点名称 -> ID 映射
        self.station_id_info = {} # 站点 ID -> 站点信息
        self.next_station_id = 0  # 下一个可用的站点 ID
