import streamlit as st
import json
import os

FILE = 'records.json'
def load_records():
    if not os.path.exists(FILE):
        return []
    with open(FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_records(records):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

st.title('💰 我的零用錢記帳本')

records = load_records()

with st.form('add_form', clear_on_submit=True):
    date = st.date_input('日期')
    kind = st.radio('收入還是支出？', ['支出', '收入'], horizontal=True)
    category = st.selectbox('類別', ['飲食', '交通', '娛樂', '文具', '零用錢', '其他'])
    item = st.text_input('項目', placeholder='例如：珍奶')
    amount = st.number_input('金額', min_value=0, step=10)
    submitted = st.form_submit_button('記下來')

if submitted:
    if item == '' or amount == 0:
        st.error('項目和金額都要填喔！')
    else:
        records.append({'日期': str(date), '收支': kind, '類別': category,
                        '項目': item, '金額': amount})
        save_records(records)
        st.success(f'已記下：{item} {amount} 元')

# 計算總收入、總支出
income = 0
expense = 0
for r in records:
    if r['收支'] == '收入':
        income += r['金額']
    else:
        expense += r['金額']

# 三個數字左右並排
col1, col2, col3 = st.columns(3)
col1.metric('總收入', f'{income} 元')
col2.metric('總支出', f'{expense} 元')
col3.metric('餘額', f'{income - expense} 元')

st.subheader('明細')
st.dataframe(records)





