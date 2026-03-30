from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from typing import Optional
from enum import Enum


class TaskCategory(Enum):
    MEDICATION   = "medication"
    FEEDING      = "feeding"
    WALK         = "walk"
    GROOMING     = "grooming"
    APPOINTMENT  = "appointment"
    OTHER        = "other"


class Recurrence(Enum):
    NONE   = "none"
    DAILY  = "daily"
    WEEKLY = "weekly"


_RECURRENCE_DELTA: dict[Recurrence, timedelta] = {
    Recurrence.DAILY:  timedelta(days=1),
    Recurrence.WEEKLY: timedelta(weeks=1),
}


@dataclass
class HouseholdMember:
    name: str
    relationship: str
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        """Append a task to this member's task list."""
        self._tasks.append(task)

    @property
    def tasks(self) -> list[Task]:
        """Return a copy of all tasks assigned to this member."""
        return list(self._tasks)


@dataclass
class Task:
    name: str
    daily_occurrence: int
    category: TaskCategory = TaskCategory.OTHER
    pet: Optional[Pet] = None
    assigned_to: Optional[HouseholdMember] = None
    scheduled_time: Optional[str] = None          # "HH:MM" format, e.g. "07:30"
    recurrence: Recurrence = Recurrence.NONE
    next_due: Optional[date] = None
    _is_complete: bool = field(default=False, repr=False, init=False)

    def set_name(self, name: str) -> None:
        """Update the task's display name."""
        self.name = name

    def set_occurrence(self, daily_occurrence: int) -> None:
        """Set how many times per day this task should occur."""
        self.daily_occurrence = daily_occurrence

    def set_complete(self, complete: bool) -> None:
        """Set the completion status of this task to the given boolean."""
        self._is_complete = complete

    def mark_complete(self) -> Optional[Task]:
        """Mark this task as completed.

        If the task recurs, returns a fresh Task for the next occurrence with
        the same assignee carried over. Returns None for non-recurring tasks.
        """
        self._is_complete = True

        delta = _RECURRENCE_DELTA.get(self.recurrence)
        if delta is None:
            return None
        next_due = date.today() + delta

        return Task(
            name=self.name,
            daily_occurrence=self.daily_occurrence,
            category=self.category,
            pet=self.pet,
            assigned_to=self.assigned_to,
            scheduled_time=self.scheduled_time,
            recurrence=self.recurrence,
            next_due=next_due,
        )

    @property
    def is_complete(self) -> bool:
        """Return whether this task has been completed."""
        return self._is_complete

    def set_pet(self, pet: Pet, owner: Optional[User] = None) -> None:
        """Link this task to a pet, and optionally auto-register it with the owner."""
        self.pet = pet
        pet._increment_task_count()
        if owner is not None and self not in owner.tasks:
            owner.add_task(self)

    def set_task_owner(self, member: HouseholdMember) -> None:
        """Assign this task to a household member and update their task list."""
        self.assigned_to = member
        member.add_task(self)


@dataclass
class Routine:
    routine_name: str
    start_time: time
    end_time: time
    pet: Optional[Pet] = None
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def set_routine_name(self, name: str) -> None:
        """Update the routine's name."""
        self.routine_name = name

    def set_start_time(self, start_time: time) -> None:
        """Set the time this routine begins."""
        self.start_time = start_time

    def set_end_time(self, end_time: time) -> None:
        """Set the time this routine ends."""
        self.end_time = end_time

    def add_task(self, task: Task) -> None:
        """Add a task to this routine's schedule."""
        self._tasks.append(task)

    @property
    def tasks(self) -> list[Task]:
        """Return a copy of all tasks in this routine."""
        return list(self._tasks)

    @property
    def duration_minutes(self) -> int:
        """Return the total length of this routine in minutes."""
        start_dt = datetime.combine(date.today(), self.start_time)
        end_dt   = datetime.combine(date.today(), self.end_time)
        return int((end_dt - start_dt).total_seconds() // 60)

    def summary(self, owner: Optional[User] = None) -> str:
        """Return a formatted string listing all tasks in this routine with assignee and status."""
        lines = [f"Routine: {self.routine_name}"]
        if self.pet:
            lines.append(f"Pet: {self.pet.name}")
        lines.append(
            f"Time: {self.start_time.strftime('%H:%M')} - "
            f"{self.end_time.strftime('%H:%M')} "
            f"({self.duration_minutes} min)"
        )
        lines.append(f"Tasks ({len(self._tasks)}):")
        for i, task in enumerate(self._tasks, start=1):
            if task.assigned_to:
                assignee = task.assigned_to.name
            elif owner:
                assignee = owner.first_name
            else:
                assignee = "Unassigned"
            status   = "Done" if task.is_complete else "Pending"
            pet_name = task.pet.name if task.pet else "?"
            lines.append(
                f"  {i:>2}. [{task.category.value}] {task.name} "
                f"({pet_name}) — {assignee} [{status}]"
            )
        return "\n".join(lines)


@dataclass
class Pet:
    name: str
    breed: str
    birthdate: date
    _routines: list[Routine] = field(default_factory=list, repr=False)
    _diet: list[str]         = field(default_factory=list, repr=False)
    _disabilities: list[str] = field(default_factory=list, repr=False)
    _task_count: int          = field(default=0, repr=False, init=False)

    @property
    def age(self) -> int:
        """Return the pet's current age in years, calculated from birthdate."""
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )

    @property
    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return self._task_count

    def _increment_task_count(self) -> None:
        """Increment the pet's task count by one."""
        self._task_count += 1

    def add_diet(self, diet_info: str) -> None:
        """Add a dietary note or restriction for this pet."""
        self._diet.append(diet_info)

    def add_disability(self, disability: str) -> None:
        """Record a disability or medical condition for this pet."""
        self._disabilities.append(disability)

    def add_routine(self, routine: Routine) -> None:
        """Attach a routine to this pet and set the routine's back-reference."""
        routine.pet = self
        self._routines.append(routine)

    @property
    def routines(self) -> list[Routine]:
        """Return a copy of all routines belonging to this pet."""
        return list(self._routines)

    @property
    def diet(self) -> list[str]:
        """Return a copy of this pet's dietary notes."""
        return list(self._diet)

    @property
    def disabilities(self) -> list[str]:
        """Return a copy of this pet's recorded disabilities."""
        return list(self._disabilities)


