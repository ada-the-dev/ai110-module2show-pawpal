import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from datetime import date
from pawpal_system import Pet, Task, TaskCategory


class TestTaskCompletion(unittest.TestCase):
    # Verifies that task completion status is tracked correctly.
    # Tasks should start incomplete and respond properly to mark_complete()
    # and set_complete().

    def test_task_is_incomplete_by_default(self):
        # A newly created task should always start as incomplete.
        # No action should be needed from the user to set this initial state.
        task = Task(name="Feed Luna", daily_occurrence=2, category=TaskCategory.FEEDING)
        self.assertFalse(task.is_complete)

    def test_mark_complete_sets_status_to_true(self):
        # Calling mark_complete() should flip is_complete to True,
        # indicating the task has been done for the day.
        task = Task(name="Feed Luna", daily_occurrence=2, category=TaskCategory.FEEDING)
        task.mark_complete()
        self.assertTrue(task.is_complete)

    def test_set_complete_false_after_mark_complete(self):
        # set_complete(False) should be able to undo a completed status.
        # This covers cases like a user accidentally marking a task done.
        task = Task(name="Feed Luna", daily_occurrence=2, category=TaskCategory.FEEDING)
        task.mark_complete()
        task.set_complete(False)
        self.assertFalse(task.is_complete)


class TestPetTaskCount(unittest.TestCase):
    # Verifies that a pet's task count stays in sync as tasks are assigned to it.
    # The count should update automatically via set_pet() with no manual tracking
    # required from the user.

    def test_task_count_starts_at_zero(self):
        # A newly created pet should have no tasks assigned to it yet.
        pet = Pet(name="Luna", breed="Golden Retriever", birthdate=date(2020, 6, 15))
        self.assertEqual(pet.task_count, 0)

    def test_task_count_increments_when_task_assigned(self):
        # Assigning one task via set_pet() should bring the count to 1.
        pet = Pet(name="Luna", breed="Golden Retriever", birthdate=date(2020, 6, 15))
        Task(name="Feed Luna", daily_occurrence=2, category=TaskCategory.FEEDING).set_pet(pet)
        self.assertEqual(pet.task_count, 1)

    def test_task_count_reflects_multiple_tasks(self):
        # Each call to set_pet() should increment the count by 1.
        # After three tasks are assigned, the count should be exactly 3.
        pet = Pet(name="Luna", breed="Golden Retriever", birthdate=date(2020, 6, 15))
        Task(name="Feed Luna",  daily_occurrence=2, category=TaskCategory.FEEDING).set_pet(pet)
        Task(name="Walk Luna",  daily_occurrence=1, category=TaskCategory.WALK).set_pet(pet)
        Task(name="Brush Luna", daily_occurrence=1, category=TaskCategory.GROOMING).set_pet(pet)
        self.assertEqual(pet.task_count, 3)

    def test_task_count_does_not_change_for_other_pet(self):
        # Assigning a task to one pet should have no effect on another pet's count.
        # Each pet's task count must be independent.
        luna  = Pet(name="Luna",  breed="Golden Retriever", birthdate=date(2020, 6, 15))
        mochi = Pet(name="Mochi", breed="Shih Tzu",         birthdate=date(2018, 3, 22))
        Task(name="Feed Luna", daily_occurrence=2, category=TaskCategory.FEEDING).set_pet(luna)
        self.assertEqual(mochi.task_count, 0)


if __name__ == "__main__":
    unittest.main()
