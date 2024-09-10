# twitch_shoutout_bot
This bot will automatically !so people that enter your stream on a cooldown, and while waiting for others to get their fair share of shoutout time.

## Install
- Download the latest build below and extract the zip
- Visit https://twitchtokengenerator.com/
- Select "Bot Chat Token" on the popup
- On the twitch authorization dialog, either log in or click the "authorize" button (purple)
- You may need to prove you're not a robot
- Copy the "access token" that is updated on screen.
- Run shoutout_bot.exe
- add the "access token" to the "twitch token" section of the window
- Add your channel name (ex: eldoonnemar)

## Usage
Once the bot is running, you can use the following commands in chat (even if you're offline) to add and remove shoutouts.
- ```!addso @username```
- ```!removeso @username```

## FAQ
- Will the bot give shoutouts while i'm offline if someone enters chat?
  - Nope.. it'll wait until you're live to begin giving shoutouts
- Can I add and remove people from chat while i'm offline?
  - Yup, just use the commands above and the bot will respond so long as you're running it on your system
- Can I close the app after stream?
  - Yes, the bot doesn't need to be running when you're not streaming, but it does need to be running on "a" pc when you're streaming to know when to show out. It contains a database for tracking shoutouts etc
- Does it do /shoutout @username?
  - Nope.. all this bot does is look for people you've told it to watch, and if they enter chat and say something, it will just send a ```!so @username```. This means you need to have another bot like moobot waiting to respond to !so messages.
- Will you eventually do your own shoutouts instead of relying on another bot to do it?
  - Yeah, i'll be adding that later.
  
## Other config items
- Bot Prefix
  - This lets you set what you type before addso and removeso. We suggest you leave this at !. It won't conflict with any other bots, but you might see warnings in the console about unrecognized commands if you have more than one bot
- Shoutout Wait Seconds
  - This is how long we wait between shoutouts if more than one person you've added comes into your channel at once. This will ensure that everyone gets their fair share of shoutout time with the timer at the top of chat.
- Shoutout Cooldown Hours
  - This is the number of hours between each users shoutout. The default is 12 hours, which means even if you stop and start your stream, the same people won't get a shoutout until this timer expires.

## Latest Build
https://github.com/HawtDogFlvrWtr/twitch_shoutout_bot/releases/download/1.0/shoutout_users.zip
