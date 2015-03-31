# coursebuilder-hello-world-module

This is an example [Course Builder] module that shows you how to create, run,
and test extensions to the system. It is not an official Google product.

We strongly recommend making customizations by creating a module, avoiding
changes to the core Course Builder codebase where possible. This not only makes
you less likely to accidentally break something with your changes, but you'll
also find it much easier to upgrade to new versions of Course Builder as they're
released.

## Requirements

You'll need a system with current versions of `bash` and `git`, as well as
`python` 2.7.

## Getting started

First, clone Course Builder and change directory to the Course Builder root:

```sh
git clone https://code.google.com/p/course-builder
cd course-builder/coursebuilder
```

Course Builder provides a management script for fetching modules, so you always
start by grabbing Course Builder, then using it to fetch the module you want to
work with. Let's grab this module, called `hello`, next:

```sh
sh scripts/modules.sh \
  --targets=hello@https://github.com/google/coursebuilder-hello-world-module
```

This will both download the module and link it to Course Builder. Now you can
start up Course Builder with this module installed:

```sh
sh scripts/start_in_shell.sh
```

To view the module in action, visit `localhost:8081/global`.

## Module contents

The structure of this module is

```sh
module.yaml            # Module definition file.
scripts/
  setup.sh             # Module configuration script.
src/                   # Module source files.
  templates/           # HTML templates.
  hello.py             # Module handler definitions.
tests/                 # Module tests.
  functional_tests.py  # Example test file.
```

Let's talk about each of them.

### `module.yaml`

This file defines your module. This is best explained by example. Here's the
`module.yaml` for this module, annotated:

```yaml
# The dotted name of the module used for imports within CB.
module_name: modules.hello.hello
# The public URI where this module may be found.
module_uri: https://github.com/google/coursebuilder-hello-world-module
# The module's version.
module_version: 1.0.0
# The version of CB this module works with. This is pinned
# to a specific revsion. Format: <cb_version>-<git_revision_number>
container_version: 1.7.0-ac4aa3131228
# Natural language description of the module.
description: Example of Course Builder modules
# License your make your module available under.
license: Apache 2.0
# List of tests in the module; see tests/ below.
tests:
  tests.ext.hello.functional_tests.GlobalHandlerTest: 2
  tests.ext.hello.functional_tests.NamespacedHandlerTest: 2
```

### `scripts/setup.sh`

When you run `modules.sh` from Course Builder, it fetches the module you want
and then invokes this script. This script is responsible for linking module
`src` and `tests` directories into the right places in your local Course Builder
filesystem (`coursebuilder/modules/<your_module>` and
`coursebuilder/tests/ext/<your_module>`, respectively). These locations must
match the dotted patterns found in your `module.yaml` or you will have problems
importing your module at runtime.

In most cases you will not need to modify this file, and can just copy it
directly into a new module. If you are creating a new module and cannot use
`modules.sh` because your files are not yet found in a version control system,
you can run this script directly to install your module into your local Course
Builder directory. Run it with `sh scripts/setup.sh -h` for details.

### `src`

Your module's source files. You may put whatever you want here; this sample
module has some templates and a single Python file that declares our handlers.
View that file for details on creating handlers, both with and without user
authentication, and with and without awareness of a current course. When
creating a new module, remember to put an `__init__.py` file in this directory
or you will have import problems.

### `tests`

Your module's test files. You may put whatever you want here; this simple
module provides an example of functional tests using [Webtest]. When creating a
new module, remember to put an `__init__.py` file in this directory or you will
have import problems.

## Working with this module

After you've downloaded and installed this module, start Course Builder normally
to use it:

```sh
sh scripts/start_in_shell.sh
```

In this example, we assume you created a course with a Context Path of `/first`
(this is what Course Builder does for you if you clicked **Create Empty Course**
on the welcome screen after starting a new CB install for the first time). We
also assume you're starting your local server on the default hostname and port.

View the global handler at `http://localhost:8081/global`. Sign in and out to
see how the UI changes.

Now, view the handler that's aware of the current course at
`http://localhost:8081/first/local`. Notice how it can display the name of the
course. Signing in and out works as before, but note you will not be able to
view the handler when signed out unless you've edited the course to make it
public. This is normal: Course Builder does not display newly-created courses to
the public by default so you can hold off on showing your content to people
before it's done.

### Running tests

You can run specific tests with `test.sh`, which is in `coursebuilder/scripts`.
For example, after you've installed this module, you can run all its tests from
the Course Builder root with:

```sh
sh scripts/test.sh tests.ext.hello.functional_tests
```

To run all tests in Course Builder as well as your module, run

```sh
python scripts/run_all_tests.py
```

## That's it

Enjoy writing Course Builder modules, and please feel free to use this as a
base. If you find things you can't do in modules, hit us up on the
[Course Builder Forums].

[Course Builder]:https://code.google.com/p/course-builder/
[Course Builder Forums]:https://groups.google.com/forum/?fromgroups#!forum/course-builder-forum
[Webtest]:http://webtest.pythonpaste.org/en/latest/
