# extra_script.py
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

# This function will run AFTER firmware build
def after_build(source, target, env):
    print(">>> Uploading LittleFS filesystem...")
    env.Execute("pio run --target uploadfs")

# Add post-action to firmware binary
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", after_build)