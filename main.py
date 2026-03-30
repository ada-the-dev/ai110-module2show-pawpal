from datetime import date, time
from pawpal_system import HouseholdMember, Pet, Task, TaskCategory, Recurrence, Scheduler, User

# --- Setup ---
owner = User(username="jsmith", first_name="Jamie")

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
    {"pet": "Luna",  "name": "Walk Luna",               "daily_occurrence": 1, "category": TaskCategory.WALK,       "assigned_to": "Alex", "scheduled_time": "17:30", "recurrence": Recurrence.DAILY,  "duration": 30, "priority": 2},
    {"pet": "Mochi", "name": "Brush Mochi",             "daily_occurrence": 1, "category": TaskCategory.GROOMING,   "assigned_to": "Alex", "scheduled_time": "19:00", "recurrence": Recurrence.WEEKLY, "duration": 20, "priority": 4},
    {"pet": "Luna",  "name": "Feed Luna",               "daily_occurrence": 2, "category": TaskCategory.FEEDING,    "assigned_to": None,   "scheduled_time": "07:00", "recurrence": Recurrence.DAILY,  "duration": 10, "priority": 2},
    {"pet": "Mochi", "name": "Mochi's Eye Drops",       "daily_occurrence": 2, "category": TaskCategory.MEDICATION, "assigned_to": None,   "scheduled_time": "09:00", "recurrence": Recurrence.DAILY,  "duration": 5,  "priority": 1},
    {"pet": "Mochi", "name": "Feed Mochi",              "daily_occurrence": 3, "category": TaskCategory.FEEDING,    "assigned_to": None,   "scheduled_time": "07:30", "recurrence": Recurrence.DAILY,  "duration": 10, "priority": 2},
    {"pet": "Luna",  "name": "Luna's Joint Supplement", "daily_occurrence": 1, "category": TaskCategory.MEDICATION, "assigned_to": None,   "scheduled_time": "08:00", "recurrence": Recurrence.NONE,   "duration": 5,  "priority": 1},
    # Intentional conflict: same time as Mochi's Eye Drops (09:00) to test detect_conflicts()
    {"pet": "Luna",  "name": "Luna's Morning Check",    "daily_occurrence": 1, "category": TaskCategory.OTHER,      "assigned_to": None,   "scheduled_time": "09:00", "recurrence": Recurrence.DAILY,  "duration": 10, "priority": 5},
]

task_objects = []
for task_info in TASKS_DATA:
    task = Task(
        name=task_info["name"],
        daily_occurrence=task_info["daily_occurrence"],
        category=task_info["category"],
        scheduled_time=task_info["scheduled_time"],
        recurrence=task_info["recurrence"],
        duration=task_info["duration"],
        priority=task_info["priority"],
    )
    task.set_pet(pets[task_info["pet"]], owner)
    if task_info["assigned_to"]:
        task.set_task_owner(members[task_info["assigned_to"]])
    task_objects.append(task)

# --- Build today's schedule via Scheduler ---
scheduler = Scheduler()
for task in owner.tasks:
    scheduler.add_task(task)

# --- Conflict detection (runs before printing the schedule) ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("SCHEDULE WARNINGS:")
    for warning in conflicts:
        print(f"  ! {warning}")
else:
    print("No scheduling conflicts detected.")

routine = scheduler.generate_routine(
    routine_name="Today's Schedule",
    start_time=time(7, 0),
    end_time=time(20, 0),
)

# --- Today's schedule ---
sort_key = lambda t: tuple(map(int, t.scheduled_time.split(":"))) if t.scheduled_time else (24, 0)
today = date.today()
print("=" * 70)
print(f"Today's Schedule — {today}")
print("=" * 70)
for task in scheduler.sort_by_time():
    assignee = task.assigned_to.name if task.assigned_to else owner.first_name
    status = "Done" if task.is_complete else "Pending"
    print(f"  {today}  {task.scheduled_time}  {task.name:<30} — {assignee} [{status}]")
print("=" * 70)

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

# --- Mark recurring tasks complete and collect next occurrences ---
next_occurrences = []
for task in task_objects:
    next_task = task.mark_complete()
    if next_task:
        next_occurrences.append(next_task)

# --- Next proposed weekly schedule (recurring tasks only) ---
print()
print("=" * 70)
print("Next Proposed Weekly Schedule — recurring tasks only")
print("=" * 70)
for task in sorted(next_occurrences, key=sort_key):
    assignee = task.assigned_to.name if task.assigned_to else owner.first_name
    print(f"  {task.next_due}  {task.scheduled_time}  {task.name:<30} — {assignee} [{task.recurrence.value}]")
print("=" * 70)

# --- Tasks sorted by scheduled_time (verifies out-of-order insertion is corrected) ---
print()
print("All tasks sorted by time:")
for task in scheduler.sort_by_time():
    time_label = task.scheduled_time if task.scheduled_time else "unscheduled"
    status = "Done" if task.is_complete else "Pending"
    print(f"  {time_label}  {task.name:<30} [{status}]")

# --- Filter: pending only (sorted by time) ---
print()
print("Pending tasks:")
for task in sorted(scheduler.filter_by_status(complete=False), key=sort_key):
    print(f"  {task.scheduled_time}  {task.name}")

# --- Filter: completed only ---
print()
print("Completed tasks:")
for task in scheduler.filter_by_status(complete=True):
    print(f"  {task.scheduled_time}  {task.name}")
