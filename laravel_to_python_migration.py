# laravel_to_python_migration.py
import sqlite3
import json
import os
from datetime import datetime

def export_laravel_data(laravel_db_path):
    """Laravel版SQLiteからデータをエクスポート"""
    
    print(f"📁 Laravel版データベースに接続中: {laravel_db_path}")
    
    try:
        # Laravel版データベースに接続
        conn = sqlite3.connect(laravel_db_path)
        cursor = conn.cursor()
        
        # エクスポート用データ構造
        export_data = {
            'export_info': {
                'export_date': datetime.now().isoformat(),
                'version': '2.0',
                'app_name': 'Laravel to Python Complete Migration',
                'source': 'Laravel SQLite Database',
                'migration_type': 'complete_replacement'
            },
            'users': [],  # 空のまま（ユーザーは移行しない）
            'sicks': [],
            'forms': [],
            'protocols': []
        }
        
        # データベース内のテーブル一覧を確認
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 検出されたテーブル: {[table[0] for table in tables]}")
        
        # sicksテーブルのデータ取得
        print("\n🔍 sicksテーブルからデータを取得中...")
        try:
            # テーブル構造を確認
            cursor.execute("PRAGMA table_info(sicks)")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            print(f"   カラム: {column_names}")
            
            # データ取得
            cursor.execute("SELECT * FROM sicks ORDER BY id")
            sicks_rows = cursor.fetchall()
            print(f"   データ件数: {len(sicks_rows)}件")
            
            for row in sicks_rows:
                # カラム名と値を対応させる
                row_dict = dict(zip(column_names, row))
                
                # Python版の形式に合わせてデータ構造を作成
                sick_data = {
                    'id': row_dict.get('id', ''),
                    'diesease': row_dict.get('diesease', ''),
                    'diesease_text': row_dict.get('diesease_text', ''),
                    'keyword': row_dict.get('keyword', ''),
                    'protocol': row_dict.get('protocol', ''),
                    'protocol_text': row_dict.get('protocol_text', ''),
                    'processing': row_dict.get('processing', ''),
                    'processing_text': row_dict.get('processing_text', ''),
                    'contrast': row_dict.get('contrast', ''),
                    'contrast_text': row_dict.get('contrast_text', ''),
                    'diesease_img': '',  # 画像データを除外
                    'protocol_img': '',  # 画像データを除外
                    'processing_img': '',  # 画像データを除外
                    'contrast_img': '',  # 画像データを除外
                    'created_at': row_dict.get('created_at', ''),
                    'updated_at': row_dict.get('updated_at', '')
                }
                
                export_data['sicks'].append(sick_data)
                
            print(f"   ✅ {len(export_data['sicks'])}件の疾患データを取得")
            
        except Exception as e:
            print(f"   ❌ sicksテーブルエラー: {e}")
        
        # formsテーブルのデータ取得
        print("\n🔍 formsテーブルからデータを取得中...")
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='forms'")
            forms_table_exists = cursor.fetchone() is not None
            
            if forms_table_exists:
                # テーブル構造を確認
                cursor.execute("PRAGMA table_info(forms)")
                forms_columns_info = cursor.fetchall()
                forms_column_names = [col[1] for col in forms_columns_info]
                print(f"   カラム: {forms_column_names}")
                
                # データ取得
                cursor.execute("SELECT * FROM forms ORDER BY id")
                forms_rows = cursor.fetchall()
                print(f"   データ件数: {len(forms_rows)}件")
                
                for row in forms_rows:
                    row_dict = dict(zip(forms_column_names, row))
                    
                    form_data = {
                        'id': row_dict.get('id', ''),
                        'title': row_dict.get('title', ''),
                        'main': row_dict.get('main', ''),
                        'post_img': '',  # 画像データを除外
                        'created_at': row_dict.get('created_at', ''),
                        'updated_at': row_dict.get('updated_at', '')
                    }
                    
                    export_data['forms'].append(form_data)
                
                print(f"   ✅ {len(export_data['forms'])}件のお知らせデータを取得")
            else:
                print("   ℹ️ formsテーブルが存在しません")
                
        except Exception as e:
            print(f"   ❌ formsテーブルエラー: {e}")
        
        # protocolsテーブルのデータ取得（存在する場合）
        print("\n🔍 protocolsテーブルからデータを取得中...")
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='protocols'")
            protocols_table_exists = cursor.fetchone() is not None
            
            if protocols_table_exists:
                # テーブル構造を確認
                cursor.execute("PRAGMA table_info(protocols)")
                protocols_columns_info = cursor.fetchall()
                protocols_column_names = [col[1] for col in protocols_columns_info]
                print(f"   カラム: {protocols_column_names}")
                
                # データ取得
                cursor.execute("SELECT * FROM protocols ORDER BY id")
                protocols_rows = cursor.fetchall()
                print(f"   データ件数: {len(protocols_rows)}件")
                
                for row in protocols_rows:
                    row_dict = dict(zip(protocols_column_names, row))
                    
                    protocol_data = {
                        'id': row_dict.get('id', ''),
                        'category': row_dict.get('category', ''),
                        'title': row_dict.get('title', ''),
                        'content': row_dict.get('content', ''),
                        'protocol_img': '',  # 画像データを除外
                        'created_at': row_dict.get('created_at', ''),
                        'updated_at': row_dict.get('updated_at', '')
                    }
                    
                    export_data['protocols'].append(protocol_data)
                
                print(f"   ✅ {len(export_data['protocols'])}件のプロトコルデータを取得")
            else:
                print("   ℹ️ protocolsテーブルが存在しません")
                
        except Exception as e:
            print(f"   ❌ protocolsテーブルエラー: {e}")
        
        conn.close()
        return export_data, "OK"
        
    except Exception as e:
        return None, f"エクスポート中にエラーが発生: {str(e)}"

