import streamlit as st
import sqlite3
import pandas as pd

# 1. 페이지 기본 설정 (웹 브라우저 탭에 표시될 이름)
st.set_page_config(page_title="서천군 종자 관리 시스템", layout="centered")

# 2. 데이터베이스(장부) 연결 및 테이블(칸) 만들기 함수
def init_db():
    # seeds.db라는 파일이 없으면 만들고, 있으면 연결합니다.
    conn = sqlite3.connect('seeds.db')
    c = conn.cursor()
    # applicants라는 이름의 표를 만듭니다 (이름, 종자, 수량 칸 생성)
    c.execute('''CREATE TABLE IF NOT EXISTS applicants
                 (이름 TEXT, 종자 TEXT, 수량 INTEGER)''')
    conn.commit()
    return conn

st.title("🌾 서천군 종자 신청 관리 (DB)")
st.write("입력한 데이터는 데이터베이스에 안전하게 저장됩니다.")

# 3. 입력 양식 (사용자가 정보를 적는 곳)
with st.form("my_form"):
    st.subheader("신규 신청자 등록")
    name = st.text_input("신청인 성함")
    seed = st.selectbox("신청 종자", ["벼(삼광)", "친환경 콩", "찰옥수수", "감자"])
    amount = st.number_input("신청 수량(kg)", min_value=1, step=1)
    
    # 제출 버튼
    submitted = st.form_submit_button("장부에 기록하기")

    if submitted:
        if name: # 이름이 비어있지 않을 때만 저장
            conn = init_db()
            c = conn.cursor()
            # 장부에 한 줄 추가하는 명령어 (INSERT)
            c.execute("INSERT INTO applicants (이름, 종자, 수량) VALUES (?, ?, ?)", 
                      (name, seed, amount))
            conn.commit()
            conn.close()
            st.success(f"✅ {name}님의 신청 정보가 저장되었습니다!")
        else:
            st.error("이름을 입력해주세요.")

# 4. 저장된 데이터 불러와서 화면에 보여주기
st.divider()
st.subheader("📋 실시간 신청 현황")

conn = init_db()
# SQL 명령어로 장부 전체 내용을 읽어와서 판다스 표(DataFrame)로 변환합니다.
df = pd.read_sql_query("SELECT * FROM applicants", conn)
conn.close()

# 표를 화면에 출력 (데이터가 없으면 비어있는 상태로 나옵니다)
st.dataframe(df, use_container_width=True)