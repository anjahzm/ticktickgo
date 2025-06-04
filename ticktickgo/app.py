import streamlit as st
from datetime import date
from uuid import uuid4

st.set_page_config(page_title="TickTickGO", page_icon="✅", layout="centered")

st.markdown("""
<style>
body {background:#000;color:#fff;font-family:Georgia,serif}
input, button {border-radius:12px}
.task.done {color:#888;text-decoration:line-through}
.task.overdue {color:#f55;font-weight:700}
.deadline {font-size:.9rem;color:#aaa;font-style:italic}
.delete {background:transparent;border:none;font-size:1.2rem;color:#f55;cursor:pointer}
.delete:hover{color:#f22}
</style>
""", unsafe_allow_html=True)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("TickTickGO – Dein Taskmanager")

with st.form("add_task", clear_on_submit=True):
    new_task_text = st.text_input("Neue Aufgabe")
    new_task_deadline = st.date_input("Deadline", value=date.today())
    submitted = st.form_submit_button("➕ Hinzufügen")
    if submitted and new_task_text.strip():
        st.session_state.tasks.append({
            "id": uuid4().hex,
            "text": new_task_text.strip(),
            "deadline": new_task_deadline,
            "done": False
        })

st.subheader("📋 Aufgabenliste")

task_to_delete = None

for i, task in enumerate(st.session_state.tasks):
    overdue = (not task["done"]) and task["deadline"] < date.today()
    css_class = "task"
    if task["done"]:
        css_class += " done"
    elif overdue:
        css_class += " overdue"

    checkbox_key = f"done_{task['id']}"
    if checkbox_key not in st.session_state:
        st.session_state[checkbox_key] = task["done"]

    c1, c2, c3 = st.columns([0.08, 0.78, 0.14])
    with c1:
        checked = st.checkbox("", key=checkbox_key)
        if checked != task["done"]:
            st.session_state.tasks[i]["done"] = checked

    with c2:
        st.markdown(
            f"<span class='{css_class}'>{task['text']}</span> "
            f"<span class='deadline'>(📅 {task['deadline'].strftime('%d.%m.%Y')})</span>",
            unsafe_allow_html=True
        )

    with c3:
        if st.button("🗑", key=f"del_{task['id']}"):
            task_to_delete = i

if task_to_delete is not None:
    st.session_state.tasks.pop(task_to_delete)
