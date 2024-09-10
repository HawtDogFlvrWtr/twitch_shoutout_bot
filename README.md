# twitch_shoutout_bot
This bot will automatically !so people that enter your stream on a cooldown, and while waiting for others to get their fair share of shoutout time.

## Insall
- Visit https://twitchtokengenerator.com/
- Select "Bot Chat Token" on the popup
- On the twitch authorization dialog, either log in or click the "authorize" button (purple)
- You may need to prove you're not a robot
- Copy the "access token" that is updated on screen.
- Run shoutout_bot.exe
- add the "access token" to the "twitch token" section of the window
- Add your channel name (ex: eldoonnemar)

## Usage
Once the bot is running, you can use the following commands in chat to add and remove shoutouts
!addso @username
!removeso @username

## Other config items
- Bot Prefix
  - This lets you set what you type before addso and removeso. We suggest you leave this at !. It won't conflict with any other bots, but you might see warnings in the console about unrecognized commands if you have more than one bot
- Shoutout Wait Seconds
  - This is how long we wait between shoutouts if more than one person you've added comes into your channel at once. This will ensure that everyone gets their fair share of shoutout time with the timer at the top of chat.
- Shoutout Cooldown Hours
  - This is the number of hours between each users shoutout. The default is 12 hours, which means even if you stop and start your stream, the same people won't get a shoutout until this timer expires.
