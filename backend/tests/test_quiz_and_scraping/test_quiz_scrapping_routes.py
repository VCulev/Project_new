from backend.tests.modules.modules import api_url, urls
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_quiz():
    async with AsyncClient() as client:
        print(f"[GET_QUIZ]: ", end="")
        response = await client.get(
            api_url(urls["QUIZ"]),
        )

        j_response = response.json()

        if response.status_code != 200:
            print(f"[ERROR]: {j_response}", end="")

        assert response.status_code == 200
        assert "results" in j_response
        assert len(j_response["results"]) == 10
        assert "category" in j_response["results"][0]
        assert "type" in j_response["results"][0]
        assert "difficulty" in j_response["results"][0]
        assert "question" in j_response["results"][0]

        print(f"[OK]: {j_response}", end="")


@pytest.mark.asyncio
async def test_scrape_questions():
    async with AsyncClient() as client:
        print(f"[SCRAPE_QUESTIONS]: ", end="")
        response = await client.get(
            api_url(urls["SCRAPING"]),
        )

        j_response = response.json()

        if response.status_code != 200:
            print(f"[ERROR]: {j_response}", end="")

        assert response.status_code == 200
        assert isinstance(j_response, list)
        for i, question in enumerate(j_response):
            assert 'title' in question
            assert 'link' in question

        print(f"[OK]: {j_response}", end="")