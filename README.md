# Zelretch Addons

The official English-only Addon collection for Zelretch.

- **Repository:** `https://github.com/ChowdhurySiam/Zelretch-Addons`
- **Main project:** `https://github.com/ChowdhurySiam/Zelretch`
- **Developer:** [Siam Chowdhury](https://github.com/ChowdhurySiam)
- **Telegram:** [@Ch0wdhury_Siam](https://t.me/Ch0wdhury_Siam)
- **Interface language:** English only

## Repository structure

All executable Addons and their machine-readable catalog live inside the dedicated `Addons/` directory:

```text
Zelretch-Addons/
├── Addons/
│   ├── *.py
│   ├── requirements.txt
│   └── zelretch_addons.json
├── README.md
├── LICENSE
└── .gitattributes
```

The repository root contains project documentation and licensing only. Zelretch synchronizes modules exclusively from `Addons/`.

## Automatic installation

The main Zelretch project synchronizes the `Addons/` folder automatically at startup. The default repository is:

```text
https://github.com/ChowdhurySiam/Zelretch-Addons
```

## Addon catalog

| Addon | Purpose | Commands |
|---|---|---|
| 🪪 **Account Insights** | Displays detailed public information and activity estimates for a Telegram account. | `.aboutacc [username/reply]` |
| 🌙 **AFK Manager** | Sets an away status, records the reason, and responds to mentions until you return. | `.afk [reason]`, `.unafk` |
| 🤖 **AI Gateway** | Sends prompts to supported OpenRouter models from a single command. | `.ai [Gemini/DeepSeek/Qwen] [message]` |
| 🌸 **Anime Character** | Fetches random anime character images by category. | `.waf [category]` |
| 🎲 **Aurora Bull** | Creates randomized playful text sequences and timed message loops. | `.abull`, `.abullspam [time] [text]`, `.abulloff` |
| 💬 **Auto Answer** | Configures automatic replies using a selected message or post. | `.aws [ID/Username] [Post ID]` |
| 🟢 **Presence Control** | Keeps the account online or returns it to normal presence behavior. | `.online`, `.offline` |
| 👁️ **Auto Read** | Automatically marks messages as read in configured chats. | `.autoread` |
| 💬 **Bull Text** | Generates randomized dramatic text for entertainment. | `.bull`, `.bulli` |
| 🎯 **Chance Meter** | Generates a playful probability score for any question or phrase. | `.chance [text]` |
| 🛡️ **Chat Administration** | Provides chat IDs, permissions, moderation, roles, links, and group-management tools. | `.id [reply]`, `.rights [-u username/id]`, `.leave`, `.pin [reply]`, `.unpin [reply]`, `.unpinall`, `.admins`, `.ban [reply] [duration]`, `.unban [reply]`, `.kick [reply]`, `.mute [reply] [duration]`, `.unmute [reply]`, `.rename [name]`, `.create [-g|--group name] [-c|--channel name]`, `.geturl [reply]`, `.addrole -n role_name -p permission_number`, `.delrole -n role_name`, `.roles [-n role_name]`, `.chatinfo` |
| 💱 **Currency Converter** | Converts amounts between configured currencies using current exchange data. | `.cr [amount] [currency]`, `.currency_config [currencies]` |
| ⚠️ **Legacy Stress Tools** | Provides legacy stress-test commands; use only with explicit authorization. | `.bomber`, `.sbomber` |
| 🖼️ **Demotivator** | Creates a demotivational-style image from replied media and custom text. | `.dem [text]` |
| 📨 **Direct Sender** | Sends replied content to a Telegram ID or username. | `.send [ID/Username]` |
| 🔎 **Public OSINT Lookup** | Queries supported public OSINT sources for a supplied phone number. | `.eye [phone]`, `.osint [phone]` |
| 🆔 **Chat ID Finder** | Shows the current chat identifier and related Telegram IDs. | `.id` |
| 🎵 **Music Finder** | Finds lyrics and music results across supported providers. | `.genius_config [api_token]`, `.l [song_name]`, `.lyrics [song_name]`, `.dm [song_name]`, `.dmusic [song_name]`, `.lm [song_name]`, `.lmusic [song_name]` |
| 💎 **Fragment Checker** | Checks supported Telegram Fragment username information. | `.fcheck [username]` |
| ✨ **Gemini AI** | Uses the supported Google Gen AI SDK for prompts, conversations, model selection, and history control. | `.gemini [text]`, `.gemini_api [api_key]`, `.gemini_model [model]`, `.gemini_chat [text]`, `.gemini_clear` |
| 🔐 **Password Generator** | Generates a random password with the requested length. | `.gen_password [length]` |
| 🗝️ **Subscription Key Extractor** | Parses supported subscription links and extracts available connection keys. | `.get_keys [link to sub]` |
| 💗 **Heart Animation** | Displays an animated heart sequence in the current message. | `.hearts`, `.magic`, `.love` |
| 📚 **History Facts** | Returns concise English-language facts from built-in history collections. | `.rfact`, `.hfact`, `.mfact`, `.sfact` |
| 🙈 **Ignore User** | Suppresses selected incoming messages from a specified user or chat. | `.ignore [user_id/@username]` |
| 🌐 **IP Information** | Displays location, network, timezone, and provider data for an IP address. | `.ipi [ip]`, `.ipinfo [ip]` |
| 🧹 **Member Cleanup** | Performs bulk member cleanup actions in chats where you have permission. | `.kickall`, `.kickall_hide`, `.kickall_withbot`, `.kickdeleted` |
| 🪜 **Text Ladder** | Builds an animated ladder pattern from custom text. | `.ladder [text]` |
| 🎧 **Last.fm Status** | Displays and optionally auto-updates your currently playing Last.fm track. | `.lastfm_api [api_key]`, `.nowplayed`, `.lastfm_config [LastFM Nickname] [Username/ID Channel] [ID Message] [Autostart: True/False]`, `.autoplayed` |
| 🔗 **Rich Link Builder** | Creates safe clickable text using a validated HTTP or HTTPS URL and label. | `.link [url] [text]` |
| 🎞️ **Media to GIF** | Converts replied photos or videos into an optimized GIF. | `.media2gif [reply to photo or video]` |
| 🖼️ **Media Gallery** | Fetches images from several supported themed media sources. | `.anime`, `.cat`, `.lolic`, `.loli`, `.lolih`, `.fem`, `.sfw`, `.furry`, `.nsfw` |
| 🧩 **Module Bridge** | Converts compatible legacy modules into the Zelretch addon format. | `.module_bridge [Link/Reply]`, `.module_bridge_config [Model]` |
| ☁️ **Multi Uploader** | Uploads replied files to multiple temporary file-hosting services. | `.catbox`, `.envs`, `.kappa`, `.0x0`, `.x0`, `.tmpfiles`, `.pomf`, `.bash` |
| 🐾 **Neko Media** | Fetches a random neko-themed image. | `.neko` |
| 🐱 **Cat Text Mode** | Adds a configurable English cat-style transformation to outgoing text. | `.nekoed [on/off]` |
| 🧾 **Fictional Profile Generator** | Creates an English fictional profile card for entertainment and testing. | `.doxx` |
| 🎭 **Patriot Text** | Applies an English leetspeak style to replied or outgoing text. | `.patriot`, `.pat [reply]` |
| 📌 **Pinterest Downloader** | Extracts and downloads supported Pinterest images or videos. | `.pinterest [link]` |
| 💠 **Premium Text** | Transforms supported characters into premium-emoji styled text. | `.prem_text [text]` |
| 📊 **Progress Animation** | Displays an animated progress bar with optional custom text. | `.progressbar [text]` |
| 🎟️ **Promo Claimer** | Monitors supported promo messages and attempts eligible token redemptions. | `.checktokens` |
| 🗑️ **Message Cleanup** | Deletes a replied message or a selected message range. | `.del [reply]`, `.purge [reply/group_id] [start_id] [stop_id]` |
| 🔳 **QR Generator** | Generates a QR code from supplied text or a link. | `.qr [text]` |
| 💬 **Quote Maker** | Creates a quote image from a replied Telegram message. | `.q [reply]` |
| 🎲 **Random Number** | Generates a random number using configurable minimum and maximum values. | `.rnd [min] [max]`, `.randomizer_config [min] [max]` |
| ⭐ **Reputation** | Tracks simple positive and negative reputation reactions in a chat. | `.rep [number]` |
| 🔞 **Adult Media Search** | Searches an adult-content provider by tags; use only where lawful and appropriate. | `.rule34 [tags]` |
| 🕵️ **Username Search** | Checks a username or identifier across supported public services. | `.sher [query]` |
| ✂️ **URL Shortener** | Creates a shortened link from supplied or replied text. | `.short [Reply/Link]` |
| 📥 **Social Downloader** | Downloads supported social-media videos from a supplied URL. | `.tt [url]` |
| 📣 **Bulk Messaging** | Sends repeated text or sticker messages with configurable count and delay. | `.stspam [count] [delay] [sticker_id]`, `.spam [count] [delay] [text]`, `.help_spam` |
| 🛡️ **Spam Protection Check** | Checks the current account against supported Telegram spam restrictions. | `.spamban` |
| 🔊 **Text to Speech** | Converts supplied English text into an audio message. | `.voice [English text]` |
| 🚀 **Speed Test** | Measures network upload speed, latency, server location, and provider information. | Automatic/background |
| 📈 **Account Statistics** | Shows Telegram dialog, contact, group, and channel statistics. | `.stat`, `.stats` |
| 📊 **Detailed Statistics** | Provides an expanded summary of account and dialog statistics. | `.stats_xdesai` |
| 📡 **Stream Utilities** | Provides supported streaming and media-link utilities. | `.stream` |
| 🔄 **Text Switch** | Swaps uppercase and lowercase English letters in supplied or replied text. | `.sw [reply|text]` |
| 🖥️ **System Information** | Displays CPU, memory, disk, platform, and runtime information. | `.sysinfo` |
| ⚙️ **Systemd Manager** | Lists and manages systemd units on compatible Linux hosts. | `.units`, `.addunit [unit] [name]`, `.delunit [unit]`, `.unit [unit] [action]`, `.nameunit [unit] [new_name]` |
| 📢 **Mention All** | Mentions chat members sequentially or in grouped batches. | `.tagallone [delay] [text]`, `.tagall [delay] [text]` |
| ✅ **Task Manager** | Creates, lists, prioritizes, and removes personal tasks. | `.td [importance:int] [task]`, `.tdl`, `.utd [task_id]` |
| 📱 **Client Detector** | Estimates which Telegram client a user is using from public message data. | `.telega [reply/@username/id]` |
| 🕒 **Current Time** | Shows the current date and time. | `.time` |
| 🎬 **Fun Animations** | Runs a collection of harmless animated text sequences. | `.hack`, `.drugs`, `.police [duration]`, `.ghoul`, `.stupid`, `.bombs`, `.call`, `.kill`, `.ZV` |
| ⌨️ **Typing Animation** | Animates supplied text as though it is being typed. | `.type [text]` |
| 🧭 **URL Inspector** | Expands shortened URLs and displays resolved host or IP information. | `.expandurl [URL]`, `.ipurl [URL]` |
| 👤 **User Information** | Displays concise or detailed public information about a Telegram user. | `.user_info [user_id/@username]`, `.user_info_full [user_id/@username]` |
| ⏳ **Wait Animation** | Displays a short animated waiting sequence. | `.wait` |
| 🌦️ **Weather** | Shows a text forecast and weather image for a city. | `.weather [city]` |
| ⛅ **Advanced Weather** | Provides detailed weather data with optional API configuration. | `.weather [city]`, `.weather_config [api_key]`, `.weather_help` |
| 📸 **Website Screenshot** | Captures a screenshot of a supplied web page. | `.webshot [url]` |
| 📖 **Wikipedia Search** | Searches English Wikipedia and returns a concise summary. | `.wiki [query]` |

## Development rules

- User-facing text, metadata, documentation, and command help must be written in English.
- Keep secrets in environment variables or MongoDB-backed runtime configuration.
- Addons must remain independent from the main deployment repository.
- Each Addon should expose `ZELRETCH_MODULE_INFO` metadata.

## License

See `LICENSE`.


## v3.1.3 Addons directory layout

- Moved every executable Addon into the repository's `Addons/` directory.
- Moved `requirements.txt` and `zelretch_addons.json` into `Addons/`.
- Updated the main Zelretch synchronizer to ignore Python files outside this folder.

## v3.1.1 runtime fixes

- Corrected the Neko Text Mode Addon so its module filename does not depend on an undeclared `os` symbol.
- The Addons package contains English/ASCII filenames only.
- Use this repository together with Zelretch v3.1.3 or later so old non-English cached Addons are removed from MongoDB automatically.

## v3.1.3 runtime reliability

- `Addons/nekomod.py` uses `pathlib.Path` for its module filename and creates its state directory before writing.
- The module no longer depends on an implicit `os` import, eliminating the startup `NameError`.
- The package remains English-only and keeps every Addon under the `Addons/` folder.
