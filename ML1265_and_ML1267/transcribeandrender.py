#! /usr/bin/env python

import os

# This is an example showing how we trabnscribe and render SRT out of Resolve using the API.
# Igor Ridanovic www.metafide.com


# Make a resolve instance. If running this script internally from the Resolve
# dropdown menu, i.e. in free Resolve you can disable these two lines.
from DaVinciResolveScriptModified import get_resolve
resolve = get_resolve()


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


# Load and print the SRT file we just generated.
srtFile = os.path.join(TEMPDIR, TEMPSRT)
with open(srtFile, 'r') as f:
    srtString = f.read()

print(srtString)
