#include <stdio.h>
#include <libxml/include/libxml.h>
#include <pf/include/ch_pf_info.h>

char *
test_msg (void)
{
    char *pf_info, *xml;

    pf_info = ch_pf_get_info();
    printf("Get pf info %s\n", pf_info);

    xml = make_xml();
    printf("make xml, %s\n", xml);

    return "test_msg";
}
