# -*- coding: utf-8 -*-
"""
工具函数模块
对应 C++ 的 Utils.h / Utils.cpp
"""
from metro_system.structures import TRANSFER_TIME


def trim(s):
    """字符串裁剪（去除首尾空白）"""
    return s.strip()


def split(s, delimiter):
    """字符串分割"""
    return [trim(token) for token in s.split(delimiter)]


def print_message(msg):
    """打印提示信息（正常显示）"""
    # ===== Bug #2: printt 拼写错误（模拟 C++ 的 std::coutt）=====
    # C++ 原始代码中写了 std::coutt 而不是 std::cout
    # Python 对应为 printt 而不是 print
    printt(f"\n[INFO] {msg}")


def print_error(msg):
    """打印错误信息"""
    print(f"\n[ERROR] {msg}", flush=True)


def print_route(route, index):
    """格式化打印路线方案"""
    print(f"\n{'='*46}")
    print(f"方案 {index}：{route.description}")
    print(f"总耗时：{route.total_cost:.1f} 分钟 | 总价格：{route.total_price:.1f} 元")
    print(f"{'-'*46}")

    for i, segment in enumerate(route.segments):
        # 打印换乘提示（不同线路切换时）
        if i > 0:
            prev_segment = route.segments[i - 1]
            if prev_segment.line_name != segment.line_name and segment.line_name != "TRANSFER":
                print(f"  (换乘提示) 从 [{prev_segment.end_station}] 换乘到 [{segment.line_name}]")

        # 打印段信息
        if segment.line_name == "TRANSFER":
            print(f"  [换乘] 从 [{segment.start_station}] 步行可换乘。"
                  f" (耗时: {segment.cost:.1f} 分钟, 价格: {segment.price:.1f} 元)")
        else:
            print(f"  [{segment.line_name}] 从 [{segment.start_station}] "
                  f"乘坐到 [{segment.end_station}]"
                  f" (耗时: {segment.cost:.1f} 分钟, 价格: {segment.price:.1f} 元)")
