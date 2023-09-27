#! /usr/bin/env python

# This is an example showing how we trabnscribe a Resolve timeline using the API.

# Make a resolve instance. If running this script internally from the Resolve
# dropdown menu, i.e. in free Resolve you can disable these two lines.
from DaVinciResolveScriptModified import get_resolve
resolve = get_resolve()


# Make some additional Resolve instances we need
projectManager  = resolve.GetProjectManager()
currentProject  = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()


# Transcribe the current timeline into subtitles.
if not currentTimeline.CreateSubtitlesFromAudio():
    print('Could not transcribe the timeline.')
    exit()
