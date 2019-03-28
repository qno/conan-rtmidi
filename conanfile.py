from conans import ConanFile, CMake, tools
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
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    _rtmidi_pkg_name = "rtmidi"
    _rtmidi_libname = "rtmidi"

    scm = {
         "type": "git",
         "subfolder": _rtmidi_libname,
         "url": "https://github.com/thestk/rtmidi",
         "revision": "master"
      }

    def build_requirements(self):
        if platform.system() == "Linux":
            dep_pkg = "libalsa/1.1.5@conan/stable"
            dep_remote = "https://api.bintray.com/conan/conan-community/conan"
            self.output.warn("Download dependency from remote '{}'".format(dep_remote))
            self.output.warn("If it is not in conan remotes add it with 'conan remote add conan-community {}'".format(dep_remote))
            self.build_requires("{}".format(dep_pkg))

    def source(self):
        tools.replace_in_file("{}/CMakeLists.txt".format(self._rtmidi_pkg_name), "project(RtMidi LANGUAGES CXX)",
                              '''project(RtMidi LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self._rtmidi_pkg_name)
        cmake.build()

    def package(self):
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self._rtmidi_libname]
