# -*- coding: utf-8 -*-
"""
数据管理模块
对应 C++ 的 DataManager.h / DataManager.cpp
负责数据的持久化存储（从文件加载和保存到文件）
"""
from metro_system.structures import Line
from metro_system import utils


class DataManager:
    """数据管理器，负责从文件加载数据和保存数据到文件"""

    def __init__(self, file_path, data):
        """
        构造函数
        :param file_path: 数据文件路径
        :param data: MetroData 数据对象（引用）
        """
        self.file_path = file_path
        self.data = data
        self.load_data()
        # 确保数据加载后通知用户
        if self.data.lines:
            utils.print_message(f"数据加载完成。已加载 {len(self.data.lines)} 条线路。")
        else:
            utils.print_error("未找到数据文件或文件为空。请检查 'data/metro_data.txt' 文件。")

    def load_data(self):
        """从文件读取数据到内存"""
        # ===== Bug #3: opne 拼写错误（模拟 C++ 的 ifstreeam）=====
        # C++ 原始代码中写了 ifstreeam 而不是 ifstream
        # Python 对应为 opne 而不是 open
        try:
            file = opne(self.file_path, 'r', encoding='utf-8')
        except Exception:
            utils.print_error(f"无法打开数据文件: {self.file_path}，你可以稍后手动创建。")
            return

        line_count = 0
        for line_str in file:
            line_count += 1
            stripped = trim(line_str)
            if not stripped:
                continue

            parts = split(stripped, ';')
            if len(parts) < 5:
                utils.print_error(f"数据格式错误 (字段少于5个) - 第 {line_count} 行，跳过该线路数据。")
                continue

            line_obj = Line()
            line_obj.name = parts[0]
            line_obj.first_train = parts[2]
            line_obj.last_train = parts[3]

            # 字符串转票价
            try:
                line_obj.full_price = float(parts[1])
            except ValueError:
                utils.print_error(f"数据格式错误 (票价非数字) - 第 {line_count} 行，跳过该线路数据。")
                continue

            # 站点列表在 parts[4] 之后
            stations_str = ""
            for i in range(4, len(parts)):
                stations_str += parts[i]
                if i < len(parts) - 1:
                    stations_str += ';'
            # 站点内部以英文逗号分隔
            line_obj.stations = split(stations_str, ',')

            if len(line_obj.stations) < 2:
                utils.print_error(f"数据格式错误 (站点少于2个) - 第 {line_count} 行，跳过该线路数据。")
                continue

            self.data.lines[line_obj.name] = line_obj

        file.close()

    def save_data(self):
        """将内存数据保存到文件"""
        try:
            file = open(self.file_path, 'w', encoding='utf-8')
        except Exception:
            utils.print_error(f"无法打开数据文件进行保存: {self.file_path}")
            return

        for line_name, line_obj in self.data.lines.items():
            stations_str = ",".join(line_obj.stations)
            file.write(f"{line_obj.name};{line_obj.full_price:.1f};"
                       f"{line_obj.first_train};{line_obj.last_train};"
                       f"{stations_str}\n")

        file.close()
        utils.print_message(f"数据已自动保存到文件: {self.file_path}")


def trim(s):
    """局部导入的 trim 函数（与 utils.trim 相同）"""
    return s.strip()


def split(s, delimiter):
    """局部导入的 split 函数（与 utils.split 相同）"""
    return [token.strip() for token in s.split(delimiter)]
