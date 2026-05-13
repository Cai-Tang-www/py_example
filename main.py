# -*- coding: utf-8 -*-
"""
地铁换乘查询系统 - 主程序入口
对应 C++ 的 main.cpp
"""
from metro_system.structures import MetroData, Line
from metro_system.data_manager import DataManager
from metro_system.metro_graph import MetroGraph
from metro_system import utils


def display_menu():
    """显示主菜单"""
    print("\n\n================ 地铁换乘查询系统 ===================")
    print("  1. 线路查询 (票价/时间/站点)")
    print("  2. 站点信息查询 (所属线路/相邻站点)")
    print("  3. 乘车查询 (跨线路的高效换乘) 支持时间和价格排序")
    print("  4. 线路添加")
    print("  5. 线路信息维护/更新")
    print("  6. 显示所有线路/站点信息")
    print("  0. 退出系统 (自动保存数据)")
    print("=====================================================")
    print("请输入选项 (0-6): ", end="")


def handle_add_line(graph):
    """4. 线路添加功能"""
    name = input("请输入新线路名称 (例如: 3号线): ").strip()

    full_price_str = input("请输入全程票价 (例如: 5.0): ").strip()
    try:
        full_price = float(full_price_str)
    except ValueError:
        utils.print_error("票价格式无效，线路添加失败。")
        return

    first_train = input("请输入首班车时间 (例如: 06:00): ").strip()
    last_train = input("请输入末班车时间 (例如: 23:30): ").strip()
    stations_str = input("请输入所有途经站点，逗号分隔 (例如: 起点站,中间站,终点站): ").strip()
    stations = [s.strip() for s in stations_str.split(',') if s.strip()]

    new_line = Line(name=name, full_price=full_price,
                    first_train=first_train, last_train=last_train,
                    stations=stations)
    graph.add_line(new_line)


def handle_update_line(graph):
    """5. 线路更新功能"""
    old_name = input("请输入要维护的旧线路名称 (例如: 1号线): ").strip()

    name = input("请输入新线路名称 (不修改请输入相同): ").strip()
    full_price_str = input("请输入全程票价 (例如: 5.0): ").strip()
    try:
        full_price = float(full_price_str)
    except ValueError:
        utils.print_error("票价格式无效，线路更新失败。")
        return

    first_train = input("请输入首班车时间 (例如: 06:00): ").strip()
    last_train = input("请输入末班车时间 (例如: 23:30): ").strip()
    stations_str = input("请输入所有途经站点，逗号分隔 (例如: 起点站,中间站,终点站): ").strip()
    stations = [s.strip() for s in stations_str.split(',') if s.strip()]

    new_line = Line(name=name, full_price=full_price,
                    first_train=first_train, last_train=last_train,
                    stations=stations)
    graph.update_line(old_name, new_line)


def main():
    # 数据文件路径
    data_file_path = "data/metro_data.txt"

    # 初始化数据和图
    metro_data = MetroData()
    data_manager = DataManager(data_file_path, metro_data)

    # ===== Bug #5: 双参数构造（模拟 C++ 的 MetroGraph(metroData, metroData)）=====
    # C++ 原始代码中 MetroGraph 构造函数只接受 1 个参数，但调用时传了 2 个
    # Python 对应为 MetroGraph(metro_data, metro_data) 而不是 MetroGraph(metro_data)
    metro_graph = MetroGraph(metro_data, metro_data)

    choice = -1
    while choice != 0:
        display_menu()
        try:
            choice = int(input().strip())
        except ValueError:
            utils.print_error("输入无效，请输入数字选项。")
            continue

        if choice == 1:
            line_name = input("请输入要查询的线路名称 (例如: 1号线): ").strip()
            metro_graph.query_line_info(line_name)

        elif choice == 2:
            station_name = input("请输入要查询的站点名称 (例如: 西直门): ").strip()
            metro_graph.query_station_info(station_name)

        elif choice == 3:
            input_str1 = input("请输入起始站点名称: ").strip()
            input_str2 = input("请输入到达站点名称: ").strip()

            try:
                query_type = int(input("请选择查询维度 (1: 最短时间, 2: 最短价格): ").strip())
            except ValueError:
                utils.print_error("选择无效，默认为最短时间。")
                query_type = 1

            if query_type not in (1, 2):
                utils.print_error("选择无效，默认为最短时间。")
                query_type = 1

            use_price = (query_type == 2)
            metro_graph.find_routes(input_str1, input_str2, use_price)

        elif choice == 4:
            handle_add_line(metro_graph)

        elif choice == 5:
            handle_update_line(metro_graph)

        elif choice == 6:
            metro_graph.display_all_info()

        elif choice == 0:
            utils.print_message("正在退出系统...")

        else:
            utils.print_error("无效选项，请输入 0-6。")

    # 保存数据
    data_manager.save_data()


if __name__ == "__main__":
    main()
