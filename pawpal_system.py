from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time, datetime
from typing import Optional
from enum import Enum


class TaskCategory(Enum):
    MEDICATION   = "medication"
    FEEDING      = "feeding"
    WALK         = "walk"
    GROOMING     = "grooming"
    APPOINTMENT  = "appointment"
    OTHER        = "other"


@dataclass
class HouseholdMember:
    name: str
    relationship: str
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks)


@dataclass
class Task:
    name: str
    daily_occurrence: int
    category: TaskCategory = TaskCategory.OTHER
    pet: Optional[Pet] = None
    assigned_to: Optional[HouseholdMember] = None
    _is_complete: bool = field(default=False, repr=False, init=False)

    def set_name(self, name: str) -> None:
        self.name = name

    def set_occurrence(self, daily_occurrence: int) -> None:
        self.daily_occurrence = daily_occurrence

    def set_complete(self, complete: bool) -> None:
        self._is_complete = complete

    @property
    def is_complete(self) -> bool:
        return self._is_complete

    def set_pet(self, pet: Pet, owner: Optional[User] = None) -> None:
        self.pet = pet
        pet._increment_task_count()
        if owner is not None and self not in owner.tasks:
            owner.add_task(self)

    def set_task_owner(self, member: HouseholdMember) -> None:
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
        self.routine_name = name

    def set_start_time(self, start_time: time) -> None:
        self.start_time = start_time

    def set_end_time(self, end_time: time) -> None:
        self.end_time = end_time

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks)

    @property
    def duration_minutes(self) -> int:
        start_dt = datetime.combine(date.today(), self.start_time)
        end_dt   = datetime.combine(date.today(), self.end_time)
        return int((end_dt - start_dt).total_seconds() // 60)

    def summary(self, owner: Optional[User] = None) -> str:
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
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )

    @property
    def task_count(self) -> int:
        return self._task_count

    def _increment_task_count(self) -> None:
        self._task_count += 1

    def add_diet(self, diet_info: str) -> None:
        self._diet.append(diet_info)

    def add_disability(self, disability: str) -> None:
        self._disabilities.append(disability)

    def add_routine(self, routine: Routine) -> None:
        routine.pet = self
        self._routines.append(routine)

    @property
    def routines(self) -> list[Routine]:
        return list(self._routines)

    @property
    def diet(self) -> list[str]:
        return list(self._diet)

    @property
    def disabilities(self) -> list[str]:
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
        self._tasks.append(task)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks)

    def generate_routine(
        self,
        routine_name: str,
        start_time: time,
        end_time: time,
        pet: Optional[Pet] = None,
    ) -> Routine:
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
        return self._username

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def pets(self) -> list[Pet]:
        return list(self._pets)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks)

    @property
    def household_members(self) -> list[HouseholdMember]:
        return list(self._household_members)

    def add_pet(self, pet: Pet) -> None:
        self._pets.append(pet)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def add_household_member(self, member: HouseholdMember) -> None:
        self._household_members.append(member)

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        return [t for t in self._tasks if t.pet is pet]
