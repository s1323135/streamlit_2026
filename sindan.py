import streamlit as st
import os

# アプリのタイトル
st.title("🎬 16タイプ映画キャラクター診断")
st.write("12個の質問に答えて、あなたの性格軸に基づいた映画キャラクタータイプを診断します。")

# 質問の定義 (各軸3問ずつ、計12問)
# 軸：1. R/F, 2. C/P, 3. T/L, 4. W/B
questions = [
    # 軸1: R【現実主義】 vs F【空想主義】
    {"q": "Q1: 自分が活躍している場面、どちらが想像できる？", "options": [("事件を解決する刑事や探偵", "R"), ("自分しか持ちえぬ力で犯人を逮捕するヒーロー", "F")]},
    {"q": "Q2: タイムスリップするとしたら？", "options": [("自分の生きてきた間の過去", "R"), ("自分が死んだあとのはるか先の未来", "F")]},
    {"q": "Q3: どちらのほうが好き？", "options": [("人情や現実をリアルに描いた作品", "R"), ("ファンタジーやSFなどのノンフィクション", "F")]},
    
    # 軸2: C【冷静美学】 vs P【情熱衝動】
    {"q": "Q4: 問題にどう対処する？", "options": [("計画を立てて着実に解決する", "C"), ("その場に任せてとにかく行動する", "P")]},
    {"q": "Q5: 旅行をするときの流れは？", "options": [("行く場所や時間など、しっかり予定を組んだ旅", "C"), ("予定は決めず現地の出会い次第の旅", "P")]},
    {"q": "Q6: 決断を下す基準は？", "options": [("論理的に正しいかどうか", "C"), ("心がワクワクするかどうか", "P")]},

    # 軸3: T【自由】 vs L【愛】
    {"q": "Q7: どちらの幸せを望む？", "options": [("自身の才能を磨き上げたスーパースター", "T"), ("大切な人に囲まれた日常", "L")]},
    {"q": "Q8: 大切なのは？", "options": [("自分自身の成長や夢", "T"), ("愛する人の幸せ", "L")]},
    {"q": "Q9: どちらの言葉に惹かれる？", "options": [("「道は自分で切り拓く」", "T"), ("「一人では行けない場所がある」", "L")]},

    # 軸4: W【光】 vs B【闇】
    {"q": "Q10: ルールや秩序をどう思う？", "options": [("どんなことがあっても守るべきものだと思う", "W"), ("障壁になるのであれば時には破ることも必要だ", "B")]},
    {"q": "Q11: 妄想するとしたらどっち？", "options": [("仲間と共に悪に立ち向かう正義の味方", "W"), ("日常を陰から守るダークヒーロー", "B")]},
    {"q": "Q12: 世界をどう変えたい？", "options": [("平和と秩序を守りたい", "W"), ("壊して新しいものを作りたい", "B")]},
]

# セッション状態（進捗とスコア）の初期化
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"R": 0, "F": 0, "C": 0, "P": 0, "T": 0, "L": 0, "W": 0, "B": 0}

# 診断フェーズ
if st.session_state.step < len(questions):
    # 進捗の表示 (機能追加1: st.progress)
    progress = st.session_state.step / len(questions)
    st.progress(progress)
    st.write(f"進捗: {st.session_state.step + 1} / {len(questions)}")

    q_data = questions[st.session_state.step]
    st.subheader(q_data["q"])
    
    # 選択肢をボタンで表示 (機能追加2: st.button)
    for label, trait in q_data["options"]:
        if st.button(label, key=f"btn_{st.session_state.step}_{trait}", use_container_width=True):
            # スコアを加算 (機能追加3: st.session_state)
            st.session_state.scores[trait] += 1
            st.session_state.step += 1
            st.rerun()

