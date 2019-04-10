from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import platform

class RtMidiConan(ConanFile):
    name = "RtMidi"
    version = "master"
    license = "MIT"
    author = "Gary P. Scavone"
    url = "https://github.com/qno/conan-rtmidi"
    description = "A set of C++ classes that provide a common API for realtime MIDI input/output across Linux (ALSA & JACK), Macintosh OS X (CoreMIDI & JACK) and Windows (Multimedia)."

    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    options = {"shared": [True, False]}
    default_options = "shared=False"

    _rtmidi_pkg_name = "rtmidi"
    _rtmidi_libname = "rtmidi"

    scm = {
         "type": "git",
         "subfolder": _rtmidi_libname,
         "url": "https://github.com/thestk/rtmidi",
         "revision": "master"
      }

    def build(self):
        if self._isVisualStudioBuild():
            cmake = CMake(self)
            cmake.definitions["RTMIDI_BUILD_TESTING"] = "False"
            cmake.configure(source_dir=self._rtmidi_pkg_name)
            cmake.build()
        else:
            self.run("cd {} && sh autogen.sh --no-configure && cd ..".format(self._rtmidi_pkg_name))
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(configure_dir=self._rtmidi_pkg_name)
            autotools.make()
            autotools.install()

    def package(self):
        self.copy("RtMidi.h", dst="include", src=self._rtmidi_pkg_name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        release_libs = [self._rtmidi_libname]
        debug_libs = [self._rtmidi_libname]

        if self._isVisualStudioBuild():
            release_libs.append("{}_static".format(self._rtmidi_libname))
            debug_libs = ["{}d".format(self._rtmidi_libname), "{}_staticd".format(self._rtmidi_libname)]

        self.cpp_info.release.libs = release_libs
        self.cpp_info.debug.libs = debug_libs

    def _isVisualStudioBuild(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"
