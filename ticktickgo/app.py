import streamlit as st
from datetime import date
from uuid import uuid4

# ---------- Basis-Layout & Styling ----------
st.set_page_config(page_title="TickTickGO", page_icon="✅", layout="centered")

st.markdown("""
<style>
body, .stApp { background-color: #806c6c; }
html, body, .stApp { color: #e9e0d8; font-family: Georgia, serif; font-size: 1.1rem;}
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-thumb { background-color: #e9e0d8; border-radius: 12px; }
input, button, textarea { border-radius: 20px; }
.task.done { color: #d3dfe8; text-decoration: line-through; }
.task.overdue { color: #ff5555; font-weight: 700; }
.deadline { font-size: .9rem; color: #d3dfe8; font-style: italic; }
.comment { font-size: 0.9rem; color: #a0b0c0; font-style: italic; margin-left: 10px; }
.delete, .edit { background: transparent; border: none; font-size: 1.2rem; color: #d3dfe8; cursor: pointer; }
.delete:hover, .edit:hover { color: #d3dfe8; }

/* Textboxen & Datum mit hellem Hintergrund und dunkler Schrift */
input[type="text"],
textarea,
input[type="date"] {
    background-color: #e9e0d8 !important;
    color: #2c2c2c !important;
    border: 2px solid #e9e0d8 !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    padding: 8px 12px !important;
    appearance: none !important;
    -webkit-appearance: none !important;
    -moz-appearance: none !important;
}

input[type="text"]:focus,
textarea:focus,
input[type="date"]:focus {
    border-color: #e9e0d8 !important;
    box-shadow: 0 0 5px #e9e0d8 !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# ---------- Neue Aufgabe anlegen ----------
st.title("TickTickGO – Dein Taskmanager")

with st.form("add_task", clear_on_submit=True):
    new_task_text = st.text_input("Neue Aufgabe")
    new_task_comment = st.text_area("Kommentar")
    new_task_deadline = st.date_input("Deadline", value=date.today())
    if st.form_submit_button("➕ Hinzufügen") and new_task_text.strip():
        st.session_state.tasks.append({
            "id": uuid4().hex,
            "text": new_task_text.strip(),
            "comment": new_task_comment.strip(),
            "deadline": new_task_deadline,
            "done": False
        })

# ---------- Aufgabenliste ----------
st.subheader("📋 Aufgabenliste")

task_to_delete = None

for i, task in enumerate(st.session_state.tasks):
    checkbox_key = f"done_{task['id']}"
    c1, c2, c3, c4 = st.columns([0.08, 0.64, 0.12, 0.12])

    with c1:
        checked = st.checkbox("", value=task["done"], key=checkbox_key)
        if checked != task["done"]:
            st.session_state.tasks[i]["done"] = checked

    overdue = (not checked) and task["deadline"] < date.today()
    css_class = "task done" if checked else ("task overdue" if overdue else "task")

    with c2:
        st.markdown(
            f"<span class='{css_class}'>{task['text']}</span> "
            f"<span class='deadline'>(📅 {task['deadline'].strftime('%d.%m.%Y')})</span>",
            unsafe_allow_html=True
        )
        if task.get("comment"):
            st.markdown(f"<div class='comment'>💬 {task['comment']}</div>", unsafe_allow_html=True)

    with c3:
        if st.button("✏️", key=f"edit_{task['id']}", help="Aufgabe bearbeiten"):
            st.session_state.edit_id = task["id"]

    with c4:
        if st.button("🗑", key=f"del_{task['id']}", help="Aufgabe löschen"):
            task_to_delete = i

if task_to_delete is not None:
    task_to_delete_id = st.session_state.tasks[task_to_delete]["id"]
    st.session_state.tasks.pop(task_to_delete)
    if st.session_state.edit_id == task_to_delete_id:
        st.session_state.edit_id = None

# ---------- Bearbeitungsformular ----------
edit_idx = next((idx for idx, t in enumerate(st.session_state.tasks)
                 if t["id"] == st.session_state.edit_id), None)

if edit_idx is not None:
    task = st.session_state.tasks[edit_idx]
    st.markdown("---")
    st.subheader("✏️ Aufgabe bearbeiten")

    with st.form("edit_task"):
        edit_text = st.text_input("Aufgabe", value=task["text"])
        edit_comment = st.text_area("Kommentar", value=task["comment"])
        edit_deadline = st.date_input("Deadline", value=task["deadline"])
        col_save, col_cancel = st.columns(2)
        save = col_save.form_submit_button("💾 Speichern")
        cancel = col_cancel.form_submit_button("❌ Abbrechen")

        if cancel:
            st.session_state.edit_id = None

        if save and edit_text.strip():
            st.session_state.tasks[edit_idx].update({
                "text": edit_text.strip(),
                "comment": edit_comment.strip(),
                "deadline": edit_deadline
            })
            st.session_state.edit_id = None
            st.rerun()
            