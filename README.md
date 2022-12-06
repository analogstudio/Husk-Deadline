# Husk Deadline Plugin

🎈 Originally forked from [David Tree's HuskStandaloneSubmitter](https://github.com/DavidTree/HuskStandaloneSubmitter) but this is focused on the plugin (we have a USD ROP submitter entrenched in our Houdini pipeline so difficult to share now)

# Installation
This repo is designed to be cloned straight into `DeadlineRepository10\custom\plugins` as 'Husk' ie.:

```bash
cd //path/to/DeadlineRepository10/custom/plugins
$ git clone git@github.com:analogstudio/Husk-Deadline.git ./Husk
```

## Monitor submission
Analog does not actively use this but the submitter so have not included it!


## Features:
  - Sequence Renders
  - Render Increments

## Setting Husk.exe Location
To set the location of Husk.exe, in Deadline Monitor goto Tools > Configure Plugin > Husk and set the Husk Path. This should be your Houdini installation directory\bin\husk.exe

## Versions Tested:
  - Deadline 10.1.23.6
  - Houdini 19.0+




