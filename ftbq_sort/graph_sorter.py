from collections import defaultdict, deque

class GraphSorter:
    @staticmethod
    def topological_sort(quests_info):
        """
        クエスト情報のリストを受け取り、トポロジカルソートされたIDのリストを返す。
        """
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        
        # このチャプターに実際に所属しているクエストIDのセット
        chapter_nodes = {q["id"] for q in quests_info}
        
        # グラフの構築
        for q in quests_info:
            node = q["id"]
            in_degree[node] += 0 
            
            for dep in q["dependencies"]:
                # 依存先が同じチャプター内の場合のみエッジを張る
                if dep in chapter_nodes:
                    graph[dep].append(node)
                    in_degree[node] += 1
                    
        # 入次数0（チャプター内での前提がないノード）を抽出してソート（順序の安定化）
        start_nodes = sorted([node for node in chapter_nodes if in_degree[node] == 0])
        queue = deque(start_nodes)
        
        sorted_ids = []
        
        # Kahnのアルゴリズム
        while queue:
            current = queue.popleft()
            sorted_ids.append(current)
            
            # 隣接ノードもソートしておくことで出力順序をより決定論的にする
            for neighbor in sorted(graph[current]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # フェールセーフ: 万が一、SNBT内で循環参照（閉路）が起きていた場合、
        # 処理されなかったIDが消えないように末尾に追加しておく
        missing_nodes = chapter_nodes - set(sorted_ids)
        if missing_nodes:
            sorted_ids.extend(sorted(list(missing_nodes)))
            
        return sorted_ids