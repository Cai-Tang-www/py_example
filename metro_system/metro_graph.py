# -*- coding: utf-8 -*-
"""
地铁图算法模块
对应 C++ 的 MetroGraph.h / MetroGraph.cpp
使用图结构（邻接表）存储地铁网络，实现换乘查询算法
"""
import heapq
from collections import defaultdict

from metro_system.structures import (
    INF, TRANSFER_TIME, Station, Edge, Route, RouteSegment
)
from metro_system import utils


class MetroGraph:
    """地铁图类，使用邻接表存储地铁网络"""

    def __init__(self, data):
        """
        构造函数
        :param data: MetroData 数据对象（引用）
        """
        self.data = data
        self.adj_list = []  # 图的邻接表
        self.build_graph()

    def build_graph(self):
        """根据当前 MetroData 数据更新构建邻接表"""
        # 1. 注册所有站点和分配站点 ID
        self.data.station_name_id.clear()
        self.data.station_id_info.clear()
        self.data.next_station_id = 0

        for line_name, line_obj in self.data.lines.items():
            for station_name in line_obj.stations:
                if station_name not in self.data.station_name_id:
                    new_station = Station(
                        station_id=self.data.next_station_id,
                        name=station_name,
                        line_name=line_obj.name
                    )
                    self.data.station_name_id[station_name] = new_station.id
                    self.data.station_id_info[new_station.id] = new_station
                    self.data.next_station_id += 1

        # 2. 初始化邻接表，构建乘车边
        self.adj_list = [[] for _ in range(self.data.next_station_id)]
        for line_name, line_obj in self.data.lines.items():
            self._process_line_for_graph(line_obj)

        # 3. 添加换乘边
        name_to_ids = defaultdict(list)
        for station_id, station_info in self.data.station_id_info.items():
            name_to_ids[station_info.name].append(station_id)

        for name, ids in name_to_ids.items():
            # 只有站点名称对应多个ID时才是换乘站
            if len(ids) > 1:
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        u = ids[i]
                        v = ids[j]
                        self.adj_list[u].append(Edge(v, TRANSFER_TIME, 0.0, "TRANSFER"))
                        self.adj_list[v].append(Edge(u, TRANSFER_TIME, 0.0, "TRANSFER"))

    def _process_line_for_graph(self, line_obj):
        """私有辅助函数，处理某条线路信息到图（站点和边）"""
        if len(line_obj.stations) < 2:
            return

        # 计算每站的分摊价格
        num_segments = len(line_obj.stations) - 1
        segment_price = line_obj.full_price / num_segments if num_segments > 0 else 0.0

        # 遍历站点列表，构建双方向边（默认每站间耗时 2.0 分钟）
        for i in range(len(line_obj.stations) - 1):
            u_id = self.data.station_name_id[line_obj.stations[i]]
            v_id = self.data.station_name_id[line_obj.stations[i + 1]]

            # ===== Bug #4: uuId 变量名拼写错误（模拟 C++ 的 uuId 拼写错误）=====
            # C++ 原始代码中写了 adjList[uuId] 而不是 adjList[uId]
            # Python 对应为 self.adj_list[uuId] 而不是 self.adj_list[u_id]
            self.adj_list[uuId].append(Edge(v_id, 2.0, segment_price, line_obj.name))
            # v -> u
            self.adj_list[v_id].append(Edge(u_id, 2.0, segment_price, line_obj.name))

    # =====================================================
    # 1. 线路信息查询
    # =====================================================
    def query_line_info(self, line_name):
        """查询某条线路的所有信息"""
        if line_name not in self.data.lines:
            utils.print_error(f"线路 [{line_name}] 不存在。")
            return

        line_obj = self.data.lines[line_name]
        print(f"\n{'='*20} 线路 [{line_name}] 信息 {'='*20}")
        print(f"  - 全票价: {line_obj.full_price:.1f} 元")
        print(f"  - 首班车: {line_obj.first_train}")
        print(f"  - 末班车: {line_obj.last_train}")
        print(f"  - 站点数量: {len(line_obj.stations)} 站")
        print(f"  - 途经站名: ", end="")
        print(" -> ".join(line_obj.stations))
        print(f"{'='*55}")

    # =====================================================
    # 2. 站点信息查询
    # =====================================================
    def query_station_info(self, station_name):
        """显示站点的所属线路、相邻站点等信息"""
        if station_name not in self.data.station_name_id:
            utils.print_error(f"站点 [{station_name}] 不存在。")
            return

        print(f"\n{'='*20} 站点 [{station_name}] 信息 {'='*20}")

        # 收集所有同名 ID（用于换乘站判断）
        name_to_ids = defaultdict(list)
        for sid, sinfo in self.data.station_id_info.items():
            name_to_ids[sinfo.name].append(sid)

        if station_name not in name_to_ids:
            return

        station_ids = name_to_ids[station_name]

        # 统计所属线路
        lines = set()
        for sid in station_ids:
            lines.add(self.data.station_id_info[sid].line_name)

        print(f"  - 所属线路: {', '.join(sorted(lines))}")
        print(f"  - 是否为换乘站: {'是' if len(station_ids) > 1 else '否'}")

        print(f"  - 相邻站点信息 (按乘车方向):")
        neighbors = set()
        for uid in station_ids:
            for edge in self.adj_list[uid]:
                # 排除换乘边，只统计同线乘车
                if edge.line_name != "TRANSFER":
                    neighbor_name = self.data.station_id_info[edge.dest_id].name
                    if neighbor_name not in neighbors:
                        print(f"    - 站点 [{neighbor_name}] 经线路 [{edge.line_name}]")
                        neighbors.add(neighbor_name)

        if not neighbors:
            print(f"    - 无相邻乘车站点。")

        print(f"{'='*55}")

    # =====================================================
    # 4. 线路添加
    # =====================================================
    def add_line(self, new_line):
        """添加新线路"""
        if new_line.name in self.data.lines:
            utils.print_error(f"线路 [{new_line.name}] 已存在，请使用维护功能。")
            return False
        if len(new_line.stations) < 2:
            utils.print_error(f"新建线路 [{new_line.name}] 站点数量不足2个。")
            return False

        self.data.lines[new_line.name] = new_line
        self.build_graph()

        utils.print_message(f"线路 [{new_line.name}] 已成功添加，稍后乘车程序保存数据。")
        return True

    # =====================================================
    # 5. 线路信息维护/更新
    # =====================================================
    def update_line(self, old_line_name, new_line):
        """更新线路信息"""
        if old_line_name not in self.data.lines:
            utils.print_error(f"原线路 [{old_line_name}] 不存在，无法更新。")
            return False
        if len(new_line.stations) < 2:
            utils.print_error(f"新线路 [{new_line.name}] 站点数量不足2个，更新失败。")
            return False

        # 移除旧线路
        del self.data.lines[old_line_name]
        # 添加新线路 (名称可替换)
        self.data.lines[new_line.name] = new_line
        # 重建图（线路、站点和边）
        self.build_graph()

        utils.print_message(f"线路 [{old_line_name}] 已成功更新为 [{new_line.name}]，稍后乘车程序保存数据。")
        return True

    # =====================================================
    # 6. 显示所有线路/站点信息
    # =====================================================
    def display_all_info(self):
        """显示所有线路和站点信息"""
        print(f"\n{'='*20} 系统总览 {'='*20}")
        print(f"共线路数: {len(self.data.lines)}, 总站点数: {len(self.data.station_name_id)}")

        print(f"\n--- 所有线路信息 ---")
        for line_name, line_obj in self.data.lines.items():
            print(f"[{line_obj.name}] 票价:{line_obj.full_price:.1f} 元 | 站点: {len(line_obj.stations)}站")
            print(f"  途经: ", end="")
            print(" -> ".join(line_obj.stations))
        print(f"{'='*50}")

    # =====================================================
    # Dijkstra 最短路径算法
    # =====================================================
    def _dijkstra(self, start_id, end_id, use_price):
        """
        Dijkstra 最短路径算法
        :param start_id: 起点ID
        :param end_id: 终点ID
        :param use_price: True=按价格, False=按时间
        :return: (路径ID列表, 结果字典)
        """
        results = {i: INF for i in range(self.data.next_station_id)}
        predecessors = {i: -1 for i in range(self.data.next_station_id)}

        results[start_id] = 0.0
        pq = [(0.0, start_id)]

        while pq:
            d, u = heapq.heappop(pq)

            if d > results[u]:
                continue
            if u == end_id:
                break

            for edge in self.adj_list[u]:
                v = edge.dest_id
                weight = edge.price if use_price else edge.distance

                if results[u] + weight < results[v]:
                    results[v] = results[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (results[v], v))

        # 路径回溯
        path = []
        current = end_id
        while current != -1:
            path.append(current)
            if current == start_id:
                break
            current = predecessors[current]
        path.reverse()

        if not path or path[0] != start_id:
            return [], results

        return path, results

    # =====================================================
    # 路径ID转Route结构
    # =====================================================
    def _path_id_to_route(self, path_ids, total_cost, total_price):
        """将ID路径转换为Route结构（同时记录时间和价格）"""
        route = Route()
        route.total_cost = total_cost
        route.total_price = total_price
        summary = ""

        if len(path_ids) < 2:
            return route

        current_line_name = ""
        current_segment_start_id = path_ids[0]
        current_segment_time = 0.0
        current_segment_price = 0.0

        for i in range(len(path_ids) - 1):
            u = path_ids[i]
            v = path_ids[i + 1]

            # 查找边信息
            edge_found = False
            for edge in self.adj_list[u]:
                if edge.dest_id == v:
                    edge_found = True
                    next_line_name = edge.line_name

                    # 1. 遇到换乘或者线路切换
                    if (next_line_name == "TRANSFER" or
                        (current_line_name != "" and next_line_name != current_line_name)):

                        # 保存前一段的乘车段
                        if current_line_name != "":
                            line_sum = (f"{self.data.station_id_info[current_segment_start_id].name}"
                                        f" -> ({current_line_name}) -> "
                                        f"{self.data.station_id_info[u].name}")
                            summary += ("" if not summary else " -> ") + line_sum

                            route.segments.append(RouteSegment(
                                self.data.station_id_info[current_segment_start_id].name,
                                self.data.station_id_info[u].name,
                                current_line_name,
                                current_segment_time,
                                current_segment_price
                            ))

                        # 处理换乘
                        if next_line_name == "TRANSFER":
                            route.segments.append(RouteSegment(
                                self.data.station_id_info[u].name,
                                self.data.station_id_info[u].name,
                                "TRANSFER",
                                TRANSFER_TIME,
                                0.0
                            ))
                            current_segment_start_id = v
                            current_segment_time = 0.0
                            current_segment_price = 0.0
                        else:
                            current_line_name = next_line_name
                            current_segment_start_id = u
                            current_segment_time = 0.0
                            current_segment_price = 0.0

                    elif current_line_name == "":
                        current_line_name = next_line_name
                        current_segment_start_id = u

                    # 累计时间和价格（换乘段除外）
                    if next_line_name != "TRANSFER":
                        current_segment_time += edge.distance
                        current_segment_price += edge.price

                    break

            if not edge_found:
                return Route()

        # 处理最后一段
        if len(path_ids) >= 2:
            final_station_name = self.data.station_id_info[path_ids[-1]].name
            line_sum = (f"{self.data.station_id_info[current_segment_start_id].name}"
                        f" -> ({current_line_name}) -> {final_station_name}")
            summary += ("" if not summary else " -> ") + line_sum

            route.segments.append(RouteSegment(
                self.data.station_id_info[current_segment_start_id].name,
                final_station_name,
                current_line_name,
                current_segment_time,
                current_segment_price
            ))

        route.description = summary
        return route

    # =====================================================
    # DFS 搜索多条路径
    # =====================================================
    def _dfs_find_routes(self, current_id, end_id, current_path, visited,
                         current_time, current_price, all_routes, max_stops, max_cost):
        """DFS 搜索所有可能的路径（追踪时间和价格）"""
        current_path.append(current_id)
        visited[current_id] = True

        # 路径过长或耗时过大，防止内存爆炸
        if len(current_path) > max_stops or current_time > max_cost:
            visited[current_id] = False
            current_path.pop()
            return

        if current_id == end_id:
            new_route = self._path_id_to_route(current_path, current_time, current_price)
            all_routes.append(new_route)
            visited[current_id] = False
            current_path.pop()
            return

        for edge in self.adj_list[current_id]:
            next_id = edge.dest_id
            if not visited[next_id]:
                self._dfs_find_routes(
                    next_id, end_id, current_path, visited,
                    current_time + edge.distance,
                    current_price + edge.price,
                    all_routes, max_stops, max_cost
                )

        visited[current_id] = False
        current_path.pop()

    # =====================================================
    # 3. 乘车查询（核心功能）
    # =====================================================
    def find_routes(self, start, end, use_price):
        """
        查找从 start 到 end 的所有有效乘车方案
        :param start: 起始站名
        :param end: 到达站名
        :param use_price: True=按最短价格, False=按最短时间
        :return: 方案列表
        """
        # 验证起始和终止站是否存在
        if start not in self.data.station_name_id or end not in self.data.station_name_id:
            utils.print_error("起始或终点站点不存在。")
            return []

        start_id = self.data.station_name_id[start]
        end_id = self.data.station_name_id[end]
        all_routes = []

        # 1. Dijkstra 算法找最短路径（根据用户选择的维度）
        shortest_path_ids, shortest_results = self._dijkstra(start_id, end_id, use_price)

        if not shortest_path_ids:
            utils.print_error(f"找不到从 [{start}] 到 [{end}] 的路径。")
            return []

        # 2. 根据 Dijkstra 获取另一种成本（为了同时记录 Route 信息）
        shortest_cost_value = shortest_results[end_id]

        if use_price:
            # shortestCostValue = 最短价格，需要再次运行Dijkstra获取最短时间
            _, time_results = self._dijkstra(start_id, end_id, False)
            shortest_price = shortest_cost_value
            shortest_time = time_results[end_id]
        else:
            # shortestCostValue = 最短时间，需要再次运行Dijkstra获取最短价格
            _, price_results = self._dijkstra(start_id, end_id, True)
            shortest_time = shortest_cost_value
            shortest_price = price_results[end_id]

        # 转换为 Route 结构，加入结果列表
        shortest_route = self._path_id_to_route(shortest_path_ids, shortest_time, shortest_price)
        all_routes.append(shortest_route)

        # 3. DFS 搜索所有路径（有时间和限制）
        current_path = []
        visited = [False] * self.data.next_station_id

        max_stops = len(shortest_path_ids) + 5
        max_time = shortest_time * 1.5

        self._dfs_find_routes(start_id, end_id, current_path, visited,
                              0.0, 0.0, all_routes, max_stops, max_time)

        # 4. 排序并去重（根据用户选择的成本维度）
        if use_price:
            all_routes.sort(key=lambda r: (r.total_price, r.total_cost))
        else:
            all_routes.sort(key=lambda r: (r.total_cost, r.total_price))

        # 简单的去重逻辑（基于站点ID路径）
        unique_routes = []
        path_set = set()
        for route in all_routes:
            if not route.segments:
                continue

            id_path = [self.data.station_name_id[route.segments[0].start_station]]
            for seg in route.segments:
                if seg.line_name != "TRANSFER":
                    id_path.append(self.data.station_name_id[seg.end_station])

            path_tuple = tuple(id_path)
            if path_tuple not in path_set:
                path_set.add(path_tuple)
                unique_routes.append(route)

        all_routes = unique_routes

        # 5. 格式化输出
        strategy = "最短价格优先" if use_price else "最短时间优先"
        print(f"\n{'='*16} 乘车查询结果 ({strategy}) {'='*16}")
        print(f"起点: {start}, 终点: {end}")
        print(f"共找到 {len(all_routes)} 条有效方案。")

        if use_price:
            print(f"最短价格方案: {shortest_price:.1f} 元, 耗时: {shortest_time:.1f} 分钟。")
        else:
            print(f"最短时间方案: {shortest_time:.1f} 分钟, 价格: {shortest_price:.1f} 元。")

        for i, route in enumerate(all_routes):
            utils.print_route(route, i + 1)

        return all_routes
