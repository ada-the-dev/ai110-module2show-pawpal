from datetime import date, time
from pawpal_system import HouseholdMember, Pet, Task, TaskCategory, Scheduler, User

# --- Setup ---
owner = User(username="jsmith", password="secret", first_name="Jamie")

# --- Pets ---
PETS_DATA = [
    {"name": "Luna",  "breed": "Golden Retriever", "birthdate": date(2020, 6, 15)},
    {"name": "Mochi", "breed": "Shih Tzu",         "birthdate": date(2018, 3, 22)},
]

pets = {}
for pet_info in PETS_DATA:
    pet = Pet(**pet_info)
    owner.add_pet(pet)
    pets[pet_info["name"]] = pet

# --- Household members ---
MEMBERS_DATA = [
    {"name": "Alex", "relationship": "Spouse"},
]

members = {}
for member_info in MEMBERS_DATA:
    member = HouseholdMember(**member_info)
    owner.add_household_member(member)
    members[member_info["name"]] = member

# --- Tasks ---
# Each entry: pet name, task name, daily_occurrence, category, assigned_to (member name or None)
# Tasks are intentionally out of time order to verify sort_by_time() works correctly.
TASKS_DATA = [
    {"pet": "Luna",  "name": "Walk Luna",               "daily_occurrence": 1, "category": TaskCategory.WALK,       "assigned_to": "Alex", "scheduled_time": "17:30"},
    {"pet": "Mochi", "name": "Brush Mochi",             "daily_occurrence": 1, "category": TaskCategory.GROOMING,   "assigned_to": "Alex", "scheduled_time": "19:00"},
    {"pet": "Luna",  "name": "Feed Luna",               "daily_occurrence": 2, "category": TaskCategory.FEEDING,    "assigned_to": None,   "scheduled_time": "07:00"},
    {"pet": "Mochi", "name": "Mochi's Eye Drops",       "daily_occurrence": 2, "category": TaskCategory.MEDICATION, "assigned_to": None,   "scheduled_time": "09:00"},
    {"pet": "Mochi", "name": "Feed Mochi",              "daily_occurrence": 3, "category": TaskCategory.FEEDING,    "assigned_to": None,   "scheduled_time": "07:30"},
    {"pet": "Luna",  "name": "Luna's Joint Supplement", "daily_occurrence": 1, "category": TaskCategory.MEDICATION, "assigned_to": None,   "scheduled_time": "08:00"},
]

task_objects = []
for task_info in TASKS_DATA:
    task = Task(
        name=task_info["name"],
        daily_occurrence=task_info["daily_occurrence"],
        category=task_info["category"],
        scheduled_time=task_info["scheduled_time"],
    )
    task.set_pet(pets[task_info["pet"]], owner)
    if task_info["assigned_to"]:
        task.set_task_owner(members[task_info["assigned_to"]])
    task_objects.append(task)

# --- Build today's schedule via Scheduler ---
scheduler = Scheduler()
for task in owner.tasks:
    scheduler.add_task(task)

routine = scheduler.generate_routine(
    routine_name="Today's Schedule",
    start_time=time(7, 0),
    end_time=time(20, 0),
)

# --- Print schedule ---
print("=" * 55)
print(routine.summary(owner))
print("=" * 55)

# --- Print per-pet task counts ---
print()
for pet in owner.pets:
    print(f"{pet.name} ({pet.breed}, age {pet.age}) — {pet.task_count} task(s) assigned")

# --- Owner and household member task summaries ---
owner_tasks = [t for t in owner.tasks if t.assigned_to is None]
print()
print(f"{owner.first_name}'s tasks:")
for task in owner_tasks:
    print(f"  - {task.name} ({task.pet.name if task.pet else '?'})")

for member in owner.household_members:
    print()
    print(f"{member.name}'s tasks ({member.relationship}):")
    for task in member.tasks:
        print(f"  - {task.name} ({task.pet.name if task.pet else '?'})")

# --- Mark some tasks complete to verify filtering ---
task_objects[2].mark_complete()   # Feed Luna     — 07:00
task_objects[3].mark_complete()   # Mochi's Eye Drops — 09:00

# --- Tasks sorted by scheduled_time (verifies out-of-order insertion is corrected) ---
print()
print("All tasks sorted by time:")
for task in scheduler.sort_by_time():
    time_label = task.scheduled_time if task.scheduled_time else "unscheduled"
    status = "Done" if task.is_complete else "Pending"
    print(f"  {time_label}  {task.name:<30} [{status}]")

# --- Filter: pending only (sorted by time) ---
sort_key = lambda t: tuple(map(int, t.scheduled_time.split(":"))) if t.scheduled_time else (24, 0)
print()
print("Pending tasks:")
for task in sorted(scheduler.filter_by_status(complete=False), key=sort_key):
    print(f"  {task.scheduled_time}  {task.name}")

# --- Filter: completed only ---
print()
print("Completed tasks:")
for task in scheduler.filter_by_status(complete=True):
    print(f"  {task.scheduled_time}  {task.name}")
