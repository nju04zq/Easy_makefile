#include <stdio.h>

#ifdef __CH_LIB_VER__

int lib_ver_mark = 1;

int ch_lib_main (void)
{
    char *test_str;

    printf("lib ver, %s\n", test_str);
    return 0;
}

#endif

#ifdef __CH_PROC_VER__

int proc_ver_mark = 1;

int ch_lib_main (void)
{
    char *test_str;

    printf("proc ver, %s\n", test_str);
    return 0;
}

#endif
