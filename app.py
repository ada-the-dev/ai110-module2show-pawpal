import streamlit as st
from pawpal_system import User, Pet, Task, TaskCategory, Scheduler, HouseholdMember

# --- Session state initialization ---
# Streamlit reruns the entire script on every interaction.
# These guards ensure our objects are created once and persist across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Owner setup ---
st.subheader("Owner Profile")
with st.form("owner_form"):
    first_name = st.text_input("First name", value="Jamie")
    username   = st.text_input("Username",   value="jsmith")
    submitted  = st.form_submit_button("Create Profile")
    if submitted:
        st.session_state.owner = User(username=username, password="", first_name=first_name)
        st.success(f"Profile created for {first_name}.")

# --- Add a pet ---
st.subheader("Add a Pet")
if st.session_state.owner is None:
    st.info("Create a profile first.")
else:
    with st.form("pet_form"):
        pet_name  = st.text_input("Pet name", value="Luna")
        breed     = st.text_input("Breed",    value="Golden Retriever")
        birthdate = st.date_input("Birthdate")
        submitted = st.form_submit_button("Add Pet")
        if submitted:
            pet = Pet(name=pet_name, breed=breed, birthdate=birthdate)
            st.session_state.owner.add_pet(pet)
            st.success(f"{pet_name} added.")

# --- Add a task ---
st.subheader("Add a Task")
if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add a pet first.")
else:
    with st.form("task_form"):
        task_name  = st.text_input("Task name", value="Morning walk")
        occurrence = st.number_input("Times per day", min_value=1, max_value=10, value=1)
        category   = st.selectbox("Category", [c.value for c in TaskCategory])
        pet_names  = [p.name for p in st.session_state.owner.pets]
        selected   = st.selectbox("For which pet?", pet_names)
        submitted  = st.form_submit_button("Add Task")
        if submitted:
            pet  = next(p for p in st.session_state.owner.pets if p.name == selected)
            task = Task(name=task_name, daily_occurrence=occurrence, category=TaskCategory(category))
            task.set_pet(pet, st.session_state.owner)
            st.success(f"Task '{task_name}' added for {selected}.")

st.divider()

# --- Generate schedule ---
st.subheader("Build Schedule")
if st.button("Generate Schedule"):
    if st.session_state.owner is None or not st.session_state.owner.tasks:
        st.warning("Add an owner and at least one task first.")
    else:
        from datetime import time
        scheduler = Scheduler()
        for task in st.session_state.owner.tasks:
            scheduler.add_task(task)
        routine = scheduler.generate_routine(
            routine_name="Today's Schedule",
            start_time=time(7, 0),
            end_time=time(20, 0),
        )
        st.text(routine.summary(st.session_state.owner))
