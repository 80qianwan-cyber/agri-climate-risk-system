
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.graph_objects as go


# =========================
# 页面配置
# =========================

st.set_page_config(
    page_title="藕大夫 - 农业极端气候智能诊断系统",
    page_icon="🌱",
    layout="wide"
)


# =========================
# 标题
# =========================

st.title("🌱 藕大夫")
st.subheader(
    "基于多模态大模型与知识图谱融合的农业极端气候智能诊断与决策系统"
)

st.divider()


# =========================
# 左侧 输入模块
# =========================

st.sidebar.header("农业环境信息输入")


crop = st.sidebar.selectbox(
    "作物类型",
    [
        "莲藕",
        "水稻",
        "小麦",
        "玉米"
    ]
)


region = st.sidebar.selectbox(
    "种植区域",
    [
        "广东省",
        "湖南省",
        "湖北省",
        "江苏省"
    ]
)


temperature = st.sidebar.slider(
    "平均温度（℃）",
    20,
    45,
    35
)


rainfall = st.sidebar.slider(
    "降雨量（mm）",
    0,
    300,
    50
)


humidity = st.sidebar.slider(
    "土壤湿度（%）",
    10,
    100,
    40
)


days = st.sidebar.slider(
    "连续异常天气天数",
    0,
    30,
    10
)


uploaded_file = st.sidebar.file_uploader(
    "上传作物图片",
    type=["jpg", "png", "jpeg"]
)



# =========================
# 图片展示
# =========================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📷 作物图像信息")

    if uploaded_file:

        img = Image.open(uploaded_file)

        st.image(
            img,
            caption="上传的作物图片",
            width=350
        )

    else:

        st.info(
            "未上传图片，系统将基于环境信息进行模拟诊断"
        )


# =========================
# 风险诊断模型（模拟）
# =========================

def risk_prediction(
        temp,
        rain,
        hum,
        abnormal_days
):

    score = 0

    if temp >= 35:
        score += 0.35

    if hum < 40:
        score += 0.30

    if rain < 30:
        score += 0.15

    if abnormal_days > 10:
        score += 0.20


    score = min(score, 0.99)


    return round(score, 2)



risk_score = risk_prediction(
    temperature,
    rainfall,
    humidity,
    days
)



with col2:

    st.subheader("🤖 多模态智能诊断结果")


    if risk_score > 0.7:

        level = "高风险"

    elif risk_score > 0.4:

        level = "中风险"

    else:

        level = "低风险"



    st.metric(
        "极端气候风险评分",
        risk_score
    )


    st.success(
        f"当前诊断结果：{level}"
    )



# =========================
# 风险仪表盘
# =========================


st.divider()

st.subheader("📊 风险可视化")


fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=risk_score*100,
        title={
            "text":"农业气候风险指数"
        },
        gauge={
            "axis":{
                "range":[0,100]
            }
        }
    )
)


st.plotly_chart(fig)



# =========================
# 知识图谱推理
# =========================

st.divider()

st.subheader("🧠 知识图谱推理路径")


graph_data = pd.DataFrame(
    {
        "节点":
        [
            "极端高温",
            "水分蒸发增加",
            "水分胁迫",
            "莲藕生长受限",
            "产量下降"
        ],

        "关系":
        [
            "导致",
            "诱发",
            "影响",
            "造成",
            "结果"
        ]
    }
)


st.table(graph_data)



# =========================
# 决策建议
# =========================


st.divider()

st.subheader("🌾 AI智能决策建议")


if level == "高风险":

    advice = [
        "增加灌溉频率，缓解水分胁迫",
        "加强田间温湿度监测",
        "提前开展病虫害风险防控"
    ]

elif level == "中风险":

    advice = [
        "持续关注天气变化",
        "优化水肥管理",
        "加强作物状态观察"
    ]

else:

    advice = [
        "保持正常农业管理",
        "持续监测环境变化"
    ]


for i,a in enumerate(advice,1):

    st.write(
        f"{i}. {a}"
    )



# =========================
# 页脚
# =========================

st.divider()

st.caption(
    "本系统为农业极端气候智能诊断原型平台，融合环境数据分析、多模态信息处理与知识图谱推理方法。"
)

