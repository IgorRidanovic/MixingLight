#! /usr/bin/env python

import os
import requests

# This script renders an SRT file in DaVinci Resolve and uploads it to OpenAI where it's
# it's summarized into a YouTube video summary.
# For this to work we have to first create a Resolve render preset with
# 'SRT Without Formatting' enabled ny hand.
# This script is a companion to a Mixing Light training presentation.
# Igor Ridanovic www.metafide.com


# Make a resolve instance. If running this script internally from the Resolve
# dropdown menu, i.e. in free Resolve you can disable these two lines.
from DaVinciResolveScriptModified import get_resolve
resolve = get_resolve()

# Place your OpenAI API key here
openai_key = yourKeyHere

# This is where we're going to load and save our files. Modify for your needs.
TEMPDIR = 'D:\\temp'
# You generally don't need to change this.
TEMPMOV = 'DeleteMe.mov'
# This name is automatically set by Resolve based on the subtitle track index.
TEMPSRT = 'Subtitle 1.srt'
# The custom render preset name. You can name your preset anything in Resolve.
PRESETNAME = 'subgen1'


# Make some additional Resolve instances we need
projectManager  = resolve.GetProjectManager()
currentProject  = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()


# Setup some basic OpenAI API parameters.
# endpoint    = 'https://api.openai.com/v1/chat/completions' # The API endpoint
# temperature = 0.6                                          # Resonse determinism. 0.0-deterministic, 2.0-random
# model       = 'gpt-3.5-turbo'                              # AI model
# price       = 0.0015                                       # USD price per 1,000 tokens for this model

# Some other model options. The pricing is not fully accurate. Biased to show more cost.
model       = 'gpt-3.5-turbo-16k'                           # Use for longer text, more expensive
price       = 0.003
# model       = 'gpt-4'                                    # Best quality responses, moat expensive
# price       = 0.06


# Here we create a Resolve subtitles file (SRT)
def transcribe():

    # Transcribe the current timeline into subtitles.
    if not currentTimeline.CreateSubtitlesFromAudio():
        print('Could not transcribe the timeline.')
        exit()


    # Load custom render preset, make a render job and start rendering.
    currentProject.LoadRenderPreset(PRESETNAME)
    currentProject.SetRenderSettings({'SelectAllFrames': True, 'TargetDir': TEMPDIR, 'CustomName': TEMPMOV})
    renderJobId = currentProject.AddRenderJob()
    currentProject.StartRendering(renderJobId)

    # StartRendering() is not blocking. We have to hold the execution until the render is finished
    while currentProject.IsRenderingInProgress():
        pass

    # Delete the temp MOV file.
    tempFile = os.path.join(TEMPDIR, TEMPMOV)
    os.remove(tempFile)



# Here we upload the SRT to OpenAI and receive a YouTube summary
def summarize():

    # Load the SRT file we just generated in Resolve.
    srtFile = os.path.join(TEMPDIR, TEMPSRT)
    with open(srtFile, 'r') as f:
        subtitles = f.read()


    # Structure the message.
    prompt  = """
            Write an inviting and compelling YouTube summary based on the SRT delineated by the tripple equal signs.
            1. Structure the summary in three short paragraphs
            2. Each paragraph must be two sentences long
            3. Write in first person plural
            4. The first paragraph must speak directly to potential viewers and use a language that will entice them
            """ + '===' + subtitles + '==='

    aiRole = """
            You're a YouTube content creator who is very skilled in writing short and compelling
            video summaries based on the video dialog structured as SRT subtitles.
            """


    message =   [
                    {'role': 'system', 'content': aiRole},
                    {'role': 'user',   'content': prompt}
                ]


    # Make a HTTP POST request to OpenAI API.
    headers  = {'Authorization': f'Bearer {openai_key}'}
    data     = {'model': model, 'temperature': temperature, 'messages': message}
    response = requests.post(endpoint, headers=headers, json=data).json()


    # Parse the information of interest from the OpenAI response.
    answer = response['choices'][0]['message']['content']
    tokens = response['usage']['total_tokens']


    # Get cost in USD for this API call.
    cost = tokens / 1000 * price
    # Cost can be very small. Suppress the scientific notation.
    cost = f'{cost:.6f}'


    # Print the results to the screen.
    print(answer)
    print('-'*64)
    print('The cost in USD is', cost)


    # Save the response.
    fileName = currentTimeline.GetName() + '_' + 'LAS_Subs' + '.srt'
    savePath = os.path.join(TEMPDIR, fileName)
    with open(savePath, 'wb') as f:
        f.write(answer.encode('utf8'))



def run():
    transcribe()
    summarize()


if __name__ == '__main__':
    run()