class Scheduler:
    # Lower number = higher priority in a generated routine
    _CATEGORY_PRIORITY: dict[TaskCategory, int] = {
        TaskCategory.MEDICATION:  0,
        TaskCategory.FEEDING:     1,
        TaskCategory.WALK:        2,
        TaskCategory.GROOMING:    3,
        TaskCategory.APPOINTMENT: 4,
        TaskCategory.OTHER:       5,
    }

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's pool for routine generation."""
        self._tasks.append(task)

    @property
    def tasks(self) -> list[Task]:
        """Return a copy of all tasks currently in the scheduler."""
        return list(self._tasks)

    def filter_by_status(self, complete: bool) -> list[Task]:
        """Return tasks matching the given completion status.

        Args:
            complete: Pass True to get completed tasks, False for pending tasks.

        Returns:
            A filtered list of Task objects whose is_complete matches the argument.
            Returns an empty list if no tasks match.
        """
        return [t for t in self._tasks if t.is_complete == complete]

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by scheduled_time (HH:MM string) ascending.

        How the lambda works:
          - "HH:MM".split(":") → ["HH", "MM"]
          - tuple(map(int, ...)) → (int_hour, int_minute)
          - This gives Python a numeric pair to compare, so "07:30" < "13:00"
            rather than a raw string comparison.
          - Tasks with no scheduled_time sort to the end via the fallback (24, 0).
        """
        return sorted(
            self._tasks,
            key=lambda t: tuple(map(int, t.scheduled_time.split(":"))) if t.scheduled_time else (24, 0),
        )

    def detect_conflicts(self) -> list[str]:
        """Detect tasks scheduled at the same time and return warning messages.

        Groups all tasks by their scheduled_time in a single O(n) pass using
        a defaultdict. Any time slot with more than one task is flagged.

        Tasks without a scheduled_time are skipped silently.
        Returns an empty list if no conflicts are found — never raises.

        Returns:
            A list of warning strings in the format:
            "Conflict at HH:MM: Task A, Task B"
        """
        time_groups: dict[str, list[Task]] = defaultdict(list)
        for task in self._tasks:
            if task.scheduled_time:
                time_groups[task.scheduled_time].append(task)

        warnings = []
        for scheduled_time, tasks in time_groups.items():
            if len(tasks) > 1:
                names = ", ".join(t.name for t in tasks)
                warnings.append(f"Conflict at {scheduled_time}: {names}")
        return warnings

    def generate_routine(
        self,
        routine_name: str,
        start_time: time,
        end_time: time,
        pet: Optional[Pet] = None,
    ) -> Routine:
        """Build and return a Routine by sorting tasks by priority and expanding by daily occurrence."""
        routine = Routine(
            routine_name=routine_name,
            start_time=start_time,
            end_time=end_time,
            pet=pet,
        )
        sorted_tasks = sorted(
            self._tasks,
            key=lambda t: (self._CATEGORY_PRIORITY.get(t.category, 5), t.name),
        )
        for task in sorted_tasks:
            for _ in range(task.daily_occurrence):
                routine.add_task(task)
        return routine


class User:
    def __init__(self, username: str, password: str, first_name: str):
        self._username = username
        self._password = password
        self._first_name = first_name
        self._pets: list[Pet] = []
        self._tasks: list[Task] = []
        self._household_members: list[HouseholdMember] = []

    @property
    def username(self) -> str:
        """Return the user's username."""
        return self._username

    @property
    def first_name(self) -> str:
        """Return the user's first name."""
        return self._first_name

    @property
    def pets(self) -> list[Pet]:
        """Return a copy of all pets owned by this user."""
        return list(self._pets)

    @property
    def tasks(self) -> list[Task]:
        """Return a copy of all tasks created by this user."""
        return list(self._tasks)

    @property
    def household_members(self) -> list[HouseholdMember]:
        """Return a copy of all household members managed by this user."""
        return list(self._household_members)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the user's list of owned pets."""
        self._pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Register a task under this user."""
        self._tasks.append(task)

    def add_household_member(self, member: HouseholdMember) -> None:
        """Add a household member to this user's household."""
        self._household_members.append(member)

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return all tasks associated with a specific pet."""
        return [t for t in self._tasks if t.pet is pet]
