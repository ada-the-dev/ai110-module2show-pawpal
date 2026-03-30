from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HouseholdMember:
    name: str
    relationship: str
    _tasks: list = field(default_factory=list, repr=False)

    def add_task(self, task: "Task") -> None:
        self._tasks.append(task)


@dataclass
class Task:
    name: str
    daily_occurrence: int
    assigned_to: Optional[HouseholdMember] = None

    def set_name(self, name: str) -> None:
        self.name = name

    def set_occurrence(self, daily_occurrence: int) -> None:
        self.daily_occurrence = daily_occurrence

    def set_task_owner(self, member: HouseholdMember) -> None:
        self.assigned_to = member


@dataclass
class Routine:
    routine_name: str
    start_time: str
    end_time: str
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def set_routine_name(self, name: str) -> None:
        self.routine_name = name

    def set_start_time(self, start_time: str) -> None:
        self.start_time = start_time

    def set_end_time(self, end_time: str) -> None:
        self.end_time = end_time

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)


@dataclass
class Pet:
    name: str
    breed: str
    age: int
    _routines: list[Routine] = field(default_factory=list, repr=False)
    _diet: list[str] = field(default_factory=list, repr=False)
    _disabilities: list[str] = field(default_factory=list, repr=False)

    def add_diet(self, diet_info: str) -> None:
        self._diet.append(diet_info)

    def add_disability(self, disability: str) -> None:
        self._disabilities.append(disability)

    def add_routine(self, routine: Routine) -> None:
        self._routines.append(routine)


class User:
    def __init__(self, username: str, password: str, first_name: str):
        self._username = username
        self._password = password
        self._first_name = first_name
        self._pets: list[Pet] = []
        self._tasks: list[Task] = []
        self._household_members: list[HouseholdMember] = []

    def add_pet(self, pet: Pet) -> None:
        self._pets.append(pet)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def add_household_member(self, member: HouseholdMember) -> None:
        self._household_members.append(member)
