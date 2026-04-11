import json
from datetime import datetime
from keywords_config import find_labels


def generate_html_content(feed_title: str, feed_updated: str, entries: list) -> str:
    """
    arXiv論文一覧のHTMLコンテンツを生成する
    
    Args:
        feed_title: フィードタイトル
        feed_updated: フィード更新日時
        entries: 論文エントリのリスト
    
    Returns:
        HTMLコンテンツ文字列
    """
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>arXiv論文一覧 - {feed_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .info {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .paper {{
            background-color: white;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s ease;
        }}
        .paper:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .paper-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .paper-title a {{
            color: #2980b9;
            text-decoration: none;
        }}
        .paper-title a:hover {{
            text-decoration: underline;
        }}
        .paper-meta {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .paper-author {{
            margin-bottom: 5px;
        }}
        .paper-date {{
            margin-bottom: 5px;
        }}
        .paper-link {{
            margin-top: 5px;
        }}
        .paper-link a {{
            color: #27ae60;
            text-decoration: none;
        }}
        .paper-link a:hover {{
            text-decoration: underline;
        }}
        .paper-summary {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ecf0f1;
            color: #555;
            line-height: 1.8;
        }}
        .count {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 10px;
        }}
        .title-list {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .title-list h2 {{
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .title-item {{
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        .title-item:last-child {{
            border-bottom: none;
        }}
        .title-item a {{
            color: #2980b9;
            text-decoration: none;
        }}
        .title-item a:hover {{
            text-decoration: underline;
            color: #3498db;
        }}
        .title-number {{
            display: inline-block;
            min-width: 30px;
            font-weight: bold;
            color: #7f8c8d;
        }}
        .section-header {{
            background-color: #3498db;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 30px 0 20px 0;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .paper {{
            scroll-margin-top: 20px;
        }}
        .paper.hidden {{
            display: none;
        }}
        .paper-checkbox {{
            margin-right: 10px;
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}
        .checkbox-label {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
            font-size: 0.9em;
            color: #495057;
        }}
        .action-buttons {{
            position: sticky;
            top: 20px;
            background-color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            margin-bottom: 20px;
            z-index: 100;
        }}
        .action-buttons button {{
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            margin-right: 10px;
            transition: background-color 0.3s ease;
        }}
        .action-buttons button:hover {{
            background-color: #2980b9;
        }}
        .action-buttons button:disabled {{
            background-color: #95a5a6;
            cursor: not-allowed;
        }}
        .selected-count {{
            display: inline-block;
            margin-left: 10px;
            color: #27ae60;
            font-weight: bold;
        }}
        .paper-labels {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
            margin-bottom: 10px;
        }}
        .label-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            color: white;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}
        .title-label-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75em;
            font-weight: 600;
            color: white;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
            margin-left: 8px;
        }}
    </style>
</head>
<body>
    <h1>{feed_title}</h1>
    
    <div class="info">
        <strong>更新日時:</strong> {feed_updated}<br>
        <strong>論文数:</strong> {len(entries)}件
    </div>
    
    <div class="action-buttons">
        <button onclick="selectAll()">全て選択</button>
        <button onclick="deselectAll()">全て解除</button>
        <button onclick="showAll()" id="showAllButton">全て表示</button>
        <button onclick="showSelectedOnly()" id="showSelectedButton">選択したもののみ表示</button>
        <span class="selected-count" id="selectedCount">0件選択中</span>
    </div>
    
    <div class="title-list">
        <h2>📋 論文タイトル一覧</h2>
"""
    
    # タイトル一覧を生成
    for i, entry in enumerate(entries, 1):
        title = entry.get('title', 'N/A').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        original_title = entry.get('title', 'N/A')
        link = entry.get('link', '#')
        paper_id = f"paper-{i}"
        
        # ラベルを取得
        labels = find_labels(original_title)
        labels_html = ""
        for label_name, label_color in labels:
            labels_html += f'<span class="title-label-badge" style="background-color: {label_color};">{label_name}</span>'
        
        html_content += f"""        <div class="title-item">
            <input type="checkbox" class="title-checkbox" data-paper-id="{paper_id}" onchange="updateSelectedCount()">
            <span class="title-number">{i}.</span>
            <a href="#{paper_id}">{title}</a>
            {labels_html}
        </div>
"""
    
    html_content += """    </div>
    
    <div class="section-header">📄 論文詳細</div>
    
    <div class="papers">
"""
    
    # 詳細情報を生成
    for i, entry in enumerate(entries, 1):
        title = entry.get('title', 'N/A').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        author = entry.get('author', 'N/A').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        published = entry.get('published', 'N/A')
        link = entry.get('link', '#')
        summary = entry.get('summary', '')
        if summary:
            summary = summary.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        paper_id = f"paper-{i}"
        # 論文データをJSON形式でエンコード（JavaScriptで使用）
        # 注意: JSONには元のデータ（エスケープ前）を使用
        original_title = entry.get('title', 'N/A')
        original_author = entry.get('author', 'N/A')
        original_summary = entry.get('summary', '')
        
        # ラベルを取得（JSONデータ作成前に）
        labels = find_labels(original_title)
        labels_data = [{"name": name, "color": color} for name, color in labels]
        
        paper_data = {
            "title": original_title,
            "author": original_author,
            "published": published,
            "link": link,
            "summary": original_summary,
            "number": i,
            "labels": labels_data
        }
        paper_data_json = json.dumps(paper_data, ensure_ascii=False)
        # HTML属性に埋め込むため、HTMLエスケープ（&と<>は既にエスケープ済みのtitle/authorとは別）
        paper_data_json_escaped = paper_data_json.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # ラベルHTMLを生成
        labels_html = ""
        if labels:
            labels_html = '<div class="paper-labels">'
            for label_name, label_color in labels:
                labels_html += f'<span class="label-badge" style="background-color: {label_color};">{label_name}</span>'
            labels_html += '</div>'
        
        html_content += f"""        <div class="paper" id="{paper_id}">
            <input type="checkbox" class="paper-checkbox" data-paper-id="{paper_id}" data-paper-data='{paper_data_json_escaped}' onchange="updateSelectedCount(); syncTitleCheckbox(this)" style="display: none;">
            <div class="paper-title">
                <span style="color: #7f8c8d; font-size: 0.9em; margin-right: 10px;">#{i}</span>
                <a href="{link}" target="_blank">{title}</a>
            </div>
            {labels_html}
            <div class="paper-meta">
                <div class="paper-author"><strong>著者:</strong> {author}</div>
                <div class="paper-date"><strong>公開日:</strong> {published}</div>
                <div class="paper-link"><strong>リンク:</strong> <a href="{link}" target="_blank">{link}</a></div>
            </div>
"""
        
        if summary:
            if "Abstract: " in summary:
                abstract_text = summary.split("Abstract: ", 1)[1]
                summary = abstract_text
                
            html_content += f"""            <div class="paper-summary">
                <strong>要約:</strong><br>
                {summary}
            </div>
"""
        
        html_content += """        </div>
"""
    
    html_content += f"""    </div>
    
    <div class="count">
        生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    
    <script>
        // タイトル一覧のチェックボックスと詳細のチェックボックスを同期
        function syncTitleCheckbox(checkbox) {{
            const paperId = checkbox.getAttribute('data-paper-id');
            const titleCheckbox = document.querySelector(`.title-checkbox[data-paper-id="${{paperId}}"]`);
            if (titleCheckbox) {{
                titleCheckbox.checked = checkbox.checked;
            }}
        }}
        
        // タイトル一覧のチェックボックスをクリックしたときの処理
        document.addEventListener('DOMContentLoaded', function() {{
            const titleCheckboxes = document.querySelectorAll('.title-checkbox');
            titleCheckboxes.forEach(checkbox => {{
                checkbox.addEventListener('change', function() {{
                    const paperId = this.getAttribute('data-paper-id');
                    const paperCheckbox = document.querySelector(`.paper-checkbox[data-paper-id="${{paperId}}"]`);
                    if (paperCheckbox) {{
                        paperCheckbox.checked = this.checked;
                        updateSelectedCount();
                        // 選択のみ表示モードの場合、表示を更新
                        if (document.getElementById('showSelectedButton').style.backgroundColor === 'rgb(41, 128, 185)') {{
                            showSelectedOnly();
                        }}
                    }}
                }});
            }});
            
            // 初期状態では全て表示
            document.getElementById('showAllButton').style.backgroundColor = '#2980b9';
        }});
        
        // 選択された論文数を更新
        function updateSelectedCount() {{
            const checkedBoxes = document.querySelectorAll('.paper-checkbox:checked');
            const count = checkedBoxes.length;
            document.getElementById('selectedCount').textContent = count + '件選択中';
        }}
        
        // 全て選択
        function selectAll() {{
            document.querySelectorAll('.paper-checkbox, .title-checkbox').forEach(cb => cb.checked = true);
            updateSelectedCount();
        }}
        
        // 全て解除
        function deselectAll() {{
            document.querySelectorAll('.paper-checkbox, .title-checkbox').forEach(cb => cb.checked = false);
            updateSelectedCount();
        }}
        
        // 全て表示
        function showAll() {{
            document.querySelectorAll('.paper').forEach(paper => {{
                paper.classList.remove('hidden');
            }});
            document.getElementById('showAllButton').style.backgroundColor = '#2980b9';
            document.getElementById('showSelectedButton').style.backgroundColor = '#3498db';
        }}
        
        // 選択したもののみ表示
        function showSelectedOnly() {{
            const checkedBoxes = document.querySelectorAll('.paper-checkbox:checked');
            const checkedIds = Array.from(checkedBoxes).map(cb => cb.getAttribute('data-paper-id'));
            
            if (checkedIds.length === 0) {{
                alert('選択した論文がありません');
                return;
            }}
            
            document.querySelectorAll('.paper').forEach(paper => {{
                const paperId = paper.getAttribute('id');
                if (checkedIds.includes(paperId)) {{
                    paper.classList.remove('hidden');
                }} else {{
                    paper.classList.add('hidden');
                }}
            }});
            
            document.getElementById('showAllButton').style.backgroundColor = '#3498db';
            document.getElementById('showSelectedButton').style.backgroundColor = '#2980b9';
        }}
        
        // チェックボックス変更時に表示を更新
        document.querySelectorAll('.paper-checkbox').forEach(checkbox => {{
            checkbox.addEventListener('change', function() {{
                updateSelectedCount();
                // 選択のみ表示モードの場合、表示を更新
                if (document.getElementById('showSelectedButton').style.backgroundColor === 'rgb(41, 128, 185)') {{
                    showSelectedOnly();
                }}
            }});
        }});
        
        // 初期化
        updateSelectedCount();
    </script>
</body>
</html>"""
    
    return html_content

