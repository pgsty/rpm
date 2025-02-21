#==============================================================#
# File      :   Makefile
# Desc      :   pgsty/pgsql-rpm repo shortcuts
# Ctime     :   2024-07-28
# Mtime     :   2024-07-28
# Path      :   Makefile
# Author    :   Ruohang Feng (rh@vonng.com)
# License   :   AGPLv3
#==============================================================#

DEVEL_PATH = sv:/data/rpm

###############################################################
#                        1. Building                          #
###############################################################
init:
	mkdir -p rpm rpm/{el7.x86_64,el8.x86_64,el9.x86_64}
	mkdir -p rpm rpm/{el7.aarch64,el8.aarch64,el9.aarch64}

build: build-amd64 build-arm64
build-amd64:
	./build	rpm/el7.x86_64
	./build	rpm/el8.x86_64
	./build	rpm/el9.x86_64
build-arm64:
	./build	rpm/el7.aarch64
	./build	rpm/el8.aarch64
	./build	rpm/el9.aarch64

builds: builds-amd64 builds-arm64
builds-amd64:
	./build	rpm/el7.x86_64 sign
	./build	rpm/el8.x86_64 sign
	./build	rpm/el9.x86_64 sign
builds-arm64:
	./build	rpm/el7.aarch64 sign
	./build	rpm/el8.aarch64 sign
	./build	rpm/el9.aarch64 sign


###############################################################
#                        2. Syncing                           #
###############################################################
# push/pull project to/from building host
push:
	rsync -avc ./ $(DEVEL_PATH)/
pushd:
	rsync -avc --delete ./ $(DEVEL_PATH)/
pull:
	rsync -avc $(DEVEL_PATH)/ ./
pulld:
	rsync -avc --delete $(DEVEL_PATH)/ ./

# push SRC to building VMs
push-el: push8 push9 #push7
push7:
	rsync -avc --exclude=RPMS --exclude=SRPMS --exclude=BUILD --exclude=BUILDROOT --delete rpmbuild/ el7:~/rpmbuild/
	ssh el7 'cp -f ~/rpmbuild/Makefile.el7 ~/rpmbuild/Makefile'
push8:
	rsync -avc --exclude=RPMS --exclude=SRPMS --exclude=BUILD --exclude=BUILDROOT --delete rpmbuild/ el8:~/rpmbuild/
push9:
	rsync -avc --exclude=RPMS --exclude=SRPMS --exclude=BUILD --exclude=BUILDROOT --delete rpmbuild/ el9:~/rpmbuild/
push8a:
	rsync -avc --exclude=RPMS --exclude=SRPMS --exclude=BUILD --exclude=BUILDROOT --delete rpmbuild/ el8a:~/rpmbuild/
push9a:
	rsync -avc --exclude=RPMS --exclude=SRPMS --exclude=BUILD --exclude=BUILDROOT --delete rpmbuild/ el9a:~/rpmbuild/

# fetch RPMS from bucilding VMs
pull-el: pull9 pull8 pull7
pull7:
	mkdir -p rpmbuild/RPMS/el7.x86_64/
	rsync -avc el7:~/rpmbuild/RPMS/x86_64/ rpmbuild/RPMS/el7.x86_64/ || true
pull8:
	mkdir -p rpmbuild/RPMS/el8.x86_64/
	rsync -avc el8:~/rpmbuild/RPMS/x86_64/ rpmbuild/RPMS/el8.x86_64/ || true
pull9:
	mkdir -p rpmbuild/RPMS/el9.x86_64/
	rsync -avc el9:~/rpmbuild/RPMS/x86_64/ rpmbuild/RPMS/el9.x86_64/ || true

pull-ela: pull9 pull8 #pull7
pull7a:
	rsync -avc el7a:~/rpmbuild/RPMS/aarch64/ rpmbuild/RPMS/el7.aarch64/ || true
pull8a:
	rsync -avc el8a:~/rpmbuild/RPMS/aarch64/ rpmbuild/RPMS/el8.aarch64/ || true
pull9a:
	rsync -avc el9a:~/rpmbuild/RPMS/aarch64/ rpmbuild/RPMS/el9.aarch64/ || true

# sync building specs with el VMs
el-dir:
	ssh el9 'rpmdev-setuptree'
	ssh el8 'rpmdev-setuptree'
	ssh el7 'rpmdev-setuptree'
el-spec:
	rsync -avc --delete rpmbuild/SPECS/   el7:~/rpmbuild/SPECS/
	rsync -avc --delete rpmbuild/SPECS/   el8:~/rpmbuild/SPECS/
	rsync -avc --delete rpmbuild/SPECS/   el9:~/rpmbuild/SPECS/
el-src:
	rsync -avc rpmbuild/SOURCES/ el7:~/rpmbuild/SOURCES/
	rsync -avc rpmbuild/SOURCES/ el8:~/rpmbuild/SOURCES/
	rsync -avc rpmbuild/SOURCES/ el9:~/rpmbuild/SOURCES/

# push to building server, then deliver to el building VMs
ps: push-ss
push-ss: push
	ssh -t sv "cd /data/rpm && make push-el"
psa: push-ssa
push-ssa: push
	ssh -t sv "cd /data/rpm && make push-el"

pl: pull-ss
pull-ss:
	ssh -t sv "cd /data/rpm && make pull-el"
	rsync -avc --delete $(DEVEL_PATH)/rpmbuild/RPMS/ rpmbuild/RPMS/
pull-rpm:
	rsync -avc --delete sv:/data/rpm/rpmbuild/RPMS/ rpmbuild/RPMS/

pp: pull-ssp
pull-ssp:
	ssh -t sv "cd /data/rpm && make pull-el repo7 repo8 repo9"
	rsync -avc --delete $(DEVEL_PATH)/rpmbuild/RPMS/ rpmbuild/RPMS/


###############################################################
#                   5. Build Repo                             #
###############################################################
repo7:
	mkdir -p rpmbuild/RPMS/el7.x86_64/debug
	mv -f rpmbuild/RPMS/el7.x86_64/*debug*.rpm rpmbuild/RPMS/el7.x86_64/debug/ || true
	./build	rpmbuild/RPMS/el7.x86_64       sign
	./build	rpmbuild/RPMS/el7.x86_64/debug sign

repo8:
	mkdir -p rpmbuild/RPMS/el8.x86_64/debug
	mv -f rpmbuild/RPMS/el8.x86_64/*debug*.rpm rpmbuild/RPMS/el8.x86_64/debug/ || true
	./build	rpmbuild/RPMS/el8.x86_64       sign
	./build	rpmbuild/RPMS/el8.x86_64/debug sign

repo9:
	mkdir -p rpmbuild/RPMS/el9.x86_64/debug
	mv -f rpmbuild/RPMS/el9.x86_64/*debug*.rpm rpmbuild/RPMS/el9.x86_64/debug/ || true
	./build	rpmbuild/RPMS/el9.x86_64       sign
	./build	rpmbuild/RPMS/el9.x86_64/debug sign


###############################################################
#                         Terraform                           #
###############################################################
u:
	cd tf && terraform apply -auto-approve
	sleep 5
	tf/ssh
	sleep 15
	tf/ssh
a:
	cd tf && terraform apply
d:
	cd tf && terraform destroy -auto-approve
destroy:
	cd tf && terraform destroy
out:
	cd tf && terraform output
ssh:
	tf/ssh
r:
	git restore tf/terraform.tf



###############################################################
#                         Inventory                           #
###############################################################
.PHONY: init build build-amd64 build-arm64 builds builds-amd64 builds-arm64 \
	push pushd pull pulld push7 push8 push9 push-el pushss