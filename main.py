# Browser entry point for pygbag (itch.io / web play)
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'code'))

from main import Game  # noqa: E402


async def main():
  game = Game()
  while game.running:
    game.tick()
    await asyncio.sleep(0)


asyncio.run(main())
