import json

class LangSorter:
    def __init__(self, lang_filepath, output_filepath):
        self.lang_filepath = lang_filepath
        self.output_filepath = output_filepath

    def sort_and_save(self, sorted_chapters):
        """ソート済みのチャプター情報を元に、langファイルを再構築して保存する"""
        print(f"Reading language file: {self.lang_filepath}")
        with open(self.lang_filepath, 'r', encoding='utf-8-sig') as f:
            lang_data = json.load(f)
            
        sorted_lang_data = {}
        used_keys = set()

        print("Sorting language keys...")
        
        for chapter in sorted_chapters:
            # 1. チャプター固有のキーを配置する
            def ch_sort_key(k):
                if k.endswith("title"): return (0, k)
                elif "subtitle" in k: return (1, k)
                else: return (2, k)
                
            ch_keys = [k for k in chapter.chapter_lang_keys if k in lang_data]
            for k in sorted(ch_keys, key=ch_sort_key):
                if k not in used_keys:
                    sorted_lang_data[k] = lang_data[k]
                    used_keys.add(k)
                
            # 2. チャプター内のクエストキーを配置する
            for qid in chapter.sorted_ids:
                quest_info = next((q for q in chapter.quests if q["id"] == qid), None)
                if not quest_info:
                    continue
                    
                def q_sort_key(k):
                    if k.endswith("title"): return (0, k)
                    elif k.endswith("subtitle"): return (1, k)
                    elif "description" in k: return (2, k)
                    else: return (3, k)

                q_keys = [k for k in quest_info["lang_keys"] if k in lang_data]
                for k in sorted(q_keys, key=q_sort_key):
                    if k not in used_keys:
                        sorted_lang_data[k] = lang_data[k]
                        used_keys.add(k)

        # 3. どのクエストにも紐づかなかった残りのキーを末尾に配置する
        leftover_keys = [k for k in lang_data.keys() if k not in used_keys]
        for k in leftover_keys:
            sorted_lang_data[k] = lang_data[k]

        print(f"Writing sorted data to: {self.output_filepath}")
        with open(self.output_filepath, 'w', encoding='utf-8') as f:
            json.dump(sorted_lang_data, f, indent=2, ensure_ascii=False)