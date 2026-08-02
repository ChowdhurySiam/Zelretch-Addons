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
| 💬 **Auto Answer** | Configures automatic replies using a selected message or post. | `.aws [ID/Username] [Post ID]` |
| 💬 **Bull Text** | Generates randomized dramatic text for entertainment. | `.bull`, `.bulli` |
| 🎯 **Chance Meter** | Generates a playful probability score for any question or phrase. | `.chance [text]` |
| 🛡️ **Chat Administration** | Provides chat IDs, permissions, moderation, roles, links, and group-management tools. | `.id [reply]`, `.rights [-u username/id]`, `.leave`, `.pin [reply]`, `.unpin [reply]`, `.unpinall`, `.admins`, `.ban [reply] [duration]`, `.unban [reply]`, `.kick [reply]`, `.mute [reply] [duration]`, `.unmute [reply]`, `.rename [name]`, `.create [-g|--group name] [-c|--channel name]`, `.geturl [reply]`, `.addrole -n role_name -p permission_number`, `.delrole -n role_name`, `.roles [-n role_name]`, `.chatinfo` |
| 📨 **Direct Sender** | Sends replied content to a Telegram ID or username. | `.send [ID/Username]` |
| 🔎 **Public OSINT Lookup** | Queries supported public OSINT sources for a supplied phone number. | `.eye [phone]`, `.osint [phone]` |
| 🆔 **Chat ID Finder** | Shows the current chat identifier and related Telegram IDs. | `.id` |
| 🎵 **Music Finder** | Finds lyrics and music results across supported providers. | `.genius_config [api_token]`, `.l [song_name]`, `.lyrics [song_name]`, `.dm [song_name]`, `.dmusic [song_name]`, `.lm [song_name]`, `.lmusic [song_name]` |
| 💎 **Fragment Checker** | Checks supported Telegram Fragment username information. | `.fcheck [username]` |
| ✨ **Gemini AI** | Uses the supported Google Gen AI SDK for prompts, conversations, model selection, and history control. | `.gemini [text]`, `.gemini_api [api_key]`, `.gemini_model [model]`, `.gemini_chat [text]`, `.gemini_clear` |
| 🔐 **Password Generator** | Generates a random password with the requested length. | `.gen_password [length]` |
| 💗 **Heart Animation** | Displays an animated heart sequence in the current message. | `.hearts`, `.magic`, `.love` |
| 🙈 **Ignore User** | Suppresses selected incoming messages from a specified user or chat. | `.ignore [user_id/@username]` |
| 🌐 **IP Information** | Displays location, network, timezone, and provider data for an IP address. | `.ipi [ip]`, `.ipinfo [ip]` |
| 🧹 **Member Cleanup** | Performs bulk member cleanup only after the requester types the exact text `CONFIRM` in the same chat within 60 seconds. | `.kickall`, `.kickall_hide`, `.kickall_withbot`, `.kickdeleted`, then `CONFIRM` |
| 🪜 **Text Ladder** | Builds an animated ladder pattern from custom text. | `.ladder [text]` |
| 🔗 **Rich Link Builder** | Creates safe clickable text using a validated HTTP or HTTPS URL and label. | `.link [url] [text]` |
| 🎞️ **Media to GIF** | Converts replied photos or videos into an optimized GIF. | `.media2gif [reply to photo or video]` |
| 🖼️ **Media Gallery** | Fetches images from several supported themed media sources. | `.anime`, `.cat`, `.lolic`, `.loli`, `.lolih`, `.fem`, `.sfw`, `.furry`, `.nsfw` |
| 🧩 **Module Bridge** | Converts compatible legacy modules into the Zelretch addon format. | `.module_bridge [Link/Reply]`, `.module_bridge_config [Model]` |
| ☁️ **Multi Uploader** | Uploads replied files to multiple temporary file-hosting services. | `.catbox`, `.envs`, `.kappa`, `.0x0`, `.x0`, `.tmpfiles`, `.pomf`, `.bash` |
| 🐾 **Neko Media** | Fetches a random neko-themed image. | `.neko` |
| 🐱 **Cat Text Mode** | Adds a configurable English cat-style transformation to outgoing text. | `.nekoed [on/off]` |
| 🧾 **Fictional Profile Generator** | Creates an English fictional profile card for entertainment and testing. | `.doxx` |
| 📌 **Pinterest Downloader** | Extracts and downloads supported Pinterest images or videos. | `.pinterest [link]` |
| 💠 **Premium Text** | Transforms supported characters into premium-emoji styled text. | `.prem_text [text]` |
| 📊 **Progress Animation** | Displays an animated progress bar with optional custom text. | `.progressbar [text]` |
| 🗑️ **Message Cleanup** | Deletes a replied message or a selected message range. | `.del [reply]`, `.purge [reply/group_id] [start_id] [stop_id]` |
| 💬 **Quote Maker** | Creates a quote image from a replied Telegram message. | `.q [reply]` |
| 🔞 **Adult Media Search** | Searches an adult-content provider by tags; use only where lawful and appropriate. | `.rule34 [tags]` |
| 🕵️ **Username Search** | Checks a username or identifier across supported public services. | `.sher [query]` |
| 📥 **Social Downloader** | Downloads public videos and audio from websites supported by yt-dlp. | `.socialdl [url/reply]`, `.sdl [url/reply]`, `.tt [url/reply]` |
| 📣 **Bulk Messaging** | Sends repeated text or sticker messages with configurable count and delay. | `.stspam [count] [delay] [sticker_id]`, `.spam [count] [delay] [text]`, `.help_spam` |
| 🛡️ **Spam Protection Check** | Checks the current account against supported Telegram spam restrictions. | `.spamban` |
| 🔊 **Text to Speech** | Converts supplied or replied English text into a Telegram-compatible voice note. | `.voice [English text/reply]`, `.tts [English text/reply]` |
| 🚀 **Speed Test** | Measures latency, download speed, upload speed, provider, and location with partial-result fallback. | `.speedtest`, `.speedconfig` |
| 📈 **Account Statistics** | Shows Telegram dialog, contact, group, and channel statistics. | `.stat`, `.stats` |
| 📊 **Detailed Statistics** | Provides an expanded summary of account and dialog statistics. | `.stats_xdesai` |
| 📡 **Stream Utilities** | Provides supported streaming and media-link utilities. | `.stream` |
| 🔄 **Text Switch** | Swaps uppercase and lowercase English letters in supplied or replied text. | `.sw [reply|text]` |
| 🖥️ **System Information** | Displays container-aware CPU, memory, disk, platform, process, and runtime information. | `.sysinfo` |
| ⚙️ **Systemd Manager** | Manages systemd units on supported Linux hosts and explains Docker/Hugging Face incompatibility clearly. | `.systemdcheck`, `.units`, `.addunit [unit] [name]`, `.delunit [unit]`, `.unit [unit] [action]`, `.nameunit [unit] [new_name]` |
| 📢 **Mention All** | Mentions chat members sequentially or in grouped batches. | `.tagallone [delay] [text]`, `.tagall [delay] [text]` |
| ✅ **Task Manager** | Creates, lists, prioritizes, and removes personal tasks. | `.td [importance:int] [task]`, `.tdl`, `.utd [task_id]` |
| 📱 **Client Detector** | Estimates which Telegram client a user is using from public message data. | `.telega [reply/@username/id]` |
| 🎬 **Fun Animations** | Runs a collection of harmless animated text sequences. | `.hack`, `.drugs`, `.police [duration]`, `.ghoul`, `.stupid`, `.bombs`, `.call`, `.kill`, `.ZV` |
| ⌨️ **Typing Animation** | Animates supplied text as though it is being typed. | `.type [text]` |
| 👤 **User Information** | Displays concise or detailed public information about a Telegram user. | `.user_info [user_id/@username]`, `.user_info_full [user_id/@username]` |
| ⏳ **Wait Animation** | Displays a short animated waiting sequence. | `.wait` |
| 🌦️ **Weather** | Shows a text forecast and weather image for a city. | `.weather [city]` |

## Development rules

- User-facing text, metadata, documentation, and command help must be written in English.
- Keep secrets in environment variables or MongoDB-backed runtime configuration.
- Addons must remain independent from the main deployment repository.
- Each Addon should expose `ZELRETCH_MODULE_INFO` metadata.

## License

See `LICENSE`.


## v3.3.0 Addons directory layout

- Moved every executable Addon into the repository's `Addons/` directory.
- Moved `requirements.txt` and `zelretch_addons.json` into `Addons/`.
- Updated the main Zelretch synchronizer to ignore Python files outside this folder.

## v3.1.1 runtime fixes

- Corrected the Neko Text Mode Addon so its module filename does not depend on an undeclared `os` symbol.
- The Addons package contains English/ASCII filenames only.
- Use this repository together with Zelretch v3.3.0 or later so old non-English cached Addons are removed from MongoDB automatically.

## v3.3.0 runtime reliability

- `Addons/nekomod.py` uses `pathlib.Path` for its module filename and creates its state directory before writing.
- The module no longer depends on an implicit `os` import, eliminating the startup `NameError`.
- The package remains English-only and keeps every Addon under the `Addons/` folder.


## v3.3.0 reliability fixes

- Fixed the Pinterest downloader for Python 3.11 and added safer URL/media handling.
- Confirmed the Neko Text Mode Addon uses `pathlib` and does not depend on an undeclared `os` import.


## Fast synchronization manifest

`Addons/zelretch_addons.json` now contains a stable `release_id` and a SHA-256 digest for every Addon. Zelretch checks this small manifest first and skips the repository archive download when the managed Addon set is unchanged.

## Undo support

Every Addon now exposes an undo path. Use the semantic inverse command shown in the command center for persistent or stateful features. For output-only Addons, reply to the generated message with:

```text
.undo
```

You may also use `.undo <message_id>` or `.undo last`. Irreversible Telegram-side actions—such as deleting messages, removing members, sending repeated messages, or redeeming a promotion—cannot be restored; `.undo` only removes the selected status/output message in those cases.

## v3.3.1 Addon retirement update

- Member Cleanup no longer starts immediately. Each cleanup command creates a pending request and requires the exact text `CONFIRM` in the same chat within 60 seconds.
- Removed the Demotivator, URL Shortener, and URL Inspector Addons.
- Cleanup progress and completion counts are reported without implying that removed members can be restored.

## v3.3.2 Addon retirement update

The following Addons were removed from the managed repository: Subscription Key Extractor, QR Generator, Current Time, Random Number, Presence Control, Reputation, Promo Claimer, Auto Read, Patriot Text, Website Screenshot, and Aurora Bull. Zelretch removes stale cached copies automatically.
## v3.3.3 Addon retirement update

Removed Last.fm Status, Wikipedia Search, History Facts, Currency Converter, and Advanced Weather. The standard Weather Addon remains available. The managed repository now contains 56 Addons.

## v3.3.4 Addon retirement update

Removed Legacy Stress Tools (`db0mb3r.py`) and its `db0mb3r` dependency. The managed repository now contains 55 Addons.

## v3.3.5 system Addon reliability

- Rebuilt Speed Test with latency, download, and upload measurements plus partial-result fallback.
- Rebuilt System Information with cgroup-aware memory and CPU quotas for Docker and Hugging Face Spaces.
- Rebuilt Systemd Manager with safe subprocess timeouts, status/log actions, and explicit compatibility diagnostics when systemd is unavailable.

## v3.3.6 media Addon reliability

- Rebuilt Social Downloader around `yt-dlp` with public URL extraction, progress updates, bounded timeouts, file-size limits, metadata captions, and video/audio/document upload fallback.
- Added `.socialdl` and `.sdl` while retaining `.tt` for compatibility.
- Rebuilt Text to Speech so the network request runs outside the event loop and generated MP3 audio is converted to Telegram-compatible OGG/Opus when FFmpeg is available.
- Added `.tts` as an alias and support for replied text.
- Dependency installation is lazy when these commands are unused; the current main project preinstalls the required packages during the Docker build.
