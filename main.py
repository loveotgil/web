import streamlit as st
import pandas as pd
import random

# --- הגדרת עמוד ותצורת RTL ---
st.set_page_config(
    page_title="אהבת המשחק - Love The Game",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- מילון תרגומים לשפות (עברית, אנגלית, רוסית) ---
TRANSLATIONS = {
    "עברית": {
        "title": "אהבת המשחק",
        "subtitle": "הבית של קהילת משחקי הלוח, הקלפים והטורנירים בישראל",
        "nav_home": "🏠 בית ורישום לליגה",
        "nav_league": "🏆 טבלת הליגה",
        "nav_rules": "📜 חוקים וטורניר",
        "nav_admin": "⚙️ פאנל ניהול",
        "reg_header": "הרשמה מהירה לליגה ולטורנירים",
        "choose_social": "התחבר באמצעות:",
        "username_label": "בחר שם משתמש (כינוי בליגה):",
        "email_label": "כתובת אימייל:",
        "register_btn": "הירשם עכשיו!",
        "success_reg": "🎉 כל הכבוד! נרשמת בהצלחה לליגה!",
        "your_player_id": "מספר השחקן שלך בליגה:",
        "league_table_title": "טבלת השחקנים הרשומים בליגה",
        "rules_title": "חוקי הטורניר והסברים",
        "rules_placeholder": "כאן יופיעו בהמשך חוקי המשחקים, נהלי הטורניר ולוחות הזמנים המעודכנים.",
        "admin_title": "פאנל ניהול - ניהול שחקנים וניקוד",
        "admin_pass": "סיסמת מנהל:",
        "admin_login_err": "סיסמה שגויה",
        "select_player": "בחר שחקן לעדכון:",
        "new_score": "עדכן ניקוד חדש:",
        "update_btn": "שמור שינויים",
        "score_updated": "הניקוד עודכן בהצלחה!",
        "total_players": "סה״כ שחקנים רשומים:",
        "lang_select": "בחר שפה / Language / Язык"
    },
    "English": {
        "title": "Love The Game",
        "subtitle": "The home of board games, card games, and tournaments community in Israel",
        "nav_home": "🏠 Home & Registration",
        "nav_league": "🏆 League Standings",
        "nav_rules": "📜 Rules & Tournament",
        "nav_admin": "⚙️ Admin Panel",
        "reg_header": "Quick Registration for League & Tournaments",
        "choose_social": "Sign in with:",
        "username_label": "Choose Username (Nickname):",
        "email_label": "Email Address:",
        "register_btn": "Register Now!",
        "success_reg": "🎉 Congratulations! You successfully registered for the league!",
        "your_player_id": "Your League Player ID:",
        "league_table_title": "Registered League Players",
        "rules_title": "Tournament Rules & Information",
        "rules_placeholder": "Game rules, tournament guidelines and updated schedules will be published here soon.",
        "admin_title": "Admin Panel - Manage Players & Scores",
        "admin_pass": "Admin Password:",
        "admin_login_err": "Incorrect password",
        "select_player": "Select player to update:",
        "new_score": "Update new score/points:",
        "update_btn": "Save Changes",
        "score_updated": "Score updated successfully!",
        "total_players": "Total Registered Players:",
        "lang_select": "Language"
    },
    "Русский": {
        "title": "Любовь к Игре (Love The Game)",
        "subtitle": "Дом сообщества настольных игр, карточных игр и турниров в Израиле",
        "nav_home": "🏠 Главная и Регистрация",
        "nav_league": "🏆 Таблица Лиги",
        "nav_rules": "📜 Правила и Турнир",
        "nav_admin": "⚙️ Панель Администратора",
        "reg_header": "Быстрая регистрация в лигу и турниры",
        "choose_social": "Войти через:",
        "username_label": "Выберите имя пользователя (ник):",
        "email_label": "Электронная почта:",
        "register_btn": "Зарегистрироваться!",
        "success_reg": "🎉 Поздравляем! Вы успешно зарегистрировались в лиге!",
        "your_player_id": "Ваш номер игрока в лиге:",
        "league_table_title": "Зарегистрированные игроки лиги",
        "rules_title": "Правила турнира и информация",
        "rules_placeholder": "Правила игр, регламент турнира и расписание будут опубликованы здесь позже.",
        "admin_title": "Панель управления - Управление игроками и очками",
        "admin_pass": "Пароль администратора:",
        "admin_login_err": "Неверный пароль",
        "select_player": "Выберите игрока для обновления:",
        "new_score": "Новый счет / очки:",
        "update_btn": "Сохранить изменения",
        "score_updated": "Счет успешно обновлен!",
        "total_players": "Всего зарегистрированных игроков:",
        "lang_select": "Язык"
    }
}

# --- הגדרת בסיס נתונים ב-Session State (שחקנים לדוגמה) ---
if 'players_db' not in st.session_state:
    st.session_state.players_db = pd.DataFrame([
        {"player_id": "LOTG-1001", "username": "LiranGamer", "email": "liran@example.com", "provider": "Google", "score": 45},
        {"player_id": "LOTG-1002", "username": "DiceQueen", "email": "queen@example.com", "provider": "TikTok", "score": 38},
        {"player_id": "LOTG-1003", "username": "BoardMaster", "email": "master@example.com", "provider": "Facebook", "score": 52},
    ])

# --- סרגלים צדדיים והגדרות שפה ---
st.sidebar.image("https://storage.googleapis.com/gweb-unify-prod-live-bucket/images/gameslover_logo.original.png", width=120) # ניתן להחליף בלוגו שלך או תמונה מקומית
lang = st.sidebar.selectbox("🌐 Choose Language / שפה / Язык", ["עברית", "English", "Русский"])
t = TRANSLATIONS[lang]

# הגדרת כיוון טקסט (RTL לעברית, LTR לאחרים)
if lang == "עברית":
    st.markdown("""
        <style>
            body, div, span, p, h1, h2, h3, h4, h5, h6 {
                direction: rtl;
                text-align: right;
            }
        </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
page = st.sidebar.radio("ניווט באתר", [t["nav_home"], t["nav_league"], t["nav_rules"], t["nav_admin"]])

# --- כותרת ראשית ולוגו ---
col_logo, col_title = st.sidebar.columns([1, 3]) if False else (None, None)
st.title(f"🎲 {t['title']}")
st.subheader(t['subtitle'])
st.markdown("---")

# ==================== דף בית ורישום (Home & Registration) ====================
if page == t["nav_home"]:
    st.header(t["reg_header"])
    
    with st.form("registration_form"):
        st.markdown(f"**{t['choose_social']}**")
        social_provider = st.radio("Provider", ["Google 🌐", "Facebook 👤", "TikTok 🎵"], horizontal=True)
        
        username = st.text_input(t["username_label"])
        email = st.text_input(t["email_label"])
        
        submitted = st.form_submit_button(t["register_btn"])
        
        if submitted:
            if not username or not email:
                st.error("אנא מלא את כל השדות / Please fill in all fields" if lang=="עברית" else "Please fill all fields")
            elif username in st.session_state.players_db["username"].values:
                st.error("שם המשתמש כבר תפוס, בחר כינוי אחר. / Username already taken.")
            else:
                new_id = f"LOTG-{random.randint(1004, 9999)}"
                new_row = pd.DataFrame([{
                    "player_id": new_id,
                    "username": username,
                    "email": email,
                    "provider": social_provider.split()[0],
                    "score": 10  בונוס רישום ראשוני
                }])
                st.session_state.players_db = pd.concat([st.session_state.players_db, new_row], ignore_index=True)
                
                st.success(t["success_reg"])
                st.balloons()
                st.info(f"**{t['your_player_id']}** `{new_id}`")

    st.markdown("---")
    st.metric(label=t["total_players"], value=len(st.session_state.players_db))

# ==================== טבלת הליגה (League Standings) ====================
elif page == t["nav_league"]:
    st.header(t["league_table_title"])
    
    # מיון השחקנים לפי ניקוד בסדר יורד
    sorted_df = st.session_state.players_db.sort_values(by="score", ascending=False).reset_index(drop=True)
    sorted_df.index = sorted_df.index + 1  # דירוג מתחיל מ-1
    
    # תצוגה טבלאית יפה
    st.dataframe(
        sorted_df[["player_id", "username", "provider", "score"]],
        column_config={
            "player_id": "מספר שחקן (ID)",
            "username": "שם משתמש",
            "provider": "אמצעי רישום",
            "score": "ניקוד ליגה"
        },
        use_container_width=True
    )

# ==================== חוקים וטורניר (Rules) ====================
elif page == t["nav_rules"]:
    st.header(t["rules_title"])
    st.info(t["rules_placeholder"])
    
    st.markdown("""
    ### מבנה הטורנירים הקרובים:
    - **טורניר פתיחת עונה:** משחקי אסטרטגיה וקופסאות בסיס.
    - **שיטת הניקוד:** ניצחון מעניק 10 נקודות, השתתפות מעניקה 3 נקודות.
    """)

# ==================== פאנל ניהול (Admin Panel) ====================
elif page == t["nav_admin"]:
    st.header(t["admin_title"])
    
    admin_password = st.text_input(t["admin_pass"], type="password")
    
    # סיסמת ניהול פשוטה להדגמה (ניתן לשנות לכל סיסמה שתרצה)
    if admin_password == "admin123":
        st.success("התחברת בהצלחה כמנהל מערכת!")
        
        player_list = st.session_state.players_db["username"].tolist()
        selected_player = st.selectbox(t["select_player"], player_list)
        
        current_score = int(st.session_state.players_db.loc[st.session_state.players_db["username"] == selected_player, "score"].values[0])
        
        new_score_val = st.number_input(t["new_score"], value=current_score, step=1)
        
        if st.button(t["update_btn"]):
            st.session_state.players_db.loc[st.session_state.players_db["username"] == selected_player, "score"] = new_score_val
            st.success(t["score_updated"])
            st.rerun()
            
        st.markdown("### רשימת שחקנים מלאה לניהול:")
        st.dataframe(st.session_state.players_db, use_container_width=True)
        
    elif admin_password != "":
        st.error(t["admin_login_err"])

