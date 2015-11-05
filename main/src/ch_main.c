#include <stdio.h>
#include <core/include/ch_db.h>
#include <core/include/ch_msg.h>
#include <core/include/ch_util.h>

extern void gvd_init();

int
main (void)
{
    char *test_str;

    gvd_init();

    test_str = test_db();
    printf("%s\n", test_str);
    test_str = test_msg();
    printf("%s\n", test_str);
    test_str = test_util();
    printf("%s\n", test_str);
    return 0;
}

