import random
import PIL
from collections import namedtuple

from PIL import Image, ImageDraw

GaussianDistribution = namedtuple('GaussianDistribution', ['mu', 'sigma'])
Platform = namedtuple('Platform', ['start', 'end', 'height'])
Point = namedtuple('Point', ['x', 'y'])

PLATFORM_HEIGHT_DISTRIBUTION = GaussianDistribution(50, 10)
PLATFORM_WIDTH_DISTRIBUTION = GaussianDistribution(100, 10)
INTER_PLATFORM_DISTRIBUTION = GaussianDistribution(500, 20)

RANDOM = random.Random()


def sample_distribution(distribution):
    return RANDOM.normalvariate(distribution.mu, distribution.sigma)


def create_platforms(num_platforms):
    last_platform_end = 0

    for i in range(num_platforms):
        start = int(sample_distribution(INTER_PLATFORM_DISTRIBUTION) + last_platform_end)
        end = int(sample_distribution(PLATFORM_WIDTH_DISTRIBUTION) + start)
        height = int(sample_distribution(PLATFORM_HEIGHT_DISTRIBUTION))

        last_platform_end = end

        yield Platform(start, end, height)


def create_mountains_between_points(p1, p2):
    mountain_start = p1.x
    mountain_end = p2.x

    num_points = int((mountain_end - mountain_start) / 10)

    for i in range(num_points):
        # TODO: use 1D Perlin function to generate point.y
        yield Point(mountain_start + i * 10, RANDOM.random() * 100)


def create_terrain(platforms):
    origin = Point(0, 0)
    first_platform_start = Point(platforms[0].start, platforms[0].height)

    terrain = []
    terrain += list(create_mountains_between_points(origin, first_platform_start))

    for i, platform in enumerate(platforms):
        platform_starts_at = Point(platform.start, platform.height)
        platform_ends_at = Point(platform.end, platform.height)

        terrain.append(platform_starts_at)
        terrain.append(platform_ends_at)

        if i < len(platforms) - 1:
            next_platform = platforms[i + 1]
            next_platform_starts_at = Point(next_platform.start, next_platform.height)
            mountains = create_mountains_between_points(platform_ends_at, next_platform_starts_at)
            terrain += mountains

    return terrain


def draw_terrain(terrain):
    im = Image.new('RGBA', (4000, 200), (255, 255, 255, 0))

    draw = ImageDraw.Draw(im)
    draw.line(terrain, fill=(0, 0, 0, 255))

    im.show()


if __name__ == '__main__':
    platforms = list(create_platforms(num_platforms=10))
    terrain = create_terrain(platforms)
    draw_terrain(terrain)