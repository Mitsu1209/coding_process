import streamlit as st
import os
import random

# --- 1. 基本設定：画像の場所を指定 ---
# プログラムと同じ場所にある "image" フォルダを参照します
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "image")

# パーツ名とファイル名の紐付け（すべて .png）
parts = {
    "開始": "画像5.png",
    "タイトル表示とデータ取得": "画像1.png",
    "【判断】実行ボタンが押された？": "画像3.png",
    "【判断】Q1, Q2, Q3 すべて「はい」か？": "画像6.png",
    "結果：身体活動量は十分です！": "画像8.png",
    "結果：不足しています。": "画像2.png",
    "終了": "画像4.png",
    "矢印": "画像9.png"
}

# 正解ルートの定義
route_yes = ["開始", "タイトル表示とデータ取得", "【判断】実行ボタンが押された？", "【判断】Q1, Q2, Q3 すべて「はい」か？", "結果：身体活動量は十分です！", "終了"]
route_no = ["開始", "タイトル表示とデータ取得", "【判断】実行ボタンが押された？", "【判断】Q1, Q2, Q3 すべて「はい」か？", "結果：不足しています。", "終了"]

# ページの設定
st.set_page_config(page_title="プログラミング体験", layout="centered")
st.title("🧩 アルゴリズム組み立てに挑戦！")
st.write("流れを完成させよう！")

# --- 2. 状態の管理（セッションステート） ---
# 組み立てたパーツの記録
if 'flow' not in st.session_state:
    st.session_state.flow = []

# ボタンの並び順の記録（ランダム化）
if 'shuffled_labels' not in st.session_state:
    all_labels = [l for l in parts.keys() if l != "矢印"]
    st.session_state.shuffled_labels = random.sample(all_labels, len(all_labels))

# --- 3. ① パーツ選択エリア（ランダム表示） ---
st.subheader("① パーツを選んで追加（順番はランダムです）")

# リセットボタンの処理
if st.button("リセットして並び替える"):
    st.session_state.flow = []
    # 並び順を新しくシャッフル
    all_labels = [l for l in parts.keys() if l != "矢印"]
    st.session_state.shuffled_labels = random.sample(all_labels, len(all_labels))
    st.rerun()

# 4列でパーツを表示
cols = st.columns(4)
for i, label in enumerate(st.session_state.shuffled_labels):
    with cols[i % 4]:
        img_path = os.path.join(IMG_DIR, parts[label])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            if st.button("追加", key=f"btn_{label}"):
                st.session_state.flow.append(label)
        else:
            st.error(f"画像不足: {parts[label]}")

# --- 4. ② 組み立てエリア（ビジュアル表示） ---
st.divider()
st.subheader("② あなたのアルゴリズム")

for i, step in enumerate(st.session_state.flow):
    # 分岐ラベルの自動表示（Yes/No）
    if i > 0:
        prev_step = st.session_state.flow[i-1]
        if "【判断】" in prev_step:
            if "不足" in step:
                st.caption("　　　　↓ (いいえ：No の場合)")
            else:
                st.caption("　　　　↓ (はい：Yes の場合)")
    
    # 現在のパーツ画像を表示
    st.image(os.path.join(IMG_DIR, parts[step]), width=220)
    
    # 次のパーツがある場合は矢印を表示
    if i < len(st.session_state.flow) - 1:
        st.image(os.path.join(IMG_DIR, parts["矢印"]), width=40)

# --- 5. ③ 判定エリア ---
st.divider()
if st.button("🚀 プログラムを実行する", type="primary"):
    if not st.session_state.flow:
        st.warning("まずはパーツを並べてみましょう。")
    elif st.session_state.flow == route_yes:
        st.balloons()
        st.success("正解！ 身体活動が十分なケースの判定に成功しました。")
    elif st.session_state.flow == route_no:
        st.snow()
        st.info("正解！ 不足しているケースもしっかり判定できました。")
    else:
        st.error("エラー！ 順番が違うか、論理的に繋がっていないようです。")