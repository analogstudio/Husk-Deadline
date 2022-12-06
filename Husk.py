#!/usr/bin/env python3

# import os
# from pathlib import Path

from System import *
from System.Diagnostics import *
from System.IO import *


from Deadline.Plugins import *
from Deadline.Scripting import *


def GetDeadlinePlugin():
    return Husk()

def CleanupDeadlinePlugin(deadlinePlugin):
    deadlinePlugin.Cleanup()

class Husk(DeadlinePlugin):
    def __init__(self):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument

    def Cleanup(self):
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback

    def InitializeProcess(self):
        self.SingleFramesOnly=True
        self.StdoutHandling=True
        self.PopupHandling=False

        self.AddStdoutHandlerCallback("USD ERROR(.*)").HandleCallback += self.HandleStdoutError
        self.AddStdoutHandlerCallback(r"ALF_PROGRESS ([0-9]+(?=%))").HandleCallback += self.HandleStdoutProgress

    def RenderExecutable(self):
        """get path to the executable"""
        return self.GetConfigEntry("USD_RenderExecutable")

    def RenderArgument(self):
        """
        Read the USDInput which should be a usd file sequence using ####'s
        """

        usd_file = self.GetPluginInfoEntry("USDInput")
        usd_file = RepositoryUtils.CheckPathMapping(usd_file)
        usd_file = usd_file.replace("\\", "/")
        print('{n} - usd_file: {v}'.format(n=__name__, v=usd_file))

        frame_number = self.GetStartFrame() # check this 2021 USD

        # this returns 0 but replace padding works...
        # usd_padding_length = FrameUtils.GetPaddingSizeFromFilename(usd_file)
        usd_file_frame = FrameUtils.ReplacePaddingWithFrameNumber(usd_file, frame_number)
        print('{n} - usd_file_frame: {v}'.format(n=__name__, v=usd_file_frame))


        argument = ""
        argument += usd_file_frame + " "
        argument += "--verbose ate{} ".format(self.GetPluginInfoEntryWithDefault("LogLevel", '3'))  # alfred style output and full verbosity
        argument += "--frame {} ".format(frame_number)
        argument += "--frame-count 1" + " " # only render 1 frame per task
        # argument += " --mplayer-monitor -"

        # simon doesnt want  the output specified, its already in the USD
        #renderer handled in job file.
        # outputPath = os.path.dirname(usd_file).split('/')#[:-4] We are now going to site the composite USD in the project root.
        # outputPath.append('render/3D_render')
        # outputPath = os.path.abspath(os.path.join(*outputPath))
        # filename = Path(usd_file).name
        # filename = Path(filename).with_suffix("")
        # paddedframe_number = StringUtils.ToZeroPaddedString(frame_number,4)

        # argument += "-o {0}/{1}.{2}.exr".format(outputPath,filename,paddedframe_number)
        # argument += " --make-output-path" + " "

        self.LogInfo("Rendering USD file: {}".format(usd_file))
        return argument

    def HandleStdoutProgress(self):
        # just incase we want to implement progress at some point
        # sr thinks this is working fine with verbose on!
        self.SetStatusMessage(self.GetRegexMatch(0))
        self.SetProgress(float(self.GetRegexMatch(1)))

    def HandleStdoutError(self):
        self.FailRender(self.GetRegexMatch(0))
