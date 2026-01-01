import os
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

# Upload LittleFS after build
def after_build(source, target, env):
    print("Uploading LittleFS filesystem...")
    env.Execute("platformio run --target uploadfs")

env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", after_build)