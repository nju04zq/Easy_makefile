####################################
###Makefile generated from script###
####################################
CC=gcc

build_dir = build

install_dir = install

gvd_lib_ver = gvd_lib

PF_LDSO = -L$(build_dir) -lch-pf

CH_COMMON_LDSO = $(PF_LDSO) \
                 -L ../libxml/lib -lxml

ch_LDSO = $(CH_COMMON_LDSO)

ch_gvd_LDSO = $(CH_COMMON_LDSO)

gvd_lib = $(GVD_COMMON)

.PHONY: all
all: $(build_dir)/libch-pf.so \
     $(build_dir)/libch-notify.so \
     $(build_dir)/libch.so \
     $(build_dir)/ch \
     $(build_dir)/ch_gvd \
     $(build_dir)/gvd_proc

ifneq ($(MAKECMDGOALS), clean)
-include $(build_dir)/core/src/ch_db.d
-include $(build_dir)/core/src/ch_msg.d
-include $(build_dir)/core/src/ch_util.d
-include $(build_dir)/gvd/ch/ch_gvd.d
-include $(build_dir)/gvd/gvd/gvd.d
-include $(build_dir)/lib/src/ch_lib_main.d
-include $(build_dir)/lib/src/ch_lib_notify.d
-include $(build_dir)/main/src/ch_gvd_dummy.d
-include $(build_dir)/main/src/ch_main.d
-include $(build_dir)/pf/src/ch_pf_info.d
endif

INCLUDE_DIR = -I. \
              -I..

MK_CFLAGS = -g -D__LINUX__ -Wall -Werror -Wformat -Wcomment -Wimplicit \
            -Wformat-y2k -Wdiv-by-zero -Wendif-labels -Wchar-subscripts \
            -Wbad-function-cast -Wformat-extra-args -Wdisabled-optimization \
            -Wdeprecated-declarations -Wimplicit-function-declaration 

$(build_dir)/libch-pf.so: $(build_dir)/core/src/ch_util.po \
                          $(build_dir)/pf/src/ch_pf_info.po
	$(CC) -shared -fPIC -o $@ $^
	@echo -e "\nGenerated $@\n"

$(build_dir)/libch-notify.so: $(build_dir)/core/src/ch_util.po \
                              $(build_dir)/lib/src/ch_lib_main.po \
                              $(build_dir)/lib/src/ch_lib_notify.po
	$(CC) -shared -fPIC -o $@ $^
	@echo -e "\nGenerated $@\n"

$(build_dir)/libch.so: $(build_dir)/core/src/ch_db.po \
                       $(build_dir)/core/src/ch_msg.po \
                       $(build_dir)/core/src/ch_util.po \
                       $(build_dir)/core/src/ch_util.po \
                       $(build_dir)/lib/src/ch_lib_main.po \
                       $(build_dir)/lib/src/ch_lib_notify.po
	$(CC) -shared -fPIC -o $@ $^
	@echo -e "\nGenerated $@\n"

$(build_dir)/ch: $(build_dir)/core/src/ch_db.o \
                 $(build_dir)/core/src/ch_msg.o \
                 $(build_dir)/core/src/ch_util.o \
                 $(build_dir)/main/src/ch_gvd_dummy.o \
                 $(build_dir)/main/src/ch_main.o
	$(CC) -o $@ $^ $(ch_LDSO)
	@echo -e "\nGenerated $@\n"

$(build_dir)/ch_gvd: $(build_dir)/core/src/ch_db.o \
                     $(build_dir)/core/src/ch_msg.o \
                     $(build_dir)/core/src/ch_util.o \
                     $(build_dir)/gvd/ch/ch_gvd.o \
                     $(build_dir)/main/src/ch_main.o
	$(CC) -o $@ $^ $(ch_gvd_LDSO)
	@echo -e "\nGenerated $@\n"

$(build_dir)/gvd_proc: $(build_dir)/gvd/gvd/gvd.o
	$(CC) -o $@ $^ $(gvd_proc_LDSO)
	@echo -e "\nGenerated $@\n"

$(build_dir)/core/src/%.o: core/src/%.c
	$(CC) -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/core/src/%.po: core/src/%.c
	$(CC) -fPIC -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/gvd/ch/%.o: gvd/ch/%.c
	$(CC) -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/gvd/ch/%.po: gvd/ch/%.c
	$(CC) -fPIC -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/gvd/gvd/%.o: gvd/gvd/%.c
	$(CC) -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/gvd/gvd/%.po: gvd/gvd/%.c
	$(CC) -fPIC -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/lib/src/%.o: lib/src/%.c
	$(CC) -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/lib/src/%.po: lib/src/%.c
	$(CC) -fPIC -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/main/src/%.o: main/src/%.c
	$(CC) -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/main/src/%.po: main/src/%.c
	$(CC) -fPIC -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/pf/src/%.o: pf/src/%.c
	$(CC) -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/pf/src/%.po: pf/src/%.c
	$(CC) -fPIC -o $@ $(MK_CFLAGS) $(INCLUDE_DIR) -c $(filter %c,$^)
	@echo

$(build_dir)/core/src/%.d: core/src/%.c $(build_dir)/core/src/.probe
	@set -e; rm -f $@; \
	echo "Making $@"; \
	$(CC) -MM $(INCLUDE_DIR) $(filter %.c,$^) > $@.$$$$; \
	sed 's#\($*\)\.o[ :]*#$(dir $@)\1.o $(dir $@)\1.po $@ : #g'<$@.$$$$>$@;\
	rm -f $@.$$$$

$(build_dir)/gvd/ch/%.d: gvd/ch/%.c $(build_dir)/gvd/ch/.probe
	@set -e; rm -f $@; \
	echo "Making $@"; \
	$(CC) -MM $(INCLUDE_DIR) $(filter %.c,$^) > $@.$$$$; \
	sed 's#\($*\)\.o[ :]*#$(dir $@)\1.o $(dir $@)\1.po $@ : #g'<$@.$$$$>$@;\
	rm -f $@.$$$$

$(build_dir)/gvd/gvd/%.d: gvd/gvd/%.c $(build_dir)/gvd/gvd/.probe
	@set -e; rm -f $@; \
	echo "Making $@"; \
	$(CC) -MM $(INCLUDE_DIR) $(filter %.c,$^) > $@.$$$$; \
	sed 's#\($*\)\.o[ :]*#$(dir $@)\1.o $(dir $@)\1.po $@ : #g'<$@.$$$$>$@;\
	rm -f $@.$$$$

$(build_dir)/lib/src/%.d: lib/src/%.c $(build_dir)/lib/src/.probe
	@set -e; rm -f $@; \
	echo "Making $@"; \
	$(CC) -MM $(INCLUDE_DIR) $(filter %.c,$^) > $@.$$$$; \
	sed 's#\($*\)\.o[ :]*#$(dir $@)\1.o $(dir $@)\1.po $@ : #g'<$@.$$$$>$@;\
	rm -f $@.$$$$

$(build_dir)/main/src/%.d: main/src/%.c $(build_dir)/main/src/.probe
	@set -e; rm -f $@; \
	echo "Making $@"; \
	$(CC) -MM $(INCLUDE_DIR) $(filter %.c,$^) > $@.$$$$; \
	sed 's#\($*\)\.o[ :]*#$(dir $@)\1.o $(dir $@)\1.po $@ : #g'<$@.$$$$>$@;\
	rm -f $@.$$$$

$(build_dir)/pf/src/%.d: pf/src/%.c $(build_dir)/pf/src/.probe
	@set -e; rm -f $@; \
	echo "Making $@"; \
	$(CC) -MM $(INCLUDE_DIR) $(filter %.c,$^) > $@.$$$$; \
	sed 's#\($*\)\.o[ :]*#$(dir $@)\1.o $(dir $@)\1.po $@ : #g'<$@.$$$$>$@;\
	rm -f $@.$$$$

$(build_dir)/core/src/.probe \
$(build_dir)/gvd/ch/.probe \
$(build_dir)/gvd/gvd/.probe \
$(build_dir)/lib/src/.probe \
$(build_dir)/main/src/.probe \
$(build_dir)/pf/src/.probe:
	@mkdir -p $@

.PHONY: install
install:
	-mkdir $(install_dir); \
	cp $(build_dir)/libch-pf.so $(build_dir)/libch-notify.so $(build_dir)/libch.so $(build_dir)/ch $(build_dir)/ch_gvd $(build_dir)/gvd_proc $(install_dir)

.PHONY: clean
clean:
	-rm -rf $(build_dir)
