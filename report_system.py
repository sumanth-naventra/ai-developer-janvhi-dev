import json

# ✅ Dummy student answers (later you will replace with real input)
student_answers = {
    "aptitude": [
        {"topic": "Percentages", "correct": True},
        {"topic": "Time & Work", "correct": False},
        {"topic": "Series", "correct": True},
        {"topic": "Ratios", "correct": False},
        {"topic": "Ages", "correct": False}
    ],
    "reasoning": [
        {"topic": "Puzzle", "correct": True},
        {"topic": "Direction Sense", "correct": False},
        {"topic": "Odd One Out", "correct": True},
        {"topic": "Pattern", "correct": True},
        {"topic": "Clock & Time", "correct": False}
    ],
    "verbal": [
        {"topic": "Vocabulary", "correct": False},
        {"topic": "Grammar", "correct": True},
        {"topic": "Reading", "correct": True},
        {"topic": "Synonyms", "correct": False},
        {"topic": "Antonyms", "correct": True}
    ],
    "difficulty": "Medium"
}

# ✅ Initialize report structure
report = {
    "score": {},
    "weak_topics": [],
    "feedback": "",
    "focus_suggestion": "",
    "difficulty": student_answers["difficulty"]
}

weak_topics_list = []

# ✅ Calculate score and weak topics
for section, answers in student_answers.items():
    if section == "difficulty":
        continue

    total = len(answers)
    correct = sum(1 for q in answers if q["correct"])
    report["score"][section] = f"{correct}/{total}"

    for q in answers:
        if not q["correct"]:
            weak_topics_list.append(q["topic"])

report["weak_topics"] = weak_topics_list

# ✅ Generate simple feedback
if len(weak_topics_list) == 0:
    report["feedback"] = "Excellent performance! No weak topics."
else:
    report["feedback"] = "You need improvement in the following topics."

report["focus_suggestion"] = f"Focus on: {', '.join(weak_topics_list)}"

# ✅ Save to file
with open("student_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("✅ Student report generated successfully.")
print("📁 Saved as student_report.json")
