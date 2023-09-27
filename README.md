# MixingLight
Accompanying code for Mixing Light(https://mixinglight.com) tutorials.

## Mixing Light Insights 1265 and 1267

**openairequest.py**
Send a prompt request to OpenAI API. It only uses HTTP requests and does not require any third party modules or libraries like OpenAI Python API, LangChain, etc.

**DaVinciResolveScriptModified.py**
Used to load the BlackMagic DaVinci Resolve API library on Linux, macOS, Windows. This is slightly modified script that normally ships with DaVinci Resolve. It is reqjuired for external scripting in Resolve Studio.

**transcribe.py**
Triggers VTT transcription into subtitles of current DaVinci Resolve timeline.

**transcribeandrender.py**
Same as previous script plus it saves an SRT subtitle file from Resolve. SRT export is not directly possible via the Resolve API. We can only save one as a sidecar to a video render. This script saves a token MOV file with the SRT and then deletes the MOV file. It requires user to prebuild a Deliver page render preset with SRT option enabled.

**summarizetimeline.py**
This script combines openairequest and transcrcribeandrender into a single script which transcodes a Resolve timeline and then sends the transcript to OpenAI API to finally receive and save a YouTube video summary and save it as a TXT file.
