# Software Architecture Workshop - Architectural Styles

Welcome to the SDA2 Software Architecture Workshop! This repository contains hands-on exercises to understand different architectural styles through practical Python implementations using Test-Driven Development (TDD).

## 🎯 Learning Objectives

By the end of this workshop, you will understand:
- The characteristics and trade-offs of different architectural styles
- How architectural decisions impact code organization and maintainability
- The practical implementation of monolithic, layered, and event-driven architectures
- Test-Driven Development as a learning and design tool
- Progressive complexity in software architecture design

## 📁 Repository Structure

This repository uses a **two-branch strategy** for educational purposes:

### `main` Branch (Starter Templates)
```
├── 01-monolith/              # Monolithic Architecture
│   ├── todo_manager.py       # TDD starter template with failing tests
│   └── guide.md             # Architecture learning guide and exercise-specific instructions
├── 02-layered/               # Layered Architecture  
│   ├── library_system.py     # TDD starter template with failing tests
│   └── guide.md             # Architecture learning guide and exercise-specific instructions
├── 03-eventdriven/           # Event-Driven Architecture
│   ├── library_system.py     # TDD starter template with failing tests
│   └── guide.md             # Architecture learning guide and exercise-specific instructions
├── LICENSE                   # MIT License
└── README.md                 # This file
```

### `solutions` Branch (Complete Implementations)
- Same structure as `main` branch
- Contains complete, working solutions
- All tests pass
- Includes interactive demos

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/bfh-teaching/sda2-workshop-architectural-styles
cd ssda2-workshop-architectural-styles
```

### 2. Verify You're on the Main Branch
```bash
git branch
# Should show: * main
```

### 3. Development Environment
- **Python 3.7+** required
- **No external dependencies** needed
- Use your favorite IDE/editor

## 🧪 Test-Driven Development Approach

This workshop uses **TDD** to guide your learning:

1. **Read failing tests** - They define exactly what to implement
2. **Implement functions** - Make tests pass one by one  
3. **Get immediate feedback** - Know instantly if your solution works
4. **Learn through testing** - Tests serve as requirements and documentation

### Running Tests
```bash
# Navigate to any exercise directory
cd 01-monolith

# Run the starter template to see failing tests
python todo_manager.py

# Implement functions to make tests pass
# Run again to see progress
python todo_manager.py
```

## 📋 Workshop Schedule & Progressive Complexity

### Part 1: Monolithic Architecture
**Complexity: 🔵 Beginner**
1. **Theory**: Direct coupling, simple structure
2. **Implementation**: Complete `01-monolith/todo_manager.py`
3. **Discussion**: When to use monoliths?

**Key Concepts:**
- Global state and direct function calls
- Tight coupling between components
- Simple deployment and development

### Part 2: Layered Architecture
**Complexity: 🟡 Intermediate**
1. **Theory**: Separation of concerns, controlled communication
2. **Implementation**: Complete `02-layered/library_system.py`
3. **Discussion**: Benefits and limitations

**Key Concepts:**
- Data Access → Business Logic → Presentation layers
- Controlled inter-layer communication
- Service isolation and testability

### Part 3: Event-Driven Architecture
**Complexity: 🔴 Advanced**
1. **Theory**: Loose coupling, async communication
2. **Implementation**: Complete `03-eventdriven/library_system.py`
3. **Discussion**: Scalability and distributed systems

**Key Concepts:**
- Message broker and event routing
- Service isolation through events
- Eventually consistent systems
- Event sourcing and audit trails

### Part 4: Comparison and Wrap-up
- Compare the three implementations
- Discuss architectural trade-offs
- Real-world application scenarios

## 🎓 Learning Workflow

### For Each Exercise:

1. **Read the Architecture Guide** (`guide.md`) - Understand theory and patterns
2. **Analyze Failing Tests** - They define exactly what to implement
3. **Implement Functions** - Follow TDD: Red → Green → Refactor
4. **Run Tests Frequently** - Get immediate feedback on progress
5. **Complete Integration** - Ensure all tests pass
6. **Compare with Solution** - When finished or stuck

### 🔍 Accessing Solutions

#### Option A: View Solutions Without Switching Branches (Recommended)
```bash
# View a solution file without leaving main branch
git show solutions:01-monolith/todo_manager.py

