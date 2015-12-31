# build dir location, do not change the var name
build_dir = build

# install dir location, do not change the var name
install_dir = install

# Do not change the following target var name
ch_proc_ver = ch libch-pf.so libch-notify.so
ch_lib_ver = libch.so libch-pf.so
gvd_proc_ver = ch_gvd gvd_proc
gvd_lib_ver = gvd_lib

# Define include dir
# Do not change the include dir name
INCLUDE_DIR = -I .

# Define CFLAGS
# Do not change the include dir name
MK_CFLAGS = -Wall -Werror \
            -Wbad-function-cast -Wchar-subscripts -Wcomment \
            -Wdeprecated-declarations -Wdisabled-optimization -Wdiv-by-zero \
            -Wendif-labels -Wformat -Wformat-extra-args \
            -Wformat-y2k -Wimplicit -Wimplicit-function-declaration \

UTIL = core/src/ch_util.c

CH_COMMON = $(UTIL) \
            core/src/ch_db.c \
            core/src/ch_msg.c

PF_LDSO = -L$(build_dir) -lch-pf

LIBXML_LDSO = -L ./libxml/lib -lxml

CH_COMMON_LDSO = $(PF_LDSO) \
                 $(LIBXML_LDSO)

ch = $(CH_COMMON) \
     main/src/ch_gvd_dummy.c \
     main/src/ch_main.c

# define relied so path for bin target
# keep the var name as bin_LDSO
ch_LDSO = $(CH_COMMON_LDSO)

libch-pf.so = $(UTIL) \
              pf/src/ch_pf_info.c

LIB_COMMON = $(UTIL) \
             lib/src/ch_lib_notify.c \
             lib/src/ch_lib_main.c

libch-notify.so = $(LIB_COMMON)

libch.so = $(LIB_COMMON) \
           $(CH_COMMON)

GVD_COMMON = gvd/gvd/gvd.c

ch_gvd = $(CH_COMMON) \
         main/src/ch_main.c \
         gvd/ch/ch_gvd.c

ch_gvd_LDSO = $(CH_COMMON_LDSO)

gvd_proc = $(GVD_COMMON)

gvd_lib = $(GVD_COMMON)

