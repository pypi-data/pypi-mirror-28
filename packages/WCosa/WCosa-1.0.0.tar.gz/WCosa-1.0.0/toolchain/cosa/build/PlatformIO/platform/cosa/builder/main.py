# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Builder for Atmel AVR series of microcontrollers
"""

from os.path import join
from time import sleep

from SCons.Script import (ARGUMENTS, COMMAND_LINE_TARGETS, AlwaysBuild,
                          Builder, Default, DefaultEnvironment)

from platformio.util import get_serialports


def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621

    if "program" in COMMAND_LINE_TARGETS:
        return

    if "micronucleus" in env['UPLOADER']:
        print "Please unplug/plug device ..."

    upload_options = {}
    if "BOARD" in env:
        upload_options = env.BoardConfig().get("upload", {})

    # Deprecated: compatibility with old projects. Use `program` instead
    if "usb" in env.subst("$UPLOAD_PROTOCOL"):
        upload_options['require_upload_port'] = False
        env.Replace(UPLOAD_SPEED=None)

    if env.subst("$UPLOAD_SPEED"):
        env.Append(UPLOADERFLAGS=["-b", "$UPLOAD_SPEED"])

    if upload_options and not upload_options.get("require_upload_port", False):
        return

    env.AutodetectUploadPort()
    env.Append(UPLOADERFLAGS=["-P", '"$UPLOAD_PORT"'])

    if env.subst("$BOARD") in ("raspduino", "emonpi"):

        def _rpi_sysgpio(path, value):
            with open(path, "w") as f:
                f.write(str(value))

        pin_num = 18 if env.subst("$BOARD") == "raspduino" else 4
        _rpi_sysgpio("/sys/class/gpio/export", pin_num)
        _rpi_sysgpio("/sys/class/gpio/gpio%d/direction" % pin_num, "out")
        _rpi_sysgpio("/sys/class/gpio/gpio%d/value" % pin_num, 1)
        sleep(0.1)
        _rpi_sysgpio("/sys/class/gpio/gpio%d/value" % pin_num, 0)
        _rpi_sysgpio("/sys/class/gpio/unexport", pin_num)
    else:
        if not upload_options.get("disable_flushing", False):
            env.FlushSerialBuffer("$UPLOAD_PORT")

        before_ports = get_serialports()

        if upload_options.get("use_1200bps_touch", False):
            env.TouchSerialPort("$UPLOAD_PORT", 1200)

        if upload_options.get("wait_for_upload_port", False):
            env.Replace(UPLOAD_PORT=env.WaitForNewSerialPort(before_ports))


env = DefaultEnvironment()

env.Replace(
    AR="avr-ar",
    AS="avr-as",
    CC="avr-gcc",
    CXX="avr-g++",
    OBJCOPY="avr-objcopy",
    RANLIB="avr-ranlib",
    SIZETOOL="avr-size",

    ARFLAGS=["rcs"],

    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=[
        "-std=gnu11"
    ],

    CCFLAGS=[
        "-g",  # include debugging info (so errors include line numbers)
        "-Os",  # optimize for size
        "-Wall",  # show warnings
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mmcu=$BOARD_MCU"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-threadsafe-statics",
        "-std=gnu++11"
    ],

    CPPDEFINES=["F_CPU=$BOARD_F_CPU"],

    LINKFLAGS=[
        "-Os",
        "-mmcu=$BOARD_MCU",
        "-Wl,--gc-sections,--relax"
    ],

    LIBS=["m"],

    SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',

    PROGNAME="firmware",
    PROGSUFFIX=".elf"
)

env.Append(
    ASFLAGS=env.get("CCFLAGS", [])[:],

    BUILDERS=dict(
        ElfToEep=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-j",
                ".eeprom",
                '--set-section-flags=.eeprom="alloc,load"',
                "--no-change-warnings",
                "--change-section-lma",
                ".eeprom=0",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".eep"
        ),

        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)

if "BOARD" in env and "digispark" in env.BoardConfig().get("build.core", ""):
    env.Replace(
        UPLOADER="micronucleus",
        UPLOADERFLAGS=[
            "-c", "$UPLOAD_PROTOCOL",
            "--timeout", "60"
        ],
        UPLOADHEXCMD='$UPLOADER $UPLOADERFLAGS $SOURCES'
    )

else:
    env.Replace(
        UPLOADER="avrdude",
        UPLOADERFLAGS=[
            "-p", "$BOARD_MCU",
            "-C",
            join(env.PioPlatform().get_package_dir("tool-avrdude") or "",
                 "avrdude.conf"),
            "-c", "$UPLOAD_PROTOCOL"
        ],
        UPLOADHEXCMD='$UPLOADER $UPLOADERFLAGS -D -U flash:w:$SOURCES:i',
        UPLOADEEPCMD='$UPLOADER $UPLOADERFLAGS -U eeprom:w:$SOURCES:i',
        PROGRAMHEXCMD='$UPLOADER $UPLOADERFLAGS -U flash:w:$SOURCES:i'
    )
    if int(ARGUMENTS.get("PIOVERBOSE", 0)):
        env.Prepend(UPLOADERFLAGS=["-v"])

#
# Target: Build executable and linkable firmware
#

target_elf = env.BuildProgram()

#
# Target: Build the .hex file
#

if "uploadlazy" in COMMAND_LINE_TARGETS:
    target_firm = join("$BUILD_DIR", "firmware.hex")
else:
    target_firm = env.ElfToHex(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload by default .hex file
#

upload = env.Alias(
    ["upload", "uploadlazy"], target_firm,
    [env.VerboseAction(BeforeUpload, "Looking for upload port..."),
     env.VerboseAction("$UPLOADHEXCMD", "Uploading $SOURCE")])
AlwaysBuild(upload)

#
# Target: Upload EEPROM data (from EEMEM directive)
#

uploadeep = env.Alias(
    "uploadeep", env.ElfToEep(join("$BUILD_DIR", "firmware"), target_elf),
    [env.VerboseAction(BeforeUpload, "Looking for upload port..."),
     env.VerboseAction("$UPLOADEEPCMD", "Uploading $SOURCE")])
AlwaysBuild(uploadeep)

#
# Target: Upload firmware using external programmer
#

program = env.Alias(
    "program", target_firm,
    [env.VerboseAction(BeforeUpload, "Looking for upload port..."),
     env.VerboseAction("$PROGRAMHEXCMD", "Programming $SOURCE")])

AlwaysBuild(program)


#
# Setup default targets
#

Default([target_firm, target_size])
