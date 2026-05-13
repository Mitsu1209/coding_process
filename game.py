import streamlit as st
import os

# --- 設定 ---
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "image")

# パーツと画像の紐付け（すべて .png）
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

# 正解ルートの設定（YesルートとNoルートの両方を許容する）
route_yes = ["開始", "タイトル表示とデータ取得", "【判断】実行ボタンが押された？", "【判断】Q1, Q2, Q3 すべて「はい」か？", "結果：身体活動量は十分です！", "終了"]
route_no = ["開始", "タイトル表示とデータ取得", "【判断】実行ボタンが押された？", "【判断】Q1, Q2, Q3 すべて「はい」か？", "結果：不足しています。", "終了"]

st.set_page_config(page_title="プログラミング体験", layout="centered")
st.title("🧩 アルゴリズム組み立てに挑戦！")

if 'flow' not in st.session_state:
    st.session_state.flow = []

# --- ① 選択エリア ---
st.subheader("① パーツを選んで追加")
cols = st.columns(4)
display_labels = [l for l in parts.keys() if l != "矢印"]

for i, label in enumerate(display_labels):
    with cols[i % 4]:
        img_path = os.path.join(IMG_DIR, parts[label])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            if st.button("追加", key=f"btn_{label}"):
                st.session_state.flow.append(label)

# --- ② 組み立てエリア ---
st.divider()
st.subheader("② あなたのアルゴリズム")

if st.button("リセット"):
    st.session_state.flow = []
    st.rerun()

for i, step in enumerate(st.session_state.flow):
    # 【追加機能】矢印のラベルを判定する
    if i > 0:
        prev_step = st.session_state.flow[i-1]
        if "【判断】" in prev_step:
            # 次のパーツが「不足しています」なら「No」、それ以外なら「Yes」と表示
            if "不足" in step:
                st.caption("　　　　↓ (No：いいえ の場合)")
            else:
                st.caption("　　　　↓ (Yes：はい の場合)")
    
    # パーツ表示
    st.image(os.path.join(IMG_DIR, parts[step]), width=220)
    
    # 矢印表示
    if i < len(st.session_state.flow) - 1:
        st.image(os.path.join(IMG_DIR, parts["矢印"]), width=40)

# --- ③ 判定エリア ---
st.divider()
if st.button("🚀 プログラムを実行する", type="primary"):
    if st.session_state.flow == route_yes:
        st.balloons()
        st.success("正解！ 身体活動が十分なケースのアルゴリズムです。")
    elif st.session_state.flow == route_no:
        st.snow() # 雪を降らせる演出
        st.info("正解！ 不足しているケースもしっかり判定できました。")
    else:
        st.error("エラー！ 順番が違うか、論理的に繋がっていません。")