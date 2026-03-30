from datetime import date, time
from pawpal_system import HouseholdMember, Pet, Task, TaskCategory, Scheduler, User

# --- Setup ---
owner = User(username="jsmith", password="secret", first_name="Jamie")

luna  = Pet(name="Luna",  breed="Golden Retriever", birthdate=date(2020, 6, 15))
mochi = Pet(name="Mochi", breed="Shih Tzu",         birthdate=date(2018, 3, 22))

owner.add_pet(luna)
owner.add_pet(mochi)

# --- Household member ---
alex = HouseholdMember(name="Alex", relationship="Spouse")
owner.add_household_member(alex)

# --- Create tasks ---
# set_pet(pet, owner) automatically registers each task with the owner
luna_supplement = Task(name="Luna's Joint Supplement", daily_occurrence=1, category=TaskCategory.MEDICATION)
luna_feed       = Task(name="Feed Luna",               daily_occurrence=2, category=TaskCategory.FEEDING)
luna_walk       = Task(name="Walk Luna",               daily_occurrence=1, category=TaskCategory.WALK)

luna_supplement.set_pet(luna, owner)
luna_feed.set_pet(luna, owner)
luna_walk.set_pet(luna, owner)

mochi_eye_drops = Task(name="Mochi's Eye Drops", daily_occurrence=2, category=TaskCategory.MEDICATION)
mochi_feed      = Task(name="Feed Mochi",         daily_occurrence=3, category=TaskCategory.FEEDING)
mochi_brush     = Task(name="Brush Mochi",        daily_occurrence=1, category=TaskCategory.GROOMING)

mochi_eye_drops.set_pet(mochi, owner)
mochi_feed.set_pet(mochi, owner)
mochi_brush.set_pet(mochi, owner)

# --- Assign some tasks to Alex ---
luna_walk.set_task_owner(alex)
mochi_brush.set_task_owner(alex)

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

# --- Owner task summary ---
owner_tasks = [t for t in owner.tasks if t.assigned_to is None]
print()
print(f"{owner.first_name}'s tasks:")
for task in owner_tasks:
    print(f"  - {task.name} ({task.pet.name if task.pet else '?'})")

# --- Household member task summary ---
print()
print(f"{alex.name}'s tasks ({alex.relationship}):")
for task in alex.tasks:
    print(f"  - {task.name} ({task.pet.name if task.pet else '?'})")
