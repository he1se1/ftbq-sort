import os
import re
import ftb_snbt_lib

class QuestData:
    def __init__(self, chapter_name, group_id="", order_index=0):
        self.chapter_name = chapter_name
        self.group_id = group_id
        self.order_index = order_index
        self.quests = []
        self.chapter_lang_keys = set()
        self.sorted_ids = []

    @staticmethod
    def extract_lang_keys(data, keys_set):
        """データ構造を再帰的に探索し、言語キーを抽出する"""
        if isinstance(data, str):
            # Pattern 1: FTB Questsの基本形式 "{lang.key}" 
            if data.startswith("{") and data.endswith("}"):
                inner = data[1:-1]
                # 誤爆防止: jsonの波括弧や空白、ダブルクォートが含まれていないかチェック
                if '"' not in inner and '{' not in inner and ' ' not in inner:
                    keys_set.add(inner)
            
            # Pattern 2: マイクラのリッチテキスト(Raw JSON)形式から "translate": "lang.key" を抽出
            if "translate" in data:
                # ダブルクォートの間のキー名を正規表現で抜き出す
                matches = re.findall(r'"translate"\s*:\s*"([^"]+)"', data)
                keys_set.update(matches)

        elif isinstance(data, dict):
            # 万が一辞書としてパースされていた場合の保険
            if "translate" in data and isinstance(data["translate"], str):
                keys_set.add(data["translate"])
            for value in data.values():
                QuestData.extract_lang_keys(value, keys_set)
        elif isinstance(data, list):
            for item in data:
                QuestData.extract_lang_keys(item, keys_set)

class SnbtParser:
    def __init__(self, quests_dir):
        self.quests_dir = quests_dir
        self.chapters_dir = os.path.join(quests_dir, "chapters")
        self.chapter_groups_file = os.path.join(quests_dir, "chapter_groups.snbt")

    def parse_all(self):
        """SNBTファイルをパースし、GUI順にソートされたQuestDataのリストを返す"""
        group_order = {}
        if os.path.exists(self.chapter_groups_file):
            print("Parsing chapter_groups.snbt...")
            with open(self.chapter_groups_file, 'r', encoding='utf-8-sig') as f:
                cg_data = ftb_snbt_lib.load(f)
                for i, group in enumerate(cg_data.get("chapter_groups", [])):
                    group_id = str(group.get("id", "")).upper()
                    group_order[group_id] = i
        else:
            print(f"Notice: {self.chapter_groups_file} not found. Proceeding without group sorting.")

        parsed_chapters = []
        if not os.path.exists(self.chapters_dir):
            raise FileNotFoundError(f"Directory not found: {self.chapters_dir}")

        chapter_files = [f for f in os.listdir(self.chapters_dir) if f.endswith(".snbt")]
        print(f"Parsing {len(chapter_files)} chapter files...")

        for filename in chapter_files:
            filepath = os.path.join(self.chapters_dir, filename)
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                parsed_data = ftb_snbt_lib.load(f)
            
            chapter_name = parsed_data.get("filename", filename.replace(".snbt", ""))
            raw_group = parsed_data.get("group", "")
            group_id = str(raw_group).upper() if raw_group else ""
            order_index = parsed_data.get("order_index", 9999)
            
            quest_data = QuestData(chapter_name, group_id, order_index)
            
            # チャプター自体に付いた言語キーを抽出する
            for ch_key in ["title", "subtitle", "description"]:
                if ch_key in parsed_data:
                    QuestData.extract_lang_keys(parsed_data[ch_key], quest_data.chapter_lang_keys)
            
            # クエスト情報とその言語キーを抽出する
            for quest in parsed_data.get("quests", []):
                quest_id = quest.get("id", "")
                dependencies = quest.get("dependencies", [])
                
                if isinstance(dependencies, str):
                    dependencies = [dependencies]
                    
                lang_keys = set()
                QuestData.extract_lang_keys(quest, lang_keys)
                    
                quest_data.quests.append({
                    "id": quest_id,
                    "dependencies": dependencies,
                    "lang_keys": lang_keys
                })
                
            parsed_chapters.append(quest_data)
            
        # グループ順序、次いでチャプターのorder_indexでソートする
        def get_sort_key(chapter):
            g_index = group_order.get(chapter.group_id, 9999) if chapter.group_id else -1
            return (g_index, chapter.order_index)

        parsed_chapters.sort(key=get_sort_key)
        return parsed_chapters