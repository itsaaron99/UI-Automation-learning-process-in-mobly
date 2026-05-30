# Must load Pyhthon module, defult=C++
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "common_lib",
    srcs = ["base_test.py"],
    visibility = ["//visibility:public"],
    deps = [
        "@pip_deps//mobly",
    ],
)