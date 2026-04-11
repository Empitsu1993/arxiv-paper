"""
興味のあるキーワードとラベルの設定
キーワードリストを編集して、タイトルに含まれる単語に応じたラベルを付けます
"""

# キーワードとラベルのマッピング
# キー: ラベル名、値: キーワードのリスト（大文字小文字を区別しない）
KEYWORD_LABELS = {
    "privacy": {
        "keywords": ["private", "differential", "privacy", "differentially","membership inference", "attribute inference", "reconstruction", "dataset inferece","model inversion", "memorization","unlearning"],
        "color": "#ff69b4",  # 明るいピンク色
    },
    "model extraction": {
        "keywords": ["model extraction", "model stealing", "distillation", "ReLU", "model reconstruction"],
        "color": "#f1c40f",  # 黄色
    },
    "synthetic data": {
        "keywords": ["synthetic data", "synthetic data generation", "data synthesis", "synthetic tabular data"],
        "color": "#e67e22",  # オレンジ色
    },
    "intellectual property": {
        "keywords": ["watermarking", "watermark","intellectual property", "copyright"],

        "color": "#27ae60",  # 緑色
    },
    "backdoor": {
        "keywords": ["backdoor", "poisoning", "poisoned"],
        "color": "#3498db",  # 青色
    },
    "agent": {
        "keywords": ["agent", "agentic", "agentic system", "agentic agent", "agentic agentic system"],
        "color": "#e74c3c",  # 赤色
    },
    "diffusion": {
        "keywords": ["diffusion"],
        "color": "#9b59b6",  # 紫
    },
    "del Pezzo": {
        "keywords": ["del Pezzo"],
        "color": "#9b59b6",  # 紫
    },
}


def find_labels(title: str) -> list[tuple[str, str]]:
    """
    タイトルからキーワードを検索し、該当するラベルを返す
    
    Args:
        title: 論文のタイトル
    
    Returns:
        [(ラベル名, 色)] のリスト
    """
    title_lower = title.lower()
    matched_labels = []
    
    for label_name, config in KEYWORD_LABELS.items():
        keywords = config["keywords"]
        color = config["color"]
        
        # タイトルにいずれかのキーワードが含まれているかチェック
        for keyword in keywords:
            if keyword.lower() in title_lower:
                matched_labels.append((label_name, color))
                break  # 1つのラベルが1回だけ追加されるように
    
    return matched_labels


def get_all_keywords() -> dict:
    """
    全てのキーワード設定を返す
    
    Returns:
        キーワード設定の辞書
    """
    return KEYWORD_LABELS

