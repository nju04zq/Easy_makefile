# Easy_makefile

## Why we need this?

It's always annoying me to create Makefile on a C project, especially when the project is a large and complex one. Now we have this python script to generate makefile for linux C projects. You only have to tell it which targets you want to build and those C source files the targets relying on.

## How to build the example project

- Goto dir libxml/lib, run "make", to build out the libxml.so.(This is actually not a step to use easy_makefile)
- Under the root dir, run "python build.py", to generate the Makefile in the same directory.
- Under the root dir, run "make", then check the build result, whether it's good. The build outputs are placed in the build/ dir.
- Run "make clean", to clean build/ dir. Note, the generated Makefile won't be cleaned out. You need to remove it manually.

## How to use easy_makefile?
- Prepare your project, basically all those souce files.
- Write the content.mk file, and put it under the root dir. How to write it? You can refer to the following section.
- Run "python build.py" to generate the Makefile.

## Introduction to the example project

The build.py is the easy_makefile tool. The content.mk is an example configure file. The others are source files/directories for a example project, with abbreviation as ch.

In the content.mk file, ch, libch-pf.so... are targets to build. The variable definition "ch = ..." is used to specify C soure files required for this "ch" target.

For this example project ch, two versions are supported, process version and library version. For process version, ch runs as a single process, and libch-notify.so is provided for other modules to utilise the notify functionality from ch(for real project IPC is needed). For library version, ch runs inside other process as a library libch.so. Also, as ch is supposed to run on various platforms, platform-dependent(PD) code should be isolated, in this case into libch-pf.so.

The directory libxml is for a library that ch relies on. The libxml/include contains all those external header files. The libxml/lib contains the source code which could build into a so library libxml.so, using the Makefile in the same directory.

There is also a sub module gvd. It's designed as a test tool for ch, but it won't be released. So we need to provide a choice, whether to build in gvd, cooperated with ch process/library version as gvd_proc/gvd_lib. And for ch process version, ch_gvd is required to replace normal ch, in order to introduce the ability to communicate with gvd.

The content.mk file illustrates the build targets definition. And Makefile is the corresponding Makefile produced by easy_makefile.
