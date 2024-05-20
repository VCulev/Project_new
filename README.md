# Tech Insights Hub

Welcome to Tech Insights Hub, an innovative platform designed to keep you informed and entertained in the world of technology. This project leverages a robust tech stack to deliver an interactive and educational experience, perfect for tech enthusiasts of all levels.

## Project Overview

Tech Insights Hub combines various cutting-edge technologies to create a seamless and engaging user experience. From web scraping to dynamic quizzes, here's a glimpse into the tools and technologies powering this project:

- **Sanic**: Fast, lightweight Python web framework with asynchronous capabilities.
- **MongoDB**: NoSQL database for storing user data and quiz questions.
- **Redis**: In-memory data structure store for caching and session management.
- **BeautifulSoup**: Python library for web scraping to fetch the latest tech news.
- **Asyncio**: Python library for writing concurrent code using async/await.
- **HTTPX**: Fully featured HTTP client for making asynchronous API calls.
- **Pytest**: Testing framework for writing scalable and maintainable tests.
- **JavaScript**: For creating dynamic and interactive user interfaces.
- **CSS**: To style HTML documents, ensuring a responsive and visually appealing design.
- **HTML**: Standard markup language for creating web pages.

## Features

Tech Insights Hub offers several exciting features designed to engage and inform:

- **Tech Newsletter**: Stay updated with the latest news and trends in the tech world. Our application scrapes recent articles from Stack Overflow and presents them in a clean, readable format.
- **Tech Quiz**: Test your knowledge with quizzes tailored to the tech industry. Quizzes are dynamically fetched from a third-party API and stored in MongoDB for easy access.
- **Easter Egg**: Keep an eye out for a special hidden feature that adds a touch of fun to your exploration of the platform!

## Why Tech Insights Hub?

The main goal of Tech Insights Hub is to provide an engaging platform for learning and staying informed about technology. Whether you're a seasoned developer or a curious beginner, there's something here for you. By combining various technologies and methodologies, this project ensures a robust and user-friendly experience.

## How to Run

To get started with Tech Insights Hub:

1. Clone the repository:
    ```bash
    git clone https://github.com/VCulev/Project_new.git
    ```
   or
   ```bash
    git clone git@github.com:VCulev/Project_new.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Project_new
    ```

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure you have Docker installed and running on your machine. Start the Docker containers:
    ```bash
    cd backend
    docker-compose up -d
    ```
    You should see messages indicating that the containers for Redis and MongoDB have started.

5. Start the Sanic server:
    - Open `main.py` file in the backend directory in your IDE and run it. This will start the server.

6. Open the frontend:
    - Navigate to the Frontend directory and open the `index.html` file in your browser.

7. Explore the web application:
    - Use the navbar to navigate between Quiz, Newsletter, and About pages.
    - On the About page, click the "Surprise Easter Egg" button to discover a hidden feature.
    - On the Newsletter page, view the latest questions and topics from Stack Overflow.

8. To stop the server:
    - Stop the `main.py` script in your IDE.
    - Quit Docker Desktop by clicking on the Docker icon and selecting "Quit Docker Desktop."

## Running Tests

To run the tests for Tech Insights Hub:

1. Navigate to the tests directory and make sure that Docker and the server are running :
    ```bash
    cd backend/tests
    ```

2. To run the authentication tests:
    ```bash
    cd auth_test
    pytest
    ```

3. To run the quiz and scraping tests:
    ```bash
    cd test_quiz_and_scraping
    pytest
    ```

    Alternatively, you can open the test files in your IDE and run them directly.

## API Response Codes

- **BadRequest (400)**
- **Unauthorized (401)**
- **Forbidden (403)**
- **NotFound (404)**
- **ServerError (500)**

Thank you for trying out Tech Insights Hub!