# Create a reference file for comparison
git show solutions:01-monolith/todo_manager.py > solution_reference.py
```

#### Option B: Switch to Solutions Branch
```bash
# Save your work first!
git add .
git commit -m "My progress on monolith exercise"

# Switch to solutions branch
git checkout solutions

# View complete implementations
cat 01-monolith/todo_manager.py

# Return to main branch
git checkout main
```

#### Option C: Use Git Stash (Temporary Save)
```bash
# Temporarily save your work
git stash push -m "Monolith exercise progress"

# Switch to solutions
git checkout solutions

# Return to main and restore work
git checkout main
git stash pop
```

## 🛡️ Protecting Your Work

### Always Save Before Switching Branches:
```bash
# Method 1: Commit your work
git add .
git commit -m "Exercise progress"

# Method 2: Stash your work  
git stash push -m "Work in progress"

# Method 3: Create backup files
cp 01-monolith/todo_manager.py my_backup.py
```

### Check Status Before Switching:
```bash
git status  # See what files you've modified
git diff    # See your changes
```

## 🔍 Key Architectural Patterns

### **Monolithic Architecture:**
- ✅ Simple development and deployment
- ✅ Direct function calls and shared state
- ❌ Difficult to scale individual components
- ❌ Tight coupling between all parts

### **Layered Architecture:**
- ✅ Clear separation of concerns  
- ✅ Each layer has specific responsibility
- ✅ Easier to test and maintain
- ❌ Can become rigid and bottlenecked

### **Event-Driven Architecture:**
- ✅ Loose coupling between services
- ✅ Highly scalable and flexible
- ✅ Independent service development
- ❌ More complex to debug and reason about
- ❌ Eventually consistent (not immediately)

## 🚧 Common Pitfalls and Tips

### General Tips:
- **Read test names carefully** - They describe what to implement
- **Start with simple functions** - Build complexity gradually
- **Run tests frequently** - Get immediate feedback
- **Read error messages** - They guide you to the problem
- **Don't copy solutions early** - Try to understand the problem first

### TDD-Specific Tips:
- **Focus on making tests pass** - Don't over-engineer initially
- **One test at a time** - Implement incrementally
- **Tests are requirements** - They define expected behavior
- **Red-Green-Refactor** - Fail → Pass → Improve

### Git Workflow Tips:
- **Save work before switching branches** - Avoid losing progress
- **Use meaningful commit messages** - Track your progress
- **Create backup files** - Safety net for important work
- **Check `git status` often** - Know what you've changed

## 📚 Educational Benefits

### Why This TDD Approach Works:
1. **Immediate Feedback** - Know instantly if you're on track
2. **Clear Requirements** - No ambiguity about what to implement
3. **Progressive Learning** - Build complexity step by step
4. **Professional Skills** - Learn industry-standard TDD practices
5. **AI-Resistant** - Must understand logic, not just fill blanks

### Architecture Learning Path:
```
Simple → Organized → Distributed
  ↓         ↓           ↓
Monolith → Layered → Event-Driven
  ↓         ↓           ↓
Direct   → Layer    → Message
Calls      Isolation   Passing
```

## 🏆 Success Criteria

Your understanding will be demonstrated by:
- **All tests passing** - Correct implementation
- **Clean code structure** - Following architectural principles
- **Explaining trade-offs** - Understanding when to use each pattern
- **Progressive complexity** - Appreciating the learning journey

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use this material for educational purposes
- ✅ Modify and adapt for your own courses
- ✅ Share with students and colleagues
- ✅ Create derivative works

## 🎉 Acknowledgments

- Inspired by real-world architectural patterns used in industry
- Test-driven approach based on modern software development practices
- Educational methodology designed for progressive skill building
- Examples chosen for clarity and practical relevance

---

**Ready to master software architecture through hands-on practice? Let's build! 🚀**

*Questions? Issues? Create a GitHub issue or reach out during the workshop.*

**Happy coding and architectural thinking!** 🏗️