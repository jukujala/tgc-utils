# Python utilities for The Game Crafter (TGC).

This repo has Python utilities to help create games in
[TGC](https://www.thegamecrafter.com/).
Now this repo includes code to upload card images to a TGC Euro Poker Deck.
You need to first create in TGC your custom game and add the custom deck component to it.

# Install

```
pip install git+https://github.com/jukujala/tgc-utils
```

# How: upload cards to a deck in TGC

## Step 1: convert image files at path

Ensure that each card image is of correct size and has a black margin to print well.
Note: the code supports currently only the
[Euro Poker Deck](https://www.thegamecrafter.com/make/products/EuroPokerDeck)
custom component.

Example command:

```
python -m tgc_utils.convert_card_images \
  --input ./tests/data/euro_card_images \
  --output ./tests/data/output_example
```

## Step 2: upload the cards to an existing TGC deck

Prerequisites:

- You completed the Step 1 above :-)

- You created a TGC secrets JSON file:

  ```
  {
    "api_key_id": <Your personal TGC API key ID>,
    "username": <Your personal TGC username>,
    "password": <Your personal TGC password>
  }
  ```

  The `username` and `password` are created by you when you create your account.
  TGC provides
  [instructions](https://www.thegamecrafter.com/developer/APIKey.html)
  how to get your `api_key_id`.

- You have a TGC game and have added Euro Poker Deck to it.

- Find a TGC deck ID to upload the files.
  It is the last part of the URL when you navigate to the custom Euro Poker Deck:
  `https://www.thegamecrafter.com/make/games/<game ID>/EuroPokerDeck/<deck ID>`.

Example command:

```
python -m tgc_utils.upload_cards \
  --input ./tests/data/output_example \
  --deck_id <deck ID> \
  --secrets_json <secrets file>
```
