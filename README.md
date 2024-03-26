# Poeflipper

### How to use: ###

***Make sure to operate on the release branch. We do not want to use main***

--> Run all commands from main project folder

git clone https://github.com/Menatos/Poeflipper.git

cd home/menatos/projects/Poeflipper

git checkout Release-1.0_3.24

add .env with DISCORD_BOT_TOKEN to project folder

sudo bash run.sh

Alternatively, you can run the release script which takes care of all of these steps.

--> check running jobs with jobs -l
--> check ids with ps -aux
--> kill all running jobs -- pkill -9 -f "python"

This is the Poeflipper discord bot. It has been developed to help you increase your currency gains during the Path of
exile leagues using a diverse amount of useful functions to help you maximize income

### Currently available functions ###

***All data is based on poe.ninja***

```/help``` displays all available methods and a short description

```/refresh_database``` refreshes the database manually. Usually, it is refreshed automatically every hour.

```/divcards_currency``` displays the cost of divination cards that reward currency and the cost of the rewards recieved
on turning them in

``/divcards_fragments`` displays the cost of divination cards that reward fragments and the cost of the rewards recieved
on turning them in

```/divcards_uniques``` displays the cost of divination cards that reward uniques and the cost of the rewards recieved
on turning them in

```/divcards_skillgems``` displays the cost of divination cards that reward skill gems and the cost of the rewards
recieved on turning them in

```/price_changes``` displays all items that have had a price change of over 30% over the last seven days.

```/predict_prices``` Takes an item as input to predict price of the items in 7 days. This value is based on the current
value of the item and the value in 7 days based on last leagues prices


Github Page:

https://github.com/Menatos/Poeflipper

Trello Page:

https://trello.com/b/NKxPpaI1/poeflipper

