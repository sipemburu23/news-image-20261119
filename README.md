# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sipemburu23/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sipemburu23/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One newspaper front page summing up Thursday 19 November 2026: 49 stories,
15 drawn (3 leads + 12 cards), 7 regions including Oceania, a UTC timeline,
a DATE CHECK of stories left out on purpose, and a solid world map.

The image is drawn from scratch with Pillow (`draw.py`, flat vector art only)
and baked into the repo as `entry.png`. `main.ts` only copies that baked
image to the output directory — it never runs the drawing code.

## Run it

```sh
node main.ts
# writes entry.png to $OUTPUT_DIR (default /output)
```

To redraw the image (build time only):

```sh
python3 draw.py
```

Referral code: `f6p8nnb7`
