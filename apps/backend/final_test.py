import asyncio
from app.services.improver import classify_skills

async def test():
    result = await classify_skills(['Python', 'JavaScript', 'TypeScript', 'AWS', 'Docker', 'Kubernetes', 'PostgreSQL', 'React'])
    print('Success! Categories:', len(result))
    for cat in result:
        print(f'  {cat["name"]}: {cat["skills"]}')

asyncio.run(test())
