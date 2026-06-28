# Must load Pyhthon module, defult=C++
load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "constants_lib",
    srcs = ["constants.py"],
)

py_test(
    name = "calculator_basic_test",
    srcs = ["test_calculator_basic_arithmetic.py"],
    main = "test_calculator_basic_arithmetic.py",
    imports = ["../.."],
    data = [
        "//:automation_mobly/ci_config.yaml",
    ],
    deps = [
        ":constants_lib",
        "//automation_mobly/common:common_lib",
        "//automation_mobly/data_models:data_models_lib",
        "//automation_mobly/libs:libs_lib",
        "@pip_deps//mobly",
    ],
)

py_test(
    name = "builtin_app_exists_and_force_stop",
    srcs = ["test_builtin_app_exists_and_force_stop.py"],
    main = "test_builtin_app_exists_and_force_stop.py",
    imports = ["../.."],
    data = [
        "//:automation_mobly/ci_config.yaml",
    ],
    deps = [
        ":constants_lib",
        "//automation_mobly/common:common_lib",
        "//automation_mobly/data_models:data_models_lib",
        "//automation_mobly/libs:libs_lib",
        "@pip_deps//mobly",
    ],
)

py_test(
    name = "test_fake_app_not_installed",
    srcs = ["test_fake_app_not_installed.py"],
    main = "test_fake_app_not_installed.py",
    imports = ["../.."],
    data = [
        "//:automation_mobly/ci_config.yaml",
    ],
    deps = [
        ":constants_lib",
        "//automation_mobly/common:common_lib",
        "//automation_mobly/data_models:data_models_lib",
        "//automation_mobly/libs:libs_lib",
        "@pip_deps//mobly",
    ],
)

py_test(
    name = "test_system_interruption_and_locale_change",
    srcs = ["test_system_interruption_and_locale_change.py"],
    main = "test_system_interruption_and_locale_change.py",
    imports = ["../.."],
    data = [
        "//:automation_mobly/ci_config.yaml",
    ],
    deps = [
        ":constants_lib",
        "//automation_mobly/common:common_lib",
        "//automation_mobly/data_models:data_models_lib",
        "//automation_mobly/libs:libs_lib",
        "@pip_deps//mobly",
    ],
)