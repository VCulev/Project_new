async def register_user(request):
    result = await request.app['requests'].register_user(request.json)
    return result


async def login_user(request):
    result = await request.app['requests'].login_user(request.json)
    return result


async def user_input(request):
    result = await request.app['requests'].receive_user_input(request.json)
    return result


async def scrape_courses(request):
    result = await request.app['requests'].scrape_courses(request.json)
    return result


async def recommendations(request):
    result = await request.app['requests'].generate_recommendations(request.json)
    return result


async def generate_courses(request):
    result = await request.app['requests'].generate_course_list(request.json)
    return result


async def display_results(request):
    result = await request.app['requests'].display_courses(request.json)
    return result