def create_migration_summary(data):
    """移行データのサマリーを作成"""
    summary = f"""
=== Laravel → Python 移行データサマリー ===

📊 データ件数:
  - 疾患データ (sicks): {len(data['sicks'])}件
  - お知らせ (forms): {len(data['forms'])}件
  - CTプロトコル (protocols): {len(data['protocols'])}件

📅 エクスポート日時: {data['export_info']['export_date']}

🔄 移行タイプ: 完全置換
  - Python版の既存データは全て削除されます
  - Laravel版データで完全に置き換わります
  - 画像データは移行されません（空文字として保存）

⚠️ 注意事項:
  - ユーザーデータは移行されません
  - 画像データは含まれません
  - Python版の既存データは消去されます
"""
    return summary

def main():
    """メイン実行関数"""
    print("=" * 60)
    print("🚀 Laravel → Python 完全移行ツール")
    print("=" * 60)
    
    # Laravel版SQLiteファイルのパス入力
    print("\n📁 Laravel版SQLiteファイルのパスを入力してください")
    print("例: C:\\path\\to\\laravel\\database\\database.sqlite")
    print("例: /path/to/laravel/database/database.sqlite")
    laravel_db_path = input("\n➤ パス: ").strip().replace('"', '')
    
    # ファイルの存在確認
    if not os.path.exists(laravel_db_path):
        print(f"\n❌ ファイルが見つかりません: {laravel_db_path}")
        print("パスを確認してもう一度実行してください。")
        return
    
    print(f"\n✅ ファイル確認OK: {laravel_db_path}")
    
    # 警告表示
    print("\n" + "⚠️ " * 20)
    print("警告: この操作はPython版の既存データを完全に削除します！")
    print("⚠️ " * 20)
    
    confirm = input("\n本当に実行しますか？ (yes/no): ").lower()
    if confirm not in ['yes', 'y']:
        print("\n処理を中止しました。")
        return
    
    # エクスポート実行
    print(f"\n🚀 データエクスポートを開始...")
    data, error = export_laravel_data(laravel_db_path)
    
    if data:
        # サマリー表示
        summary = create_migration_summary(data)
        print(summary)
        
        # JSONファイルとして保存
        output_filename = f'laravel_migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ エクスポート完了！")
        print(f"📁 出力ファイル: {output_filename}")
        print(f"📦 ファイルサイズ: {os.path.getsize(output_filename):,} bytes")
        
        print("\n" + "=" * 60)
        print("🎯 次の手順:")
        print("=" * 60)
        print("1. Python版アプリを起動")
        print("   コマンド: streamlit run main.py")
        print()
        print("2. 管理者でログイン")
        print("   Email: admin@hospital.jp")
        print("   Password: Okiyoshi1126")
        print()
        print("3. 「ユーザー管理」→「データバックアップ」タブを開く")
        print()
        print(f"4. '{output_filename}' をアップロード")
        print()
        print("5. 「データを復元」ボタンをクリック")
        print()
        print("6. 移行完了！")
        print("=" * 60)
        
        # 最終確認
        print(f"\n🎉 Laravel版データの移行準備が完了しました！")
        print(f"📁 ファイル: {output_filename}")
        
    else:
        print(f"\n❌ エラー: {error}")
        print("エラーの詳細を確認して、もう一度実行してください。")

if __name__ == "__main__":
    main()