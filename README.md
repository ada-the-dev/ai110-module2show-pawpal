# What is PawPal+?

**PawPal+** is a Streamlit app that helps a pet owner plan care tasks for their pet, involving other caretakers in the process! Based on the provided information, a schedule will be generated. Any conflicting start times for tasks will be alerted to the owner.

## Smarter Scheduling

The app is able to do the following.
1. Sort tasks in a schedule by time.
2. Filter tasks into groups based on their completion status.
3. Automate recurring tasks into a "next week schedule."
4. Detect conflict between tasks start times.

## Features List
Owner Profile
- Set up your personal profile with a name and username to get started.

Pet Management
- Add one or more pets with their name, breed, and birthdate. The app tracks each pet's age and how many tasks are assigned to them.

Household Members
- Add family members or roommates who help with pet care. Each person can be assigned specific tasks and has their own task list.

Task Creation
- Create care tasks for any pet with details like what type of care it is, how many times a day it needs to happen, what time it's scheduled, and who's responsible for it.

Task Assignment
- Assign any task to yourself or a household member. The app remembers who is in charge by default when the task repeats.

Recurring Tasks
- Mark a task as daily or weekly. When it's completed, the app automatically prepares the next occurrence with the same details — no need to re-enter anything.

Daily Schedule View
- See all of today's tasks organized by time, showing who each task is assigned to, which pet it's for, and whether it's pending or done.

Next Week Preview
- After completing recurring tasks, the app generates a proposed schedule for the next occurrence of each repeating task, sorted by time.

Conflict Alerts
- If two tasks are scheduled at the same time, the app automatically flags it with a warning before displaying the schedule.

Pending & Completed Filters
- Quickly view only what still needs to be done today, or review what has already been completed.

## Demo
<a href="/demo_images/pawpal_demo1.PNG" target="_blank"><img src='/demo_images/pawpal_demo1.PNG' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

This is the starting screen. Go ahead and enter input for the user.

<a href="/demo_images/pawpal_demo2.PNG" target="_blank"><img src='/demo_images/pawpal_demo2.PNG' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

After entering image for the user, add pet information for each pet you have.
This feature will become available after information about the user is provided.

<a href="/demo_images/pawpal_demo3.PNG" target="_blank"><img src='/demo_images/pawpal_demo3.PNG' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

Add additional caretakers and family members who will help take care of the pet.

<a href="/demo_images/pawpal_demo4.PNG" target="_blank"><img src='/demo_images/pawpal_demo4.PNG' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

Add tasks.

<a href="/demo_images/pawpal_demo5.PNG" target="_blank"><img src='/demo_images/pawpal_demo5.PNG' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

After adding tasks, you can use the drop down menus in the edit and remove sections to edit and remove tasks.

<a href="/demo_images/pawpal_demo6.PNG" target="_blank"><img src='/demo_images/pawpal_demo6.PNG' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

Here is where your schedule is generated. Time conflict alerts will be given here as well.

## Getting started

### Requirements

- Python 3.10+
- Streamlit

### Install dependencies

```pip install streamlit```

### Run the Web App

```streamlit run app.py```

### Run the CLI Demo

```python main.py```