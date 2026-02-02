# Grading Rubric - Trading Bot Application Task

## Evaluation Scale: 0-5 Points
- **0**: Not implemented / Fails completely
- **1**: Minimal implementation with major issues
- **2**: Basic implementation with significant issues
- **3**: Acceptable implementation with some issues
- **4**: Good implementation with minor issues
- **5**: Excellent implementation, professional quality

---

## 1. Correctness (25 points)

### 1.1 Order Placement (10 points)
- [ ] **5 pts**: Successfully places MARKET orders on testnet
- [ ] **5 pts**: Successfully places LIMIT orders on testnet

**Score**: _____ / 10

### 1.2 Order Sides (5 points)
- [ ] **2.5 pts**: BUY orders work correctly
- [ ] **2.5 pts**: SELL orders work correctly

**Score**: _____ / 5

### 1.3 API Integration (10 points)
- [ ] **5 pts**: Correctly uses Binance Futures Testnet endpoint
- [ ] **3 pts**: Proper authentication (API key, signature)
- [ ] **2 pts**: Handles API responses correctly

**Score**: _____ / 10

**Total Correctness Score**: _____ / 25

---

## 2. Code Quality (25 points)

### 2.1 Structure & Organization (10 points)
- [ ] **3 pts**: Clear separation of concerns (client/CLI layers)
- [ ] **3 pts**: Modular design with reusable components
- [ ] **2 pts**: Logical file/folder structure
- [ ] **2 pts**: Follows Python naming conventions

**Score**: _____ / 10

### 2.2 Readability (8 points)
- [ ] **3 pts**: Clear, meaningful variable/function names
- [ ] **2 pts**: Appropriate comments and docstrings
- [ ] **2 pts**: Consistent code style
- [ ] **1 pt**: Type hints (bonus)

**Score**: _____ / 8

### 2.3 Reusability (7 points)
- [ ] **4 pts**: Client wrapper can be used independently
- [ ] **3 pts**: Functions/classes are reusable components

**Score**: _____ / 7

**Total Code Quality Score**: _____ / 25

---

## 3. Validation & Error Handling (20 points)

### 3.1 Input Validation (8 points)
- [ ] **2 pts**: Validates symbol format
- [ ] **2 pts**: Validates side (BUY/SELL)
- [ ] **2 pts**: Validates order type (MARKET/LIMIT)
- [ ] **2 pts**: Validates quantity (positive number)
- [ ] **2 pts**: Validates price (required for LIMIT)

**Score**: _____ / 8

### 3.2 Error Handling (12 points)
- [ ] **4 pts**: Handles API errors gracefully
- [ ] **3 pts**: Handles network failures (timeout, connection)
- [ ] **3 pts**: Handles invalid input errors
- [ ] **2 pts**: Provides clear error messages to user

**Score**: _____ / 12

**Total Validation & Error Handling Score**: _____ / 20

---

## 4. Logging (15 points)

### 4.1 Log Completeness (8 points)
- [ ] **3 pts**: Logs API requests with parameters
- [ ] **3 pts**: Logs API responses
- [ ] **2 pts**: Logs errors with context

**Score**: _____ / 8

### 4.2 Log Quality (7 points)
- [ ] **3 pts**: Appropriate log levels (DEBUG, INFO, ERROR)
- [ ] **2 pts**: Structured, readable log format
- [ ] **2 pts**: Not too verbose, not too sparse

**Score**: _____ / 7

**Total Logging Score**: _____ / 15

---

## 5. Documentation (10 points)

### 5.1 README.md (7 points)
- [ ] **2 pts**: Clear setup instructions
- [ ] **2 pts**: Usage examples with commands
- [ ] **2 pts**: Explains project structure
- [ ] **1 pt**: Troubleshooting section

**Score**: _____ / 7

### 5.2 Code Documentation (3 points)
- [ ] **2 pts**: Key functions have docstrings
- [ ] **1 pt**: Inline comments where needed

