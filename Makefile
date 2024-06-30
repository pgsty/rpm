# build repo in parallel by default
b: rebuild

# build repo in parallel
rebuild:
	./rebuild

# build repo one by one
build:
	./build	infra/x86_64
	./build	infra/aarch64
	./build	pgsql/el7.x86_64
	./build	pgsql/el8.x86_64
	./build	pgsql/el9.x86_64

# build repo manually
create:
	cd /data/repo/rpm/infra/x86_64     && createrepo_c . && repo2module -s stable . modules.yaml && modifyrepo_c --mdtype=modules modules.yaml repodata/
	cd /data/repo/rpm/infra/aarch64    && createrepo_c . && repo2module -s stable . modules.yaml && modifyrepo_c --mdtype=modules modules.yaml repodata/
	cd /data/repo/rpm/pgsql/el7.x86_64 && createrepo_c .
	cd /data/repo/rpm/pgsql/el8.x86_64 && createrepo_c . && repo2module -s stable . modules.yaml && modifyrepo_c --mdtype=modules modules.yaml repodata/
	cd /data/repo/rpm/pgsql/el9.x86_64 && createrepo_c . && repo2module -s stable . modules.yaml && modifyrepo_c --mdtype=modules modules.yaml repodata/

push-sv:
	rsync -avc ./pgsql/ sv:/data/rpm/pgsql/
pushd-sv:
	rsync -avc --delete ./pgsql/ sv:/data/rpm/pgsql/
repo-sv:
	ssh sv 'cd /data/rpm && make'
pull-sv:
	rsync -avc sv:/data/rpm/pgsql/ ./pgsql/
pulld-sv:
	rsync -avc --delete sv:/data/rpm/pgsql/ ./pgsql/

.PHONY: b rebuild build create