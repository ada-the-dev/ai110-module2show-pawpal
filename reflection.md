# PawPal+ Project Reflection

## 1. System Design
- The user should be able to add a pet.
- The user should be able to add tasks they want to do for their pet.
- The user should be able to see a recommended schedule of tasks for a day.

**a. Initial design**

- Briefly describe your initial UML design.
    The initial UML design includes an user class and pet class. An user may own zero to many pets. A pet may have zero to many routines, and each routine may consist of zero to many tasks. Additionally, a task can be assigned
    to a household member (the user included).

- What classes did you include, and what responsibilities did you assign to each?
    I included five classes: User, Pet, Routine, Task, and HouseholdMember. I explained the relationships between the classes earlier. In regards to their attributes and methods, the classes will have a few basic attributes to describe the particular class. For example, the pet class will contain information about the pet's name, breed, and age. Additionally, there are some setter functions throughout the classes to allow the user to set the values of these attributes.

**b. Design changes**

- Did your design change during implementation?
    Yes.

- If yes, describe at least one change and why you made it.
    The AI gave feedback that the classes had no getter functions, and I made this change because, as it correctly pointed out, if I cannot retrieve the values of any relevant attributes then I will not be able to use or display this information for the user.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    Constraints that my scheduler considers is time. It checked if start times for tasks were equal to each other.

- How did you decide which constraints mattered most?
    I was mainly focused on getting the bare bones of the scheduler implemented, and the first constraint that came to mind was time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One tradeoff that my scheduler makes is that it gives a warning when two task's start times are equal to each other. Ideally, the scheduler should also be able to detect overlapping durations as well.

- Why is that tradeoff reasonable for this scenario?
    This tradeoff is reasonable because we do want the code to give a warning if two tasks start times are equal to each other, and we are in the early stages of development. Features can be more fleshed out as further development occurs.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
