
from asyncio.windows_events import NULL


def combinada(x, y=10, *args, **kwargs):
    return x, y, args, kwargs

print(f"Lambda combinada (1, 20, 30, 40, z=50): {combinada(1, 20, 30, 40, z=50)}")
# Output: (1, 20, (30, 40), {'z': 50}) -> x=1, y=20 (override default), args=(30, 40), kwargs={'z': 50}
