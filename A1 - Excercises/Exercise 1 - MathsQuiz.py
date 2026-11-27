import tkinter as tk
import random

# Colours
BG = "#101827"
CARD = "#1C293B"
YELLOW = "#9CB800"
WHITE = "#FFFFFF"
GREY = "#AAB6C8"
GREEN = "#36C98F"
RED = "#F16C78"

# Quiz variables
score = 0
questionNumber = 1
attempts = 0
difficulty = ""

# Window
window = tk.Tk()
window.title("Maths Quiz")
window.geometry("750x550")
window.configure(bg=BG)
window.resizable(False, False)


# ---------------- FUNCTIONS ----------------

def clearScreen():
    for widget in window.winfo_children():
        widget.destroy()


def randomInt(minimum, maximum):
    return random.randint(minimum, maximum)


def decideOperation():
    return random.choice(["+", "-"])


def makeLabel(parent, text, size, colour, bold=False, background=CARD):
    return tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold" if bold else "normal"),
        fg=colour,
        bg=background
    )


def makeButton(parent, text, command, colour=YELLOW):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=colour,
        fg=WHITE,
        activebackground=colour,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        padx=15,
        pady=10,
        cursor="hand2"
    )


# ---------------- MAIN MENU ----------------

def displayMenu():
    clearScreen()

    makeLabel(window, "MATHS QUIZ", 28, WHITE, True, BG).pack(pady=(35, 5))
    makeLabel(window, "Test your maths skills", 12, GREY, background=BG).pack()

    card = tk.Frame(window, bg=CARD, padx=35, pady=25)
    card.pack(padx=100, pady=30, fill="x")

    makeLabel(card, "Choose Your Difficulty", 17, WHITE, True).pack(pady=10)

    makeButton(
        card, "EASY", lambda: startQuiz("Easy"), GREEN
    ).pack(fill="x", pady=7)

    makeButton(
        card, "MODERATE", lambda: startQuiz("Moderate")
    ).pack(fill="x", pady=7)

    makeButton(
        card, "ADVANCED", lambda: startQuiz("Advanced"), "#D65B83"
    ).pack(fill="x", pady=7)

    makeLabel(
        window, "10 Questions  |  2 Attempts  |  100 Points",
        10, GREY, background=BG
    ).pack(pady=5)


# ---------------- START QUIZ ----------------

def startQuiz(level):
    global score, questionNumber, attempts, difficulty

    score = 0
    questionNumber = 1
    attempts = 0
    difficulty = level

    showQuiz()
    displayProblem()


# ---------------- QUIZ SCREEN ----------------

def showQuiz():
    global questionLabel, answerEntry
    global feedbackLabel, scoreLabel, progressLabel

    clearScreen()

    header = tk.Frame(window, bg=BG)
    header.pack(fill="x", padx=35, pady=20)

    makeLabel(header, "MATHS QUIZ", 19, WHITE, True, BG).pack(side="left")
    makeLabel(header, difficulty.upper(), 11, YELLOW, True, BG).pack(side="right")

    info = tk.Frame(window, bg=BG)
    info.pack(fill="x", padx=40)

    progressLabel = makeLabel(info, "QUESTION 1 / 10", 10, GREY, True, BG)
    progressLabel.pack(side="left")

    scoreLabel = makeLabel(info, "SCORE: 0", 10, GREEN, True, BG)
    scoreLabel.pack(side="right")

    # Progress bar
    progress = tk.Frame(window, bg=CARD, height=8)
    progress.pack(fill="x", padx=40, pady=12)

    # Question card
    card = tk.Frame(window, bg=CARD, padx=30, pady=25)
    card.pack(fill="both", expand=True, padx=40, pady=10)

    makeLabel(card, "SOLVE THE QUESTION", 11, GREY, True).pack(pady=10)

    questionLabel = makeLabel(card, "", 34, WHITE, True)
    questionLabel.pack(pady=20)

    makeLabel(card, "Enter your answer", 11, GREY).pack(pady=5)

    answerEntry = tk.Entry(
        card,
        font=("Arial", 20),
        bg="#28374C",
        fg=WHITE,
        insertbackground=WHITE,
        justify="center",
        relief="flat",
        width=12
    )
    answerEntry.pack(ipady=8, pady=10)

    feedbackLabel = makeLabel(card, "", 11, WHITE)
    feedbackLabel.pack(pady=8)

    makeButton(card, "SUBMIT ANSWER", checkAnswer).pack(pady=10)

    makeLabel(
        window, "First attempt: 10 points     Second attempt: 5 points",
        10, GREY, background=BG
    ).pack(pady=10)

    answerEntry.bind("<Return>", lambda event: checkAnswer())


# ---------------- DISPLAY QUESTION ----------------

def displayProblem():
    global num1, num2, operation, correctAnswer, attempts

    attempts = 0

    # Select number range
    if difficulty == "Easy":
        if questionNumber <= 3:
            minimum, maximum = 1, 9
        elif questionNumber <= 7:
            minimum, maximum = 10, 99
        else:
            minimum, maximum = 100, 999

    elif difficulty == "Moderate":
        if questionNumber <= 3:
            minimum, maximum = 10, 99
        elif questionNumber <= 7:
            minimum, maximum = 100, 999
        else:
            minimum, maximum = 1000, 9999

    else:
        minimum, maximum = 1000, 9999

    num1 = randomInt(minimum, maximum)
    num2 = randomInt(minimum, maximum)
    operation = decideOperation()

    if operation == "+":
        correctAnswer = num1 + num2
    else:
        correctAnswer = num1 - num2

    questionLabel.config(
        text=f"{num1} {operation} {num2} = ?"
    )

    progressLabel.config(
        text=f"QUESTION {questionNumber} / 10"
    )

    scoreLabel.config(text=f"SCORE: {score}")

    feedbackLabel.config(text="")
    answerEntry.delete(0, tk.END)
    answerEntry.focus()


# ---------------- CHECK ANSWER ----------------

def isCorrect(answer):
    return answer == correctAnswer


def checkAnswer():
    global score, attempts

    try:
        answer = int(answerEntry.get())
    except ValueError:
        feedbackLabel.config(text="Please enter a valid number.", fg=RED)
        return

    if isCorrect(answer):
        if attempts == 0:
            score += 10
        else:
            score += 5

        scoreLabel.config(text=f"SCORE: {score}")
        feedbackLabel.config(text="Correct answer!", fg=GREEN)

        window.after(800, nextQuestion)

    else:
        attempts += 1

        if attempts == 1:
            feedbackLabel.config(text="Incorrect! Try again.", fg=RED)
            answerEntry.delete(0, tk.END)
            answerEntry.focus()
        else:
            feedbackLabel.config(
                text=f"Incorrect! Answer: {correctAnswer}",
                fg=RED
            )
            window.after(1200, nextQuestion)


# ---------------- NEXT QUESTION ----------------

def nextQuestion():
    global questionNumber

    questionNumber += 1

    if questionNumber > 10:
        displayResults()
    else:
        displayProblem()


# ---------------- RESULTS ----------------

def displayResults():
    clearScreen()

    makeLabel(window, "QUIZ COMPLETED!", 27, WHITE, True, BG).pack(pady=(40, 10))

    card = tk.Frame(window, bg=CARD, padx=40, pady=30)
    card.pack(fill="x", padx=100, pady=20)

    makeLabel(card, "YOUR FINAL SCORE", 12, GREY, True).pack(pady=10)

    makeLabel(card, f"{score} / 100", 38, GREEN, True).pack(pady=10)

    if score >= 90:
        grade = "A+"
        message = "Excellent work!"
    elif score >= 80:
        grade = "A"
        message = "Very good!"
    elif score >= 70:
        grade = "B"
        message = "Good job!"
    elif score >= 60:
        grade = "C"
        message = "Keep practising!"
    elif score >= 50:
        grade = "D"
        message = "You can improve!"
    else:
        grade = "F"
        message = "Try again!"

    makeLabel(card, f"Grade: {grade}", 20, YELLOW, True).pack(pady=5)
    makeLabel(card, message, 12, WHITE).pack(pady=5)

    makeButton(window, "PLAY AGAIN", displayMenu).pack(pady=8)
    makeButton(window, "EXIT", window.destroy, "#39475B").pack(pady=5)


# ---------------- RUN PROGRAM ----------------

displayMenu()
window.mainloop()
