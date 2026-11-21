#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2026-09-03
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   Apache-2.0
#==============================================================#

ACTIVE_PG_VERSIONS := 19 18 17 16 15

setup:
	@echo "# Install pgext in the Linux builder, or use ../docker build images"
	@echo "pgext env repo"
	@echo "pgext env tool"
	@echo "pgext env spec"
	@echo "pgext env rust"
	@echo "pgext env pgrx"
	@echo "pgext pkg <name...> --pg 19"

# Specs and build helpers are synchronized separately from sources and build
# products.  Keep remote build roots free of local staging and output files.
SPEC_RSYNC_ARGS := -az \
	--exclude=/BUILD/ --exclude=/BUILDROOT/ --exclude=/RPMS/ \
	--exclude=/SRPMS/ --exclude=/SOURCES/ --exclude=.DS_Store

###############################################################
#                      Prepare Environment                    #
###############################################################
pm:   specm   srcm
p9:   spec9   src9    
p10:  spec10  src10   
p9a:  spec9a  src9a   
p10a: spec10a src10a

###############################################################
#                      Push SPEC to Remote                    #
###############################################################
spec: spec9 spec10 spec9a spec10a
specm:
	rsync $(SPEC_RSYNC_ARGS) rpmbuild/ meta:~/rpmbuild/
spec9:
	rsync $(SPEC_RSYNC_ARGS) rpmbuild/ el9:~/rpmbuild/
spec10:
	rsync $(SPEC_RSYNC_ARGS) rpmbuild/ el10:~/rpmbuild/

spec9a:
	rsync $(SPEC_RSYNC_ARGS) rpmbuild/ el9a:~/rpmbuild/
spec10a:
	rsync $(SPEC_RSYNC_ARGS) rpmbuild/ el10a:~/rpmbuild/

###############################################################
#                      Push SRC to Remote                     #
###############################################################
# Update remote source tarball
src: src9 src10 src9a src10a
srcm:
	rsync -avz src/ meta:~/ext/src/
src9:
	rsync -avz src/ el9:~/rpmbuild/SOURCES/
src10:
	rsync -avz src/ el10:~/rpmbuild/SOURCES/

src9a:
	rsync -avz src/ el9a:~/rpmbuild/SOURCES/
src10a:
	rsync -avz src/ el10a:~/rpmbuild/SOURCES/

###############################################################
#                      Pull RPM from Remote                   #
###############################################################
yum-new: yum-clean yum-init
yum-init:
	mkdir -p yum/el9.x86_64 yum/el10.x86_64 yum/meta
	mkdir -p yum/el9.aarch64 yum/el10.aarch64
yum-clean:
	rm -rf yum/el9.x86_64 yum/el10.x86_64
	rm -rf yum/el9.aarch64 yum/el10.aarch64
yum-pull: yum9 yum10 yum9a yum10a
pullx: yum9 yum10
pulla: yum9a yum10a

yumm:
	rsync -avc meta:~/rpmbuild/RPMS/x86_64/  yum/meta/
	rsync -avc meta:~/rpmbuild/RPMS/aarch64/ yum/meta/
yum9:
	rsync -avc el9:~/rpmbuild/RPMS/x86_64/   yum/el9.x86_64/
yum10:
	rsync -avc el10:~/rpmbuild/RPMS/x86_64/  yum/el10.x86_64/
yum9a:
	rsync -avc el9a:~/rpmbuild/RPMS/aarch64/  yum/el9.aarch64/
yum10a:
	rsync -avc el10a:~/rpmbuild/RPMS/aarch64/ yum/el10.aarch64/


###############################################################
#                         Terraform                           #
###############################################################
u: up
up:
	cd tf && terraform apply -auto-approve
	sleep 5
	tf/ssh
	sleep 15
	tf/ssh
a: apply
apply:
	cd tf && terraform apply
d: destory
destory:
	cd tf && terraform destroy -auto-approve
out:
	cd tf && terraform output
ssh:
	tf/ssh
rs:
	git restore tf/terraform.tf
upload:
	bin/upload.sh



###############################################################
#                         Inventory                           #
###############################################################
.PHONY: setup \
	pm p9 p10 p9a p10a \
	spec specm spec9 spec10 spec9a spec10a \
	src srcm src9 src10 src9a src10a \
	yum-new yum-init yum-clean yum-pull pullx pulla \
	yumm yum9 yum10 yum9a yum10a \
	pg_ttl_index pgfincore etcd_fdw \
	u up a apply d destory out ssh rs upload
