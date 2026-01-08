###  Record your observations on BDD and working this way, including the pros and cons, and how would you introduce it into your project.

Having gained some experience with both BDD and TDD, I can see the strengths and limitations of each approach.  

I think BDD can be particularly useful in a business context, especially when working with non-technical clients or colleagues. Describing how an application should behave in plain English means everyone involved can understand the expected behaviour without needing technical knowledge. This makes it easier to gather requirements, validate ideas, and avoid any misunderstandings. A downside, though, is that I feel BDD alone isn’t enough for actually writing the code as it doesn't fully ensure the implementation of the code is correct.

That's why I believe TDD complements BDD by breaking code development into smaller, manageable tasks and testing the it as it’s written. Using the Red-Green-Refactor cycle ensures that each component works as intended and behaves in the way you want it to. It also allows you to work more confidently with the code you are writing, knowing that any changes or new implementations won’t break existing functionality.

If I was going to use BDD in a future project again, I would use it as a supplementary tool rather than the primary method for writing code. It would be particularly valuable for engaging with clients to capture their requirements and expected behaviours. By documenting behaviours in plain English, clients can see and verify that their needs are accurately being met. TDD would then be my main approach for implementation, turning these behaviours into working, tested code.  

**Pros of BDD:**
- Makes requirements and expected behaviour clear to everyone, technical or not.
- Helps reduce misunderstandings between developers, clients, and stakeholders.
- Provides a framework for automated acceptance testing.

**Cons of BDD:**
- Alone, it doesn’t drive code implementation.
- Can become comlicated if overused or too detailed.
- Requires collaboration and discipline to stay effective.

Overall, I feel combining BDD with TDD gives a balanced approach: clear expectations, accurate requirements, and reliable, well-tested code.