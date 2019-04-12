from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import re, os

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

    def source(self):
        # the conan_basic_setup() must be called, otherwise the compiler runtime will not setup correct which
        # leads then to linker errors if recipe e.g. is build with /MT runtime for MS compiler
        # see https://github.com/conan-io/conan/issues/3312
        self._patchCMakeListsFile(self._rtmidi_libname)

    def build(self):
        if self._isVisualStudioBuild():
            cmake = CMake(self)
            cmake.definitions["RTMIDI_BUILD_TESTING"] = False
            if self.options.shared:
                cmake.definitions["RTMIDI_BUILD_STATIC_LIBS"] = False
            else:
                cmake.definitions["RTMIDI_BUILD_SHARED_LIBS"] = False

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
            if not self.options.shared:
                release_libs = ["{}_static".format(self._rtmidi_libname)]
                debug_libs = ["{}_staticd".format(self._rtmidi_libname)]
                self.cpp_info.libs = ["winmm"]
            else:
                debug_libs = ["{}d".format(self._rtmidi_libname)]

        self.cpp_info.release.libs = release_libs
        self.cpp_info.debug.libs = debug_libs


    def _isVisualStudioBuild(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"

    def _patchCMakeListsFile(self, src_dir):
        cmake_project_line = ""
        cmake_file = "{}{}CMakeLists.txt".format(src_dir, os.sep)
        for line in open(cmake_file, "r", encoding="utf8"):
            if re.match("^PROJECT.*\\(.*\\).*", line.strip().upper()):
                cmake_project_line = line
                break
        self.output.warn("patch '{}' to inject conanbuildinfo".format(cmake_file))
        tools.replace_in_file(cmake_file, "{}".format(cmake_project_line),
                              '''{}
include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)
conan_basic_setup()'''.format(cmake_project_line))
