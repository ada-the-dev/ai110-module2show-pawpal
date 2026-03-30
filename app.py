import streamlit as st
from datetime import time
from pawpal_system import User, Pet, Task, TaskCategory, Recurrence, Scheduler, HouseholdMember

# --- Session state initialization ---
# Streamlit reruns the entire script on every interaction.
# These guards ensure our objects are created once and persist across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "members" not in st.session_state:
    st.session_state.members = []

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ app!
"""
)

with st.expander("Purpose", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) while also involving other household members!
"""
    )

with st.expander("How to Get Started", expanded=True):
    st.markdown(
        """Fill out each input section from the top down to proceed to the next input.
        A schedule will be generated based on the provided information, and it will alert you of any time conflicts based on the given start times.
"""
    )

st.divider()

# --- Owner setup ---
st.subheader("Owner Profile")
with st.form("owner_form"):
    first_name = st.text_input("First name", placeholder="e.g. Jamie")
    username   = st.text_input("Username",   placeholder="e.g. jsmith")
    submitted  = st.form_submit_button("Create Profile")
    if submitted:
        st.session_state.owner = User(username=username, password="", first_name=first_name)
        st.session_state.scheduler = Scheduler()
        st.success(f"Profile created for {first_name}.")

# --- Add a pet ---
st.subheader("Add a Pet")
if st.session_state.owner is None:
    st.info("Create a profile first.")
else:
    with st.form("pet_form"):
        pet_name  = st.text_input("Pet name", placeholder="e.g. Luna")
        breed     = st.text_input("Breed",    placeholder="e.g. Golden Retriever")
        birthdate = st.date_input("Birthdate")
        submitted = st.form_submit_button("Add Pet")
        if submitted:
            pet = Pet(name=pet_name, breed=breed, birthdate=birthdate)
            st.session_state.owner.add_pet(pet)
            st.success(f"{pet_name} added.")

# --- Add a household member ---
st.subheader("Add a Household Member")
if st.session_state.owner is None:
    st.info("Create a profile first.")
else:
    with st.form("member_form"):
        member_name     = st.text_input("Name", placeholder="e.g. Alex")
        relationship    = st.text_input("Relationship", placeholder="e.g. Spouse")
        submitted       = st.form_submit_button("Add Member")
        if submitted:
            member = HouseholdMember(name=member_name, relationship=relationship)
            st.session_state.owner.add_household_member(member)
            st.session_state.members.append(member)
            st.success(f"{member_name} added as {relationship}.")

    if st.session_state.members:
        st.markdown("**Current household members:**")
        for m in st.session_state.members:
            st.markdown(f"- {m.name} ({m.relationship})")

# --- Add a task ---
st.subheader("Add a Task")
if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add a pet first.")
else:
    with st.form("task_form"):
        task_name      = st.text_input("Task name", placeholder="e.g. Morning walk")
        occurrence     = st.number_input("Times per day", min_value=1, max_value=10, value=1)
        category       = st.selectbox("Category", [c.value for c in TaskCategory])
        recurrence     = st.selectbox("Recurrence", [r.value for r in Recurrence])
        scheduled_time = st.time_input("Scheduled time", value=time(8, 0))
        pet_names      = [p.name for p in st.session_state.owner.pets]
        selected_pet   = st.selectbox("For which pet?", pet_names)
        assignee_options = ["Owner"] + [m.name for m in st.session_state.members]
        selected_assignee = st.selectbox("Assign to", assignee_options)
        submitted      = st.form_submit_button("Add Task")
        if submitted:
            pet  = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
            task = Task(
                name=task_name,
                daily_occurrence=occurrence,
                category=TaskCategory(category),
                recurrence=Recurrence(recurrence),
                scheduled_time=scheduled_time.strftime("%H:%M"),
            )
            task.set_pet(pet, st.session_state.owner)
            if selected_assignee != "Owner":
                member = next(m for m in st.session_state.members if m.name == selected_assignee)
                task.set_task_owner(member)
            st.session_state.scheduler.add_task(task)
            st.success(f"Task '{task_name}' added for {selected_pet}, assigned to {selected_assignee}.")

st.divider()

# --- Generate schedule ---
st.subheader("Today's Schedule")
if st.session_state.owner is None or not st.session_state.owner.tasks:
    st.info("Add an owner and at least one task first.")
else:
    scheduler = st.session_state.scheduler

    # --- Conflict warnings ---
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"Scheduling conflict — {warning}")
    else:
        st.success("No scheduling conflicts detected.")

    # --- All tasks sorted by time ---
    st.markdown("#### All Tasks")
    sorted_tasks = scheduler.sort_by_time()
    st.dataframe(
        [
            {
                "Time":       task.scheduled_time or "—",
                "Task":       task.name,
                "Pet":        task.pet.name if task.pet else "—",
                "Category":   task.category.value,
                "Recurrence": task.recurrence.value,
                "Assigned To": task.assigned_to.name if task.assigned_to else (st.session_state.owner.first_name),
                "Status":     "Done" if task.is_complete else "Pending",
            }
            for task in sorted_tasks
        ],
        use_container_width=True,
    )

    # --- Pending tasks ---
    st.markdown("#### Pending Tasks")
    pending = sorted(
        scheduler.filter_by_status(complete=False),
        key=lambda t: tuple(map(int, t.scheduled_time.split(":"))) if t.scheduled_time else (24, 0),
    )
    if pending:
        st.dataframe(
            [
                {
                    "Time":        task.scheduled_time or "—",
                    "Task":        task.name,
                    "Pet":         task.pet.name if task.pet else "—",
                    "Assigned To": task.assigned_to.name if task.assigned_to else st.session_state.owner.first_name,
                }
                for task in pending
            ],
            use_container_width=True,
        )
    else:
        st.success("All tasks completed!")

    # --- Completed tasks ---
    st.markdown("#### Completed Tasks")
    completed = scheduler.filter_by_status(complete=True)
    if completed:
        st.dataframe(
            [
                {
                    "Time": task.scheduled_time or "—",
                    "Task": task.name,
                    "Pet":  task.pet.name if task.pet else "—",
                }
                for task in completed
            ],
            use_container_width=True,
        )
    else:
        st.info("No tasks completed yet.")