# 結果表示フェーズ
else:
    # 各軸の判定
    s = st.session_state.scores
    res1 = "R" if s["R"] >= s["F"] else "F" # 同点の場合Rを優先
    res2 = "C" if s["C"] >= s["P"] else "P" # 同点の場合Cを優先
    res3 = "T" if s["T"] > s["L"] else "L"
    res4 = "W" if s["W"] > s["B"] else "B"
    
    type_code = f"{res1}{res2}{res3}{res4}"
    
    def get_image_path(filename):
        """ファイルが存在するか確認し、存在しなければプレースホルダーURLを返す"""
        # 実行環境によってパスが変わるため、複数の候補地をチェックする
        possible_paths = [
            filename, # 実行ディレクトリ直下
            os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), # スクリプトと同じ場所
            os.path.join("eigasindan4", filename), # サブフォルダ内
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "eigasindan4", filename) # スクリプト下のサブフォルダ
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        # ファイルが見つからない場合は、デバッグ用にダミー画像を返す
        return f"https://placehold.jp/24/cccccc/ffffff/300x300.png?text={filename}+Not+Found"

    # 16タイプの詳細データマッピング
    type_details = {
        "RCTW": {"name": "アンディ(ショーシャンクの空に)", "desc": "不条理で過酷な現実に耐えながらも希望を捨てず、知性と不屈の忍耐で自由を勝ち取る。静かなる意志の強さを持つタイプです。", "image": get_image_path("RCTW.jpg")}, # 現実主義, 冷静美学, 自由, 光
        "RCTB": {"name": "フランク(キャッチ・ミー・イフ・ユーキャン)", "desc": "天才的な頭脳と分析力を持ち、ルールを巧みにすり抜けながら、スリルと孤独の間に生きる知性派の逃亡者です。", "image": get_image_path("RCTB.jpg")}, # 現実主義, 冷静美学, 自由, 闇
        "RCLW": {"name": "ミランダ(プラダを着た悪魔)", "desc": "プロフェッショナルとしての圧倒的な美学と厳格さを持ちながらも、愛に仕事と組織を頂点へと導く、妥協を許さないカリスマリーダーです。", "image": get_image_path("RCLW.jpg")},
        "RCLB": {"name": "レオン(leon)", "desc": "冷徹なプロの殺し屋としての技術を持ちながら、心の奥底には不器用な愛を秘めている。非情な現実と純粋な絆の間で生きる、哀愁漂う実力者です。", "image": get_image_path("RCLB.jpg")}, # 現実主義, 冷静美学, 愛, 闇
        "RPTW": {"name": "ニーマン(セッション)", "desc": "限界を超えようとする圧倒的な情熱を持ち、自らの美学を磨き上げるためなら狂気すら辞さない、凄まじい向上心の持ち主です。", "image": get_image_path("RPTW.jpg")}, # 現実主義, 情熱衝動, 自由, 光
        "RPTB": {"name": "タイラー・ダーテン(ファイト・クラブ)", "desc": "虚飾に満ちた現実に牙を剥き、人間の本能的な衝動を解放する。破壊の先に自由を見出す、カリスマ的な反逆児タイプです。", "image": get_image_path("RPTB.jpg")}, # 現実主義, 情熱衝動, 自由, 闇
        "RPLW": {"name": "アン王女(ローマの休日)", "desc": "日常を飛び出し束の間の自由と情熱的な恋を求めた。気品溢れる振る舞いの中に、愛を大切にする熱い心を秘めています。", "image": get_image_path("RPLW.jpg")}, # 現実主義, 情熱衝動, 愛, 光
        "RPLB": {"name": "ベイビー(ベイビー・ドライバー)", "desc": "犯罪の世界という過酷な現実の中で、音楽への情熱と愛する人を守るために生きる。卓越したセンスと繊細な心を持つドライバーです。", "image": get_image_path("RPLB.jpg")}, # 現実主義, 情熱衝動, 愛, 闇
        "FCTW": {"name": "トゥルーマン(トゥルーマン・ショー)", "desc": "虚構の世界に違和感を感じ、冷静な観察眼で真実を探求し続ける。偽りの平和よりも、自由を求めて旅立つ勇敢な人です。", "image": get_image_path("FCTW.jpg")}, # 空想主義, 冷静美学, 自由, 光
        "FCTB": {"name": "デッカード(ブレードランナー)", "desc": "退廃的な未来を舞台に、職務と己の正義の間で揺れる。冷静な判断力の中に、拭いきれない憂いと孤独を抱えた捜査官です。", "image": get_image_path("FCTB.jpg")}, # 空想主義, 冷静美学, 自由, 闇
        "FCLW": {"name": "マルコム＆コール(シックスセンス)", "desc": "死者の姿が見えるという空想的な状況下で、静かな知恵と深い愛をもって魂の救済を試みる。優しさと真理を見極める目を持つタイプです。", "image": get_image_path("FCLW.jpg")}, # 空想主義, 冷静美学, 愛, 光
        "FCLB": {"name": "ジョー・ブラック(ジョー・ブラックによろしく)", "desc": "死神という超常的な存在でありながら、人間の愛に触れ、冷静にその美しさを学んでいく。神秘的で気品に満ちたキャラクターです。", "image": get_image_path("FCLB.jpg")}, # 空想主義, 冷静美学, 愛, 闇
        "FPTW": {"name": "ハリー・ポッター", "desc": "魔法の世界で、友情と勇気を武器に宿命へ立ち向かう。選ばれし運命を背負いながらも、情熱で仲間を守り抜く物語の主人公です。", "image": get_image_path("FPTW.jpg")}, # 空想主義, 情熱衝動, 自由, 光
        "FPTB": {"name": "ネオ(マトリックス)", "desc": "仮想現実の中で目覚め、世界の法則すら書き換える情熱と力を持つ。自由を求めて戦う、覚醒した知性と行動力の持ち主です。", "image": get_image_path("FPTB.jpg")}, # 空想主義, 情熱衝動, 自由, 闇
        "FPLW": {"name": "エドワード(シザーハンズ)", "desc": "おとぎ話のような存在でありながら、純粋無垢な愛と豊かな感情を持つ。孤独の中で美しさを見出す、心優しい芸術家タイプです。", "image": get_image_path("FPLW.jpg")}, # 空想主義, 情熱衝動, 愛, 光
        "FPLB": {"name": "ジョン・コンスタンティン(コンスタンティン)", "desc": "悪魔が跋扈する世界で、自らの罪と対峙しながら愛と救済のために戦う。皮肉屋で影がありながらも、情熱を秘めたヒーローです。", "image": get_image_path("FPLB.jpg")} # 空想主義, 情熱衝動, 愛, 闇
    }
    
    result = type_details.get(type_code, {"name": "未知のキャラクター", "desc": "詳細なデータが見つかりませんでした。", "image": get_image_path("default.png")})
    
    st.success("🎉 診断が完了しました！")

    # カラムを使って画像と解説を横並びに表示
    col_img, col_info = st.columns([1, 1.2])
    
    with col_img:
        # width指定の代わりに use_container_width=True を使うと、カラムの幅に自動でフィットします
        st.image(result["image"], use_container_width=True)
    
    with col_info:
        st.subheader("あなたの映画キャラクタータイプは...")
        st.header(f"「{type_code}：{result['name']}」")
        st.write(result["desc"])
    
    # 軸の説明を表示
    st.info(f"""
    【診断結果の分析】
    - 基盤: {"現実主義(R)" if res1=="R" else "空想主義(F)"}
    - 美学: {"冷静美学(C)" if res2=="C" else "情熱衝動 (P)"}
    - 優先: {"自由・夢(T)" if res3=="T" else "愛(L)"}
    - 属性: {"光(W)" if res4=="W" else "影(B)"}
    """)
    
    if st.button("最初からやり直す"):
        st.session_state.step = 0
        st.session_state.scores = {"R": 0, "F": 0, "C": 0, "P": 0, "T": 0, "L": 0, "W": 0, "B": 0}
        st.rerun()