**Score**: _____ / 3

**Total Documentation Score**: _____ / 10

---

## 6. CLI Interface (5 points)

### 6.1 User Experience (5 points)
- [ ] **2 pts**: Clear command structure
- [ ] **1 pt**: Formatted output (readable)
- [ ] **1 pt**: Help text available
- [ ] **1 pt**: Success/failure messages clear

**Score**: _____ / 5

**Total CLI Score**: _____ / 5

---

## Bonus Points (5 points)

### Additional Features (up to 5 points)
- [ ] **2 pts**: Additional order types (Stop-Loss, OCO, etc.)
- [ ] **2 pts**: Enhanced CLI UX (menus, prompts, rich formatting)
- [ ] **2 pts**: Additional useful commands (balance check, etc.)
- [ ] **1 pt**: Testing scripts or unit tests
- [ ] **1 pt**: Exceptional documentation or architecture docs

**Bonus Score**: _____ / 5

---

## Total Score Calculation

| Category | Score | Weight | Weighted Score |
|----------|-------|--------|----------------|
| Correctness | ___ / 25 | 100% | ___ |
| Code Quality | ___ / 25 | 100% | ___ |
| Validation & Errors | ___ / 20 | 100% | ___ |
| Logging | ___ / 15 | 100% | ___ |
| Documentation | ___ / 10 | 100% | ___ |
| CLI Interface | ___ / 5 | 100% | ___ |
| **Subtotal** | **___ / 100** | | |
| Bonus Points | ___ / 5 | | ___ |
| **Total** | **___ / 105** | | |

---

## Final Grade Scale

| Score Range | Grade | Decision |
|-------------|-------|----------|
| 90-105 | A+ | **Strongly recommend** for interview |
| 80-89 | A | **Recommend** for interview |
| 70-79 | B | **Consider** for interview |
| 60-69 | C | Borderline - discuss with team |
| Below 60 | D/F | Do not advance |

---

## Red Flags (Automatic Fail)

Check if any of these apply:
- [ ] Doesn't run / crashes on startup
- [ ] Cannot place orders at all
- [ ] No error handling whatsoever
- [ ] No logging implementation
- [ ] Missing README or setup instructions
- [ ] Hardcoded API credentials in code
- [ ] Uses wrong endpoint (mainnet instead of testnet)

**Red Flags Present**: _____ (If any checked, consider carefully)

---

## Reviewer Notes

### Strengths:
```
[Space for reviewer comments on what the candidate did well]




```

### Areas for Improvement:
```
[Space for reviewer comments on what could be better]




```

### Overall Impression:
```
[Space for overall assessment and recommendation]




```

---

## Interview Decision

- [ ] **Advance to Interview** - Strong candidate
- [ ] **Advance to Interview** - Acceptable candidate
- [ ] **Discuss with Team** - Borderline case
- [ ] **Do Not Advance** - Does not meet requirements

**Reviewer Name**: _________________  
**Date**: _________________  
**Signature**: _________________

---

## Quick Checklist for Fast Screening

Use this for initial filtering before detailed scoring:

**Must-Have Features** (all must be YES):
- [ ] Can place MARKET orders
- [ ] Can place LIMIT orders  
- [ ] Has input validation
- [ ] Has error handling
- [ ] Has logging to files
- [ ] Has README with setup instructions
- [ ] Structured code (not single file)

**If ANY must-have is NO, score automatically < 60**

**Quality Indicators** (count YES answers):
- [ ] Type hints used
- [ ] Clean code structure
- [ ] Good variable naming
- [ ] Docstrings present
- [ ] Handles edge cases
- [ ] Professional output formatting
- [ ] Additional features beyond requirements

**7/7 = A+, 5-6/7 = A, 3-4/7 = B, 1-2/7 = C, 0/7 = D**

---

**This rubric designed for**:  
Anything.ai - Junior Python Developer Position  
Trading Bot Application Task  
February 2026
