"""
飞书 Bot 管理后台 (Streamlit)
用于管理员工 Skill 配置、查看飞书 Bot 状态
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

API_BASE_URL = "http://localhost:8001"

st.set_page_config(
    page_title="飞书 Bot 管理后台",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .skill-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .employee-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "refresh_key" not in st.session_state:
        st.session_state.refresh_key = 0


def check_api_connection() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def check_feishu_connection() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/feishu/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_skill_list() -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE_URL}/admin/skills", timeout=10)
        if response.status_code == 200:
            return response.json().get("skills", [])
        return []
    except:
        return []


def get_employee_list() -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE_URL}/admin/employees", timeout=10)
        if response.status_code == 200:
            return response.json().get("employees", [])
        return []
    except:
        return []


def create_skill(data: Dict) -> Dict:
    try:
        response = requests.post(f"{API_BASE_URL}/admin/skills", json=data, timeout=10)
        return {"success": response.status_code == 200, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_skill(skill_id: str, data: Dict) -> Dict:
    try:
        response = requests.put(f"{API_BASE_URL}/admin/skills/{skill_id}", json=data, timeout=10)
        return {"success": response.status_code == 200, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_skill(skill_id: str) -> Dict:
    try:
        response = requests.delete(f"{API_BASE_URL}/admin/skills/{skill_id}", timeout=10)
        return {"success": response.status_code == 200}
    except Exception as e:
        return {"success": False, "error": str(e)}


def register_employee(data: Dict) -> Dict:
    try:
        response = requests.post(f"{API_BASE_URL}/admin/employees", json=data, timeout=10)
        return {"success": response.status_code == 200, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def bind_employee_skill(feishu_user_id: str, skill_id: str) -> Dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin/employees/{feishu_user_id}/bind-skill",
            json={"skill_id": skill_id},
            timeout=10,
        )
        return {"success": response.status_code == 200}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_feishu_sessions(limit: int = 50) -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE_URL}/admin/feishu/sessions?limit={limit}", timeout=10)
        if response.status_code == 200:
            return response.json().get("sessions", [])
        return []
    except:
        return []


def render_status_tab():
    st.header("飞书 Bot 状态")

    col1, col2, col3 = st.columns(3)

    api_ok = check_api_connection()
    feishu_ok = check_feishu_connection()

    with col1:
        if api_ok:
            st.success("API 服务已连接")
        else:
            st.error("API 服务未连接")
            st.info("请先启动后端服务: python -m api.server")

    with col2:
        if feishu_ok:
            st.success("飞书 Bot 已初始化")
        else:
            st.warning("飞书 Bot 未初始化")
            st.info("请在 .env 中配置飞书应用参数")

    with col3:
        try:
            resp = requests.get(f"{API_BASE_URL}/feishu/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                st.info(f"Bot 名称: {data.get('bot_name', 'N/A')}")
        except:
            st.info("Bot 信息不可用")

    st.divider()

    st.subheader("飞书应用配置检查")
    try:
        with open(".env", "r", encoding="utf-8") as f:
            env_content = f.read()

        config_map = {
            "FEISHU_APP_ID": "飞书应用 App ID",
            "FEISHU_APP_SECRET": "飞书应用 App Secret",
            "FEISHU_VERIFICATION_TOKEN": "飞书 Verification Token",
        }

        for key, label in config_map.items():
            if key in env_content:
                for line in env_content.splitlines():
                    if line.startswith(key) and "=" in line:
                        value = line.split("=", 1)[1].strip()
                        if value:
                            st.success(f"{label}: 已配置 ({value[:8]}...)")
                        else:
                            st.error(f"{label}: 未填写")
                        break
            else:
                st.info(f"{label}: 未在 .env 中配置")
    except FileNotFoundError:
        st.warning(".env 文件不存在")
    except Exception as e:
        st.error(f"读取配置失败: {e}")

    st.divider()

    st.subheader("快速测试")
    st.info("在飞书中向机器人发送消息，即可测试 Bot 是否正常工作")

    st.markdown("""
    **测试步骤：**
    1. 确保后端服务已启动
    2. 在飞书中搜索并添加机器人
    3. 向机器人发送一条消息
    4. 观察是否收到回复
    """)


def render_skills_tab():
    st.header("Skill 模板管理")

    skills = get_skill_list()
    st.metric("已配置 Skill", len(skills))

    tab1, tab2 = st.tabs(["Skill 列表", "新建 Skill"])

    with tab1:
        if not skills:
            st.info("暂无 Skill 模板。系统会自动创建默认模板。")
        else:
            for skill in skills:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        style_emoji = {
                            "rigorous": "🔬",
                            "efficient": "⚡",
                            "beginner": "🌱",
                            "balanced": "⚖️",
                        }
                        emoji = style_emoji.get(skill.get("answer_style", ""), "")
                        st.markdown(
                            f"**{emoji} {skill.get('name', '未知')}** "
                            f"`{skill.get('id', '')}`"
                        )
                        st.caption(f"风格: {skill.get('answer_style', 'N/A')} | "
                                   f"温度: {skill.get('temperature', 0)} | "
                                   f"优先级: {skill.get('priority', 0)}")
                        st.caption(f"描述: {skill.get('description', '无')}")
                    with col2:
                        if st.button("编辑", key=f"edit_{skill['id']}"):
                            st.session_state[f"edit_skill_{skill['id']}"] = True
                        if skill["id"] not in ("skill_default", "skill_rigorous", "skill_efficient", "skill_beginner"):
                            if st.button("删除", key=f"del_{skill['id']}"):
                                result = delete_skill(skill["id"])
                                if result["success"]:
                                    st.success("删除成功")
                                    st.rerun()
                                else:
                                    st.error(f"删除失败: {result.get('error')}")

                    if st.session_state.get(f"edit_skill_{skill['id']}"):
                        with st.form(key=f"form_{skill['id']}"):
                            name = st.text_input("名称", value=skill.get("name", ""))
                            description = st.text_input("描述", value=skill.get("description", ""))
                            answer_style = st.selectbox(
                                "回答风格",
                                ["rigorous", "efficient", "beginner", "balanced"],
                                index=["rigorous", "efficient", "beginner", "balanced"].index(
                                    skill.get("answer_style", "balanced")
                                ),
                            )
                            temperature = st.slider("温度", 0.0, 1.5, float(skill.get("temperature", 0.7)), 0.1)
                            max_tokens = st.number_input("最大 Token", 256, 8192, skill.get("max_tokens", 2048))
                            priority = st.number_input("优先级", 0, 100, skill.get("priority", 0))
                            system_prompt = st.text_area(
                                "系统提示词补充",
                                value=skill.get("system_prompt_suffix", ""),
                                height=200,
                            )
                            knowledge_scope_str = st.text_input(
                                "知识范围（逗号分隔）",
                                value=", ".join(skill.get("knowledge_scope", [])),
                            )

                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.form_submit_button("保存修改"):
                                    knowledge_scope = [s.strip() for s in knowledge_scope_str.split(",") if s.strip()]
                                    result = update_skill(skill["id"], {
                                        "name": name,
                                        "description": description,
                                        "answer_style": answer_style,
                                        "temperature": temperature,
                                        "max_tokens": max_tokens,
                                        "priority": priority,
                                        "system_prompt_suffix": system_prompt,
                                        "knowledge_scope": knowledge_scope,
                                    })
                                    if result["success"]:
                                        st.success("更新成功")
                                        st.session_state[f"edit_skill_{skill['id']}"] = False
                                        st.rerun()
                                    else:
                                        st.error(f"更新失败: {result.get('error')}")
                            with col_b:
                                if st.form_submit_button("取消"):
                                    st.session_state[f"edit_skill_{skill['id']}"] = False

                    st.divider()

    with tab2:
        with st.form("new_skill_form"):
            st.subheader("创建新 Skill")
            name = st.text_input("Skill 名称 *", placeholder="例如: 财务分析型")
            description = st.text_input("描述", placeholder="简述这个 Skill 的特点")
            answer_style = st.selectbox(
                "回答风格 *",
                [
                    ("rigorous", "严谨型 - 详细、有逻辑、引用来源"),
                    ("efficient", "高效型 - 框架式、点到为止"),
                    ("beginner", "新人友好型 - 通俗易懂、带比喻"),
                    ("balanced", "平衡型 - 标准风格"),
                ],
                format_func=lambda x: x[1],
            )
            temperature = st.slider("LLM 温度", 0.0, 1.5, 0.7, 0.1,
                                   help="较低=更确定性回答，较高=更有创造性")
            max_tokens = st.number_input("最大 Token 数", 256, 8192, 2048)
            priority = st.number_input("优先级", 0, 100, 5)
            system_prompt_suffix = st.text_area(
                "系统提示词（追加到基础提示词后）",
                value="",
                height=200,
                placeholder="在这里写你对 AI 回答风格的具体要求...",
            )
            knowledge_scope_str = st.text_input(
                "知识范围标签（逗号分隔）",
                placeholder="例如: 技术文档, 操作手册, 财务报告",
                help="设置后，检索时会优先匹配这些标签的文档",
            )

            submitted = st.form_submit_button("创建 Skill", type="primary")
            if submitted:
                if not name:
                    st.error("请输入 Skill 名称")
                else:
                    knowledge_scope = [s.strip() for s in knowledge_scope_str.split(",") if s.strip()]
                    result = create_skill({
                        "name": name,
                        "description": description,
                        "answer_style": answer_style[0],
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "priority": priority,
                        "system_prompt_suffix": system_prompt_suffix,
                        "knowledge_scope": knowledge_scope,
                    })
                    if result["success"]:
                        st.success("Skill 创建成功！")
                        st.rerun()
                    else:
                        st.error(f"创建失败: {result.get('error')}")


def render_employees_tab():
    st.header("员工管理")

    employees = get_employee_list()
    skills = get_skill_list()
    skill_map = {s["id"]: s["name"] for s in skills}

    st.metric("已注册员工", len(employees))

    tab1, tab2 = st.tabs(["员工列表", "注册员工"])

    with tab1:
        if not employees:
            st.info("暂无注册员工。员工首次在飞书中发消息时会自动注册。")
        else:
            header_cols = st.columns([2, 1.5, 2, 1, 2, 1.5])
            header_cols[0].markdown("**员工名称**")
            header_cols[1].markdown("**部门**")
            header_cols[2].markdown("**当前 Skill**")
            header_cols[3].markdown("**状态**")
            header_cols[4].markdown("**注册时间**")
            header_cols[5].markdown("**操作**")
            st.divider()
            for emp in employees:
                with st.container():
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 2, 1, 2, 1.5])
                    with col1:
                        st.write(f"**{emp.get('name', emp.get('feishu_user_id', '未知')[:16])}**")
                    with col2:
                        st.write(emp.get("department", "-"))
                    with col3:
                        skill_name = skill_map.get(emp.get("skill_id"), "未设置")
                        st.write(skill_name)
                    with col4:
                        if emp.get("is_active", True):
                            st.success("启用")
                        else:
                            st.error("禁用")
                    with col5:
                        ts = emp.get("created_at", "")
                        if ts:
                            dt = str(ts)[:19] if isinstance(ts, str) else datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
                            st.write(dt)
                        else:
                            st.write("-")
                    with col6:
                        selected_skill = st.selectbox(
                            "绑定 Skill",
                            options=[""] + [s["id"] for s in skills],
                            format_func=lambda x: skill_map.get(x, "选择 Skill...") if x else "选择 Skill...",
                            key=f"skill_{emp['feishu_user_id']}",
                        )
                        if selected_skill and selected_skill != emp.get("skill_id", ""):
                            result = bind_employee_skill(emp["feishu_user_id"], selected_skill)
                            if result["success"]:
                                st.success("已更新")
                                st.rerun()
                            else:
                                st.error("更新失败")

                    st.divider()

    with tab2:
        st.subheader("手动注册员工")
        st.caption("如果员工尚未在飞书中发过消息，可以手动注册")

        with st.form("register_employee"):
            feishu_user_id = st.text_input("飞书 Open ID *", placeholder="ou_xxx...")
            name = st.text_input("姓名")
            department = st.text_input("部门")
            skill_options = [""] + list(skill_map.values())
            skill_names = list(skill_map.values())
            skill_ids = [""] + [s["id"] for s in skills]

            selected_skill_name = st.selectbox("初始 Skill", options=skill_ids,
                                              format_func=lambda x: skill_map.get(x, "默认") if x else "默认")

            submitted = st.form_submit_button("注册", type="primary")
            if submitted:
                if not feishu_user_id:
                    st.error("请输入飞书 Open ID")
                else:
                    result = register_employee({
                        "feishu_user_id": feishu_user_id,
                        "name": name,
                        "department": department,
                        "skill_id": selected_skill_name if selected_skill_name else None,
                    })
                    if result["success"]:
                        st.success("员工注册成功！")
                        st.rerun()
                    else:
                        st.error(f"注册失败: {result.get('error')}")


def render_preview_tab():
    st.header("Skill 风格预览")

    st.info("以下展示了不同 Skill 模板对同一问题的回答风格差异")

    question = st.text_area(
        "测试问题",
        value="请介绍一下 RAG 技术的工作原理？",
        height=80,
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        test_employee_id = st.text_input("测试员工 ID", placeholder="ou_xxx...")
    with col2:
        st.caption("留空则使用默认 Skill")

    if st.button("预览不同 Skill 的回答风格", type="primary"):
        skills = get_skill_list()
        if not skills:
            st.warning("暂无 Skill 数据")
        else:
            preview_skills = [s for s in skills if s["id"] in (
                "skill_rigorous", "skill_efficient", "skill_beginner", "skill_default"
            )]
            if not preview_skills:
                preview_skills = skills[:3]

            for skill in preview_skills:
                with st.expander(f"{skill['name']} ({skill['answer_style']})", expanded=True):
                    style_emoji = {
                        "rigorous": "🔬",
                        "efficient": "⚡",
                        "beginner": "🌱",
                        "balanced": "⚖️",
                    }
                    st.markdown(f"**风格**: {style_emoji.get(skill['answer_style'], '')} {skill.get('description', '')}")
                    st.markdown(f"**温度**: {skill.get('temperature', 0)} | **最大 Token**: {skill.get('max_tokens', 0)}")
                    st.markdown(f"**系统提示词**:\n```\n{skill.get('system_prompt_suffix', '无')[:300]}\n```")


def render_sessions_tab():
    st.header("飞书会话记录")

    sessions = get_feishu_sessions(limit=50)
    if not sessions:
        st.info("暂无会话记录。员工在飞书中与机器人对话后，会在此显示。")
        return

    st.metric("总会话数", len(sessions))

    for session in sessions:
        user_display = session.get("feishu_user_id", "未知")[:16]
        msg_count = session.get("message_count", 0)
        updated = str(session.get("updated_at", ""))[:19]

        with st.expander(f"{user_display} · {msg_count} 条消息 · {updated}"):
            try:
                resp = requests.get(
                    f"{API_BASE_URL}/sessions/{session['id']}/messages",
                    timeout=10,
                )
                if resp.status_code == 200:
                    messages = resp.json().get("messages", [])
                    for msg in messages[-6:]:
                        role = msg.get("role", "")
                        content = msg.get("content", "")
                        if role == "user":
                            st.markdown(f"**用户**: {content[:200]}")
                        else:
                            st.markdown(f"**AI**: {content[:200]}")
                        st.divider()
                else:
                    st.info("无法加载消息详情")
            except Exception as e:
                st.error(f"加载失败: {e}")


def render_config_tab():
    st.header("飞书应用配置指南")

    st.markdown("""
    ## 飞书应用创建步骤

    ### 第一步：创建企业自建应用

    1. 打开 [飞书开放平台](https://open.feishu.cn/app)
    2. 点击「创建企业自建应用」
    3. 填写应用名称和描述
    4. 获取 **App ID** 和 **App Secret**

    ### 第二步：配置应用能力

    1. 在「添加应用能力」中，选择「机器人」
    2. 启用机器人功能

    ### 第三步：配置事件订阅

    1. 进入「事件与回调」→「事件订阅」
    2. 订阅事件：`im.message.receive_v1`（接收消息）
    3. 配置**请求地址**（即你的后端服务地址）：

    ```
    https://your-domain.com/feishu/webhook
    ```

    4. 获取 **Verification Token**（在「事件与回调」→「事件配置」中）

    ### 第四步：发布应用

    1. 在「版本管理与发布」中创建版本
    2. 申请发布（或在企业内直接启用）

    ### 第五步：配置环境变量

    在 `.env` 文件中添加：

    ```env
    FEISHU_APP_ID=cli_xxxxxxxxxxxxx
    FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxx
    FEISHU_VERIFICATION_TOKEN=xxxxxxxxxxxxxxxxxxxxxx
    ```

    ### 第六步：启动服务

    ```bash
    # 启动 API 服务
    python main.py --api

    # 或同时启动 API 和 Streamlit
    python main.py --api & python main.py --ui
    ```
    """)

    st.divider()

    st.subheader("环境变量参考")

    config_ref = {
        "FEISHU_APP_ID": "飞书应用的 App ID",
        "FEISHU_APP_SECRET": "飞书应用的 App Secret",
        "FEISHU_VERIFICATION_TOKEN": "飞书事件验证 Token",
        "FEISHU_WEBHOOK_PATH": "飞书 Webhook 路径（默认: /feishu/webhook）",
        "FEISHU_ENABLE_STREAMING": "是否启用流式回复（默认: False）",
        "FEISHU_RATE_LIMIT_PER_MINUTE": "每分钟每用户最大请求数（默认: 20）",
    }

    for key, desc in config_ref.items():
        st.write(f"- **{key}**: {desc}")

    st.divider()

    st.subheader("API 端点")

    endpoints = [
        ("GET", "/feishu/webhook", "飞书 URL 验证"),
        ("POST", "/feishu/webhook", "飞书事件回调"),
        ("GET", "/feishu/health", "飞书 Bot 健康检查"),
        ("GET", "/admin/skills", "获取所有 Skill"),
        ("POST", "/admin/skills", "创建 Skill"),
        ("PUT", "/admin/skills/{id}", "更新 Skill"),
        ("DELETE", "/admin/skills/{id}", "删除 Skill"),
        ("GET", "/admin/employees", "获取所有员工"),
        ("POST", "/admin/employees", "注册员工"),
        ("POST", "/admin/employees/{id}/bind-skill", "绑定员工 Skill"),
        ("GET", "/admin/feishu/sessions", "获取飞书会话列表"),
    ]

    for method, path, desc in endpoints:
        col1, col2, col3 = st.columns([1, 3, 4])
        with col1:
            color = "green" if method == "GET" else "orange" if method == "POST" else "red"
            st.markdown(f":{color}[{method}]")
        with col2:
            st.code(path, language=None)
        with col3:
            st.write(desc)


def main():
    init_session_state()

    st.markdown('<h1 class="main-header">飞书 Bot 管理后台</h1>', unsafe_allow_html=True)

    api_connected = check_api_connection()
    if not api_connected:
        st.warning("API 服务未连接，请确保后端已启动: python -m api.server")
        return

    tabs = [
        "状态总览",
        "Skill 管理",
        "员工管理",
        "风格预览",
        "会话记录",
        "配置指南",
    ]
    selected_tab = st.sidebar.radio("导航", tabs, index=0)

    if selected_tab == "状态总览":
        render_status_tab()
    elif selected_tab == "Skill 管理":
        render_skills_tab()
    elif selected_tab == "员工管理":
        render_employees_tab()
    elif selected_tab == "风格预览":
        render_preview_tab()
    elif selected_tab == "会话记录":
        render_sessions_tab()
    elif selected_tab == "配置指南":
        render_config_tab()


if __name__ == "__main__":
    main()
