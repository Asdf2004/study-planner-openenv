tasks = {
    "easy": {
        "target": 30,
        "grader": lambda score: min(max(score/30,0.01),0.99)
    },

    "medium": {
        "target": 60,
        "grader": lambda score: min(max(score/60,0.01),0.99)
    },

    "hard": {
        "target": 100,
        "grader": lambda score: min(max(score/100,0.01),0.99)
    }
}
