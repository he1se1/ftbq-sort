import os
import ftb_snbt_lib

class QuestData:
    def __init__(self, chapter_name, group_id="", order_index=0):
        self.chapter_name = chapter_name
        self.group_id = group_id
        self.order_index = order_index
        self.quests = []

class SnbtParser:
    def __init__(self, quests_dir):
        self.quests_dir = quests_dir
        self.chapters_dir = os.path.join(quests_dir, "chapters")
        self.chapter_groups_file = os.path.join(quests_dir, "chapter_groups.snbt")

    def parse_all(self):
        """ディレクトリ内のSNBTファイルをパースし、GUI順にソートされたQuestDataのリストを返す"""
        
        # 1. chapter_groups.snbt を読み込んでグループの表示順序(インデックス)をマッピング
        group_order = {}
        if os.path.exists(self.chapter_groups_file):
            with open(self.chapter_groups_file, 'r', encoding='utf-8-sig') as f:
                cg_data = ftb_snbt_lib.load(f)
                for i, group in enumerate(cg_data.get("chapter_groups", [])):
                    group_id = group.get("id", "")
                    group_order[group_id] = i

        # 2. chapters ディレクトリ内のクエストを読み込む
        parsed_chapters = []
        if not os.path.exists(self.chapters_dir):
            raise FileNotFoundError(f"Directory not found: {self.chapters_dir}")

        for filename in os.listdir(self.chapters_dir):
            if not filename.endswith(".snbt"):
                continue
                
            filepath = os.path.join(self.chapters_dir, filename)
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                parsed_data = ftb_snbt_lib.load(f)
            
            chapter_name = parsed_data.get("filename", filename.replace(".snbt", ""))
            group_id = parsed_data.get("group", "")
            order_index = parsed_data.get("order_index", 9999)
            
            quest_data = QuestData(chapter_name, group_id, order_index)
            
            # クエスト情報の抽出
            for quest in parsed_data.get("quests", []):
                quest_id = quest.get("id", "")
                dependencies = quest.get("dependencies", [])
                
                if isinstance(dependencies, str):
                    dependencies = [dependencies]
                    
                quest_data.quests.append({
                    "id": quest_id,
                    "dependencies": dependencies
                })
                
            parsed_chapters.append(quest_data)
            
        # 3. チャプターのソート (第1キー: グループの順序, 第2キー: チャプターのorder_index)
        def get_sort_key(chapter):
            if chapter.group_id:
                # グループに属している場合はそのグループの順番を取得（不明なら後ろへ）
                g_index = group_order.get(chapter.group_id, 9999)
            else:
                # グループに属していない独立したチャプターは、FTB Questsの仕様上上に表示されるため -1
                g_index = -1 
                
            return (g_index, chapter.order_index)

        parsed_chapters.sort(key=get_sort_key)
            
        return parsed_chapters