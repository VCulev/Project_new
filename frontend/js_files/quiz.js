document.addEventListener('DOMContentLoaded', async () => {
    const quizContainer = document.getElementById('quizContainer');
    const submitBtn = document.getElementById('submitBtn');
    const feedbackContainer = document.getElementById('feedbackContainer');
    let currentQuestionIndex = 0;
    let selectedAnswerIndex = -1;
    let score = 0;
    let questions = [];
    let selectedAnswers = [];

    const fetchQuizQuestions = async () => {
        try {
            const response = await fetch('http://localhost:4000/api/quiz');
            if (!response.ok) {
                throw new Error('Failed to fetch quiz questions');
            }
            const data = await response.json();
            return data.results;
        } catch (error) {
            throw new Error('Error fetching quiz questions: ' + error.message);
        }
    };

    const displayQuizQuestions = () => {
        feedbackContainer.innerHTML = '';

        const question = questions[currentQuestionIndex];
        const decodedQuestion = decodeURIComponent(question.question);
        const questionElement = document.createElement('div');
        questionElement.innerHTML = `
            <p class="text-lg font-semibold">${decodedQuestion}</p>
        `;
        const answersElement = document.createElement('div');
        question.incorrect_answers.forEach((answer, index) => {
            const decodedAnswer = decodeURIComponent(answer);
            answersElement.innerHTML += `
                <div class="answer p-2 rounded-md border" data-index="${index}">
                    <span>${decodedAnswer}</span>
                </div>
            `;
        });
        const correctIndex = question.incorrect_answers.length;
        const decodedCorrectAnswer = decodeURIComponent(question.correct_answer);
        answersElement.innerHTML += `
            <div class="answer p-2 rounded-md border" data-index="${correctIndex}">
                <span>${decodedCorrectAnswer}</span>
            </div>
        `;
        questionElement.appendChild(answersElement);
        quizContainer.innerHTML = '';
        quizContainer.appendChild(questionElement);

        selectedAnswerIndex = -1;

        const answers = quizContainer.querySelectorAll('.answer');
        answers.forEach(answer => {
            answer.classList.remove('selected');
            answer.addEventListener('click', selectAnswer);
        });
    };

    const selectAnswer = (event) => {
        const target = event.target.closest('.answer');
        if (target && !target.classList.contains('selected')) {
            const index = parseInt(target.getAttribute('data-index'));
            selectedAnswerIndex = index;

            const answers = quizContainer.querySelectorAll('.answer');
            answers.forEach(answer => {
                answer.classList.remove('selected');
            });

            target.classList.add('selected');
        }
    };

    const submitAnswer = () => {
        if (selectedAnswerIndex === -1) {
            feedbackContainer.innerText = 'Please select an answer.';
            return;
        }
        const question = questions[currentQuestionIndex];
        const correctIndex = question.incorrect_answers.length;
        const isCorrect = (selectedAnswerIndex === correctIndex);

        selectedAnswers.push({
            question: decodeURIComponent(question.question),
            selectedAnswer: decodeURIComponent(
                selectedAnswerIndex < correctIndex
                    ? question.incorrect_answers[selectedAnswerIndex]
                    : question.correct_answer
            ),
            correctAnswer: decodeURIComponent(question.correct_answer),
            isCorrect: isCorrect
        });

        if (isCorrect) {
            score++;
        }
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            displayQuizQuestions();
        } else {
            displayResults();
        }
    };

    const displayResults = () => {
        const percentage = (score / questions.length) * 100;
        feedbackContainer.innerHTML = `
            <p>You scored ${percentage.toFixed(2)}% (${score}/${questions.length}).</p>
            <button id="playAgainBtn" class="bg-blue-500 text-white py-2 px-4 rounded-md mt-4 mr-2">Play Again</button>
            <button id="nextQuizBtn" class="bg-blue-500 text-white py-2 px-4 rounded-md mt-4">Next Quiz</button>
            <div class="mt-4">
                ${selectedAnswers.map(answer => `
                    <div class="mb-2">
                        <p><strong>Question:</strong> ${answer.question}</p>
                        <p><strong>Your Answer:</strong> <span class="${answer.isCorrect ? 'feedback-correct' : 'feedback-incorrect'}">${answer.selectedAnswer}</span></p>
                        <p><strong>Correct Answer:</strong> <span class="feedback-correct">${answer.correctAnswer}</span></p>
                        <p><strong>Correct:</strong> ${answer.isCorrect ? 'Yes' : 'No'}</p>
                    </div>
                `).join('')}
            </div>
        `;
        quizContainer.innerHTML = '';
        submitBtn.style.display = 'none';

        const playAgainBtn = document.getElementById('playAgainBtn');
        playAgainBtn.addEventListener('click', () => {
            resetQuiz();
            displayQuizQuestions();
        });

        const nextQuizBtn = document.getElementById('nextQuizBtn');
        nextQuizBtn.addEventListener('click', async () => {
            resetQuiz();
            try {
                questions = await fetchQuizQuestions();
                displayQuizQuestions();
            } catch (error) {
                console.error(error.message);
                feedbackContainer.innerText = 'Error fetching quiz questions.';
            }
        });
    };

    const resetQuiz = () => {
        currentQuestionIndex = 0;
        score = 0;
        selectedAnswers = [];
        submitBtn.style.display = 'block';
        feedbackContainer.innerHTML = '';
    };

    const initializeQuiz = async () => {
        try {
            questions = await fetchQuizQuestions();
            displayQuizQuestions();
            submitBtn.addEventListener('click', submitAnswer);
        } catch (error) {
            console.error(error.message);
            feedbackContainer.innerText = 'Error fetching quiz questions.';
        }
    };

    await initializeQuiz();

    quizContainer.addEventListener('click', selectAnswer);
});
