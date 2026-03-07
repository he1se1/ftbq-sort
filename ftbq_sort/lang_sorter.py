import json

class LangSorter:
    def __init__(self, lang_filepath, output_filepath):
        self.lang_filepath = lang_filepath
        self.output_filepath = output_filepath

    def sort_and_save(self, sorted_chapters):
        """
        sorted_chapters: list of tuples (chapter_name, sorted_id_list)
        """
        with open(self.lang_filepath, 'r', encoding='utf-8-sig') as f:
            lang_data = json.load(f)
            
        # 1. すべてのパース済みIDをフラットなセットにしておく
        all_quest_ids = set()
        for _, ids in sorted_chapters:
            all_quest_ids.update(ids)

        # 2. キーの分類
        quest_keys_map = {qid: [] for qid in all_quest_ids}
        unmapped_quest_keys = []
        other_keys = []

        for key in lang_data.keys():
            matched_id = None
            for qid in all_quest_ids:
                if f".{qid}." in key or key.endswith(f".{qid}"):
                    matched_id = qid
                    break
            
            if matched_id:
                quest_keys_map[matched_id].append(key)
            elif ".quests." in key:
                unmapped_quest_keys.append(key)
            else:
                other_keys.append(key)

        # 3. other_keysの中からチャプター固有のキー（title等）を抽出し、残りを末尾行きにする
        chapter_keys_map = {ch_name: [] for ch_name, _ in sorted_chapters}
        leftover_keys = []

        for key in other_keys:
            assigned = False
            # キーをドットで分割 (例: "gto.steam.title" -> ["gto", "steam", "title"])
            parts = key.split('.')
            
            for ch_name, _ in sorted_chapters:
                # ドット区切りの一部にチャプター名(ファイル名)が完全一致すれば、そのチャプターのキーとみなす
                if ch_name in parts:
                    chapter_keys_map[ch_name].append(key)
                    assigned = True
                    break
                    
            if not assigned:
                leftover_keys.append(key) # チャプターグループ名などはここに入る

        # 4. 新しい辞書に順番に詰め直す
        sorted_lang_data = {}

        # チャプターごとに書き出し
        for ch_name, ids in sorted_chapters:
            
            # --- A. まずチャプターのタイトル・サブタイトル等を配置 ---
            def ch_sort_key(k):
                # チャプターキー内でも title -> subtitle の順になるように調整
                if k.endswith("title"): return (0, k)
                elif "subtitle" in k: return (1, k)
                else: return (2, k)
                
            for k in sorted(chapter_keys_map[ch_name], key=ch_sort_key):
                sorted_lang_data[k] = lang_data[k]
                
            # --- B. 次にそのチャプターに属するクエスト群を配置 ---
            for qid in ids:
                if qid in quest_keys_map:
                    def q_sort_key(k):
                        parts = k.split(f".{qid}.")
                        suffix = parts[-1] if len(parts) > 1 else k
                        
                        if suffix == "title": return (0, k)
                        elif suffix == "subtitle": return (1, k)
                        elif suffix.startswith("description"): return (2, k)
                        else: return (3, k)

                    for k in sorted(quest_keys_map[qid], key=q_sort_key):
                        sorted_lang_data[k] = lang_data[k]

        # --- C. パースできなかった不明なクエストキーを配置 ---
        for k in unmapped_quest_keys:
            sorted_lang_data[k] = lang_data[k]

        # --- D. 最後にその他のキー (チャプターグループ名など) をファイルの末尾に配置 ---
        for k in leftover_keys:
            sorted_lang_data[k] = lang_data[k]

        # 5. JSONとして書き出し
        with open(self.output_filepath, 'w', encoding='utf-8') as f:
            json.dump(sorted_lang_data, f, indent=2, ensure_ascii=False)