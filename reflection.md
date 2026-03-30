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
    I used AI tools to help with debugging and as a second pair of eyes on my thought process and design decisions. For example, I was not sure why my input fields on the UI did not accept input. The AI provided feedback for why this was happening, and I implemented the changes.

- What kinds of prompts or questions were most helpful?
    The prompts that were most helpful were ones where I asked the AI to explain a change or element first before generating any changes in code. This was helpful because I got to review the AI's thought process to make sure it aligned with mine and had the right context (that I have) to work with.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.


- How did you evaluate or verify what the AI suggested?


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested the main features of the program. This included the scheduler and householdMember related functions to ensure that time conflicts were correctly detected and that householdMembers are tied correctly to assigned tasks.

- Why were these tests important?
    These test are important because they ensure that what is implemented will result in sound logic and a smooth experience for the end user.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am very confident that it works as intended; however, it definitely needs to be fleshed out more to account for the nuances of time conflicts.

- What edge cases would you test next if you had more time?
    I would test if the scheduler is able to detect time conflicts correctly when the input is the same (ex. 10:00), but the time of day is not (ex. am vs pm).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisfied with the scheduler feature and the ability to assign tasks to either the pet owner and additional caretakers.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    If I had another iteration, I'd want to work on improving the scheduler feature. Again, I would like to flesh it out more to the point where it can display more relevant information as it relates to the duration of tasks, any conflicts, there, and such.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    One importnat thing I learned about working with AI on this project is that it makes a lot of assumptions to fill in the gaps I don't provide. Even if I do provide a lot of context for it to work with. This said, by identifying these filled-in gaps, I get to further deepen my understanding of the system I want to create for my program.
