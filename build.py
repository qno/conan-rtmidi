from bincrafters import build_template_default
import os

# see https://github.com/bincrafters/bincrafters-package-tools/blob/master/README.md
# see https://github.com/conan-io/conan-package-tools/blob/develop/README.md
os.environ["BINTRAY_REPOSITORY"]            = "conan-public"
os.environ["CONAN_UPLOAD"]                  = "https://api.bintray.com/conan/qno/conan-public"
os.environ["CONAN_USERNAME"]                = "qno"
os.environ["CONAN_PASSWORD"]                = os.environ["BINTRAY_API_KEY"] # set by azure job
os.environ["CONAN_LOGIN_USERNAME"]          = os.environ["BINTRAY_LOGIN"]   # set by azure job
os.environ["CONAN_STABLE_BRANCH_PATTERN"]   = "stable/*"
os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = "0"
os.environ["CONAN_DOCKER_32_IMAGES"]        = "1"
os.environ["CONAN_CHANNEL"]                 = "testing"


if __name__ == "__main__":
  builder = build_template_default.get_builder(pure_c=False)
  builder.run()
