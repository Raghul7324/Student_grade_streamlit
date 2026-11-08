import pandas as pd
import streamlit as st


def get_grade(marks):
    """Same grading scale as the original code."""
    if marks < 0 or marks > 100:
        return None
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "E"


def parse_mark(text):
    """Return (mark, error). Never raises on bad input."""
    text = text.strip()
    if not text:
        return None, "Please enter a mark."
    try:
        mark = float(text)
    except ValueError:
        return None, "Mark must be a number."
    if mark < 0 or mark > 100:
        return None, "Marks should be between 0 and 100."
    return (int(mark) if mark.is_integer() else mark), None


st.set_page_config(page_title="Student Grade Manager", page_icon="🎓")
st.title("🎓 Student Grade Manager")
#st.caption("WITH st.session_state: the list survives every rerun.")

# --- The key difference: create the list ONCE and keep it across reruns ---
if "students" not in st.session_state:
    st.session_state.students = []

# --- Add student form ---
with st.form("add_student_form", clear_on_submit=True):
    name = st.text_input("Name")
    mark_text = st.text_input("Mark (0 - 100)")
    submitted = st.form_submit_button("Add student")

if submitted:
    name = name.strip()
    mark, error = parse_mark(mark_text)
    if not name:
        st.error("Please enter a student name.")
    elif error:
        st.error(error)
    else:
        st.session_state.students.append({"Name": name, "Mark": mark})
        st.success(f"Added {name} with mark {mark}.")

# --- Show table + metrics ---
students = st.session_state.students

if students:
    rows = [
        {"Name": s["Name"], "Mark": s["Mark"], "Grade": get_grade(s["Mark"])}
        for s in students
    ]
    df = pd.DataFrame(rows)
    st.subheader("Students")
    # Left-align header and cell values for Name, Mark and Grade.
    # st.table renders real HTML, so the text-align style is applied reliably
    # (st.dataframe draws on a canvas and ignores it).
    styled_df = (
        df.style.hide(axis="index")
        .set_properties(**{"text-align": "left"})
        .set_table_styles([{"selector": "th", "props": [("text-align", "left")]}])
    )
    st.table(styled_df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Class Average", f"{df['Mark'].mean():.1f}")
    c2.metric("Highest", f"{df['Mark'].max():g}")
    c3.metric("Lowest", f"{df['Mark'].min():g}")

    if st.button("Clear all students"):
        st.session_state.students = []
        st.rerun()
else:
    st.info("No students yet. Add one using the form above.")