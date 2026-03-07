from collections import defaultdict, deque

class GraphSorter:
    @staticmethod
    def topological_sort(quests_info):
        """クエスト情報のリストを受け取り、トポロジカルソートされたIDのリストを返す"""
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        
        chapter_nodes = {q["id"] for q in quests_info}
        
        # グラフを構築する（同一チャプター内の依存関係のみを考慮）
        for q in quests_info:
            node = q["id"]
            in_degree[node] += 0 
            
            for dep in q["dependencies"]:
                if dep in chapter_nodes:
                    graph[dep].append(node)
                    in_degree[node] += 1
                    
        # 依存を持たないノードから処理を開始する
        start_nodes = sorted([node for node in chapter_nodes if in_degree[node] == 0])
        queue = deque(start_nodes)
        
        sorted_ids = []
        
        while queue:
            current = queue.popleft()
            sorted_ids.append(current)
            
            for neighbor in sorted(graph[current]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # 循環参照などで未処理となったノードを末尾に追加する
        missing_nodes = chapter_nodes - set(sorted_ids)
        if missing_nodes:
            sorted_ids.extend(sorted(list(missing_nodes)))
            
        return sorted_ids