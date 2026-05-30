# Must load Pyhthon module, defult=C++
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "libs_lib",
    srcs = glob(["*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        "//automation_mobly/common:common_lib",
        "@pip_deps//mobly",
    ],
)