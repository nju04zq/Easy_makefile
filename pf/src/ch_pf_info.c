#include <stdio.h>
#include <core/include/ch_util.h>

char *
ch_pf_get_info (void)
{
    char *str;

    str = test_util();
    printf("%s: %s", __FUNCTION__, str);

    return "pf_sys_info";
}
