# Easy_makefile
It's always annoying for me to create Makefile on a C project, especially when the project is a large and complex one. Now we have this python script to generate makefile for linux C projects. You only have to tell it which targets you want to build and those C source files the targets relying on.

The build.py is the easy_makefile tool. The content.mk is an example configure file. The others are files/directories for a example project, with abbreviation as ch.

In the content.mk file, ch/libch-pf.so... are targets to build. The variable definition "ch = ..." is used to specify C soure files required for this "ch" target.

For this example project ch, two versions are supported, process version and library version. For process version, ch runs as a single process, and libch-notify.so is provided for other modules to utilise the notify functionality from ch(for real project IPC is needed). For library version, ch runs inside other process as a library libch.so. Also, as ch is supposed to run on various platforms, platform-dependent(PD) code should be isolated, in this case into libch-pf.so.

There is also a sub module gvd. It's designed as a test tool for ch, but it won't be released. So we need to provide a choice, whether to build in gvd, cooperated with ch process/library version as gvd_proc/gvd_lib. And for ch process version, ch_gvd is required to replace normal ch, in order to introduce the ability to communicate with gvd.

The content.mk file illustrates the build targets definition. And Makefile is the corresponding Makefile produced by easy_makefile.