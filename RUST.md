# Building rust & pgrx Extensions


------

## Node & Machine

```bash
cd pigsty; make rpm
./node.yml -i files/pigsty/rpmbuild.yml -t node_repo,node_pkg

sudo yum groupinstall --nobest -y 'Development Tools';
rpmdev-setuptree
```

------

## Env & Proxy

```bash
PROXY=http://192.168.0.104:8118
export HTTP_PROXY=${PROXY}
export HTTPS_PROXY=${PROXY}
export ALL_PROXY=${PROXY}
export NO_PROXY="localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"
```

```bash
alias pg16="export PATH=/usr/pgsql-16/bin:/root/.cargo/bin:/pg/bin:/usr/share/Modules/bin:/usr/lib64/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/home/vagrant/.cargo/bin;"
alias pg15="export PATH=/usr/pgsql-15/bin:/root/.cargo/bin:/pg/bin:/usr/share/Modules/bin:/usr/lib64/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/home/vagrant/.cargo/bin;"
alias pg14="export PATH=/usr/pgsql-14/bin:/root/.cargo/bin:/pg/bin:/usr/share/Modules/bin:/usr/lib64/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/home/vagrant/.cargo/bin;"
alias pg13="export PATH=/usr/pgsql-13/bin:/root/.cargo/bin:/pg/bin:/usr/share/Modules/bin:/usr/lib64/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/home/vagrant/.cargo/bin;"
alias pg12="export PATH=/usr/pgsql-12/bin:/root/.cargo/bin:/pg/bin:/usr/share/Modules/bin:/usr/lib64/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/home/vagrant/.cargo/bin;"
alias build="HTTPS_PROXY=${PROXY} cargo pgrx package -v"
alias b="HTTPS_PROXY=${PROXY} cargo pgrx package"
```

Edit `~/.ssh/config`:

```bash
echo "Host github.com
    Hostname ssh.github.com
    Port 443
    User git" >> ~/.ssh/config

ssh -T git@github.com
```



------

## rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
```


--------

## pgrx

```bash
cargo install --locked cargo-pgrx@0.12.5  # build latest extensions
cargo install --locked cargo-pgrx@0.11.3  # build most extensions
cargo install --locked cargo-pgrx@0.10.2  # build pgdd & pg_tiktoken
cargo pgrx init
```

--------

## build

Build with `rpmbuild`:

```bash
cd ~/rpmbuild/

make rust: pg_search pg_lakehouse pg_graphql pg_jsonschema wrappers pgmq pg_vectorize pg_later plprql pg_idkit pgsmcrypto pgvectorscale
make pgdd pg_tiktoken 
make pgml # extra setup on el9
```



--------

## Legacy Batch Building Approach

Clone rust extension repo:

```bash
cd ~;
cd ~; git clone --recursive git@github.com:postgresml/postgresml.git  ; cd ~/postgresml     && git checkout v2.9.3
cd ~; git clone --recursive https://github.com/paradedb/paradedb.git  ; cd ~/paradedb       && git checkout v0.8.6
cd ~; git clone git@github.com:supabase/pg_graphql.git                ; cd ~/pg_graphql     && git checkout v1.5.7                 
cd ~; git clone git@github.com:supabase/pg_jsonschema.git             ; cd ~/pg_jsonschema  && git checkout v0.3.1                    
cd ~; git clone git@github.com:supabase/wrappers.git                  ; cd ~/wrappers       && git checkout v0.4.1               
cd ~; git clone git@github.com:tembo-io/pgmq.git                      ; cd ~/pgmq           && git checkout v1.2.1 #v1.3.3           
cd ~; git clone git@github.com:tembo-io/pg_vectorize.git              ; cd ~/pg_vectorize   && git checkout v0.17.0                   
cd ~; git clone git@github.com:tembo-io/pg_later.git                  ; cd ~/pg_later       && git checkout v0.1.1               
cd ~; git clone git@github.com:VADOSWARE/pg_idkit.git                 ; cd ~/pg_idkit       && git checkout v0.2.3               
cd ~; git clone git@github.com:zhuobie/pgsmcrypto.git                 ; #cd ~/pgsmcrypto     && git checkout v0.1.0                 
cd ~; git clone git@github.com:kelvich/pg_tiktoken.git                ; #cd ~/pg_tiktoken    && git checkout v1.0.0                  
cd ~; git clone git@github.com:rustprooflabs/pgdd.git                 ; cd ~/pgdd           && git checkout 0.5.2           
cd ~; git clone git@github.com:kaspermarstal/plprql.git               ; cd ~/plprql         && git checkout v0.1.0             
cd ~; git clone git@github.com:timescale/pgvectorscale.git            ; cd ~/pgvectorscale  && git checkout 0.2.0                    

cd ~/paradedb;     cargo update
cd ~/pgmq/pgmq-rs; cargo update
```

Building rust extensions:

```bash
cd ~/paradedb/pg_search;       pg16 build;    pg15 build;    pg14 build;    pg13 build;  pg12 build; 
cd ~/paradedb/pg_lakehouse;    pg16 build;    pg15 build;                    
cd ~/pg_graphql;               pg16 build;    pg15 build;    pg14 build;     
cd ~/pg_jsonschema;            pg16 build;    pg15 build;    pg14 build;    pg13 build;  pg12 build; 
cd ~/wrappers/wrappers;        pg16 build;    pg15 build;    pg14 build;     
cd ~/pgmq;                     pg16 build;    pg15 build;    pg14 build;    pg13 build;  pg12 build; 
cd ~/pg_tier;                  pg16 build;                                   
cd ~/pg_vectorize/extension;   pg16 build;    pg15 build;    pg14 build;                
cd ~/pg_later;                 pg16 build;    pg15 build;    pg14 build;    pg13 build; 
cd ~/pgsmcrypto;               pg16 build;    pg15 build;    pg14 build;    pg13 build;  pg12 build; 
cd ~/pg_idkit;                 pg16 build;    pg15 build;    pg14 build;    pg13 build;  pg12 build; 
cd ~/plprql/plprql;            pg16 build;    pg15 build;    pg14 build;    pg13 build;  pg12 build; 

export RUSTFLAGS="-C target-feature=+avx2,+fma"
cd ~/pgvectorscale/pgvectorscale; pg16 build;    pg15 build;

# use pgrx version 0.10.2
cd ~/pgdd;                     pg16 build;    pg15 build;    pg14 build;       # 16,15,14
cd ~/pg_tiktoken;              pg16 build;    pg15 build;    pg14 build;       # 16,15,14
```


```bash
rm -rf ~/rpmbuild/SOURCES/pgml_16;          cp -r ~/postgresml/pgml-extension/target/release/pgml-pg16 ~/rpmbuild/SOURCES/pgml_16;
rm -rf ~/rpmbuild/SOURCES/pgml_15;          cp -r ~/postgresml/pgml-extension/target/release/pgml-pg15 ~/rpmbuild/SOURCES/pgml_15;
rm -rf ~/rpmbuild/SOURCES/pgml_14;          cp -r ~/postgresml/pgml-extension/target/release/pgml-pg14 ~/rpmbuild/SOURCES/pgml_14;

rm -rf ~/rpmbuild/SOURCES/pg_search_16;     cp -r ~/paradedb/target/release/pg_search-pg16      ~/rpmbuild/SOURCES/pg_search_16;
rm -rf ~/rpmbuild/SOURCES/pg_search_15;     cp -r ~/paradedb/target/release/pg_search-pg15      ~/rpmbuild/SOURCES/pg_search_15;
rm -rf ~/rpmbuild/SOURCES/pg_search_14;     cp -r ~/paradedb/target/release/pg_search-pg14      ~/rpmbuild/SOURCES/pg_search_14;
rm -rf ~/rpmbuild/SOURCES/pg_search_13;     cp -r ~/paradedb/target/release/pg_search-pg13      ~/rpmbuild/SOURCES/pg_search_13;
rm -rf ~/rpmbuild/SOURCES/pg_search_12;     cp -r ~/paradedb/target/release/pg_search-pg12      ~/rpmbuild/SOURCES/pg_search_12;

rm -rf ~/rpmbuild/SOURCES/pg_lakehouse_16;  cp -r ~/paradedb/target/release/pg_lakehouse-pg16   ~/rpmbuild/SOURCES/pg_lakehouse_16;
rm -rf ~/rpmbuild/SOURCES/pg_lakehouse_15;  cp -r ~/paradedb/target/release/pg_lakehouse-pg15   ~/rpmbuild/SOURCES/pg_lakehouse_15;

rm -rf ~/rpmbuild/SOURCES/pg_graphql_16;    cp -r ~/pg_graphql/target/release/pg_graphql-pg16 ~/rpmbuild/SOURCES/pg_graphql_16;
rm -rf ~/rpmbuild/SOURCES/pg_graphql_15;    cp -r ~/pg_graphql/target/release/pg_graphql-pg15 ~/rpmbuild/SOURCES/pg_graphql_15;
rm -rf ~/rpmbuild/SOURCES/pg_graphql_14;    cp -r ~/pg_graphql/target/release/pg_graphql-pg14 ~/rpmbuild/SOURCES/pg_graphql_14;

rm -rf ~/rpmbuild/SOURCES/pg_jsonschema_16; cp -r ~/pg_jsonschema/target/release/pg_jsonschema-pg16 ~/rpmbuild/SOURCES/pg_jsonschema_16;
rm -rf ~/rpmbuild/SOURCES/pg_jsonschema_15; cp -r ~/pg_jsonschema/target/release/pg_jsonschema-pg15 ~/rpmbuild/SOURCES/pg_jsonschema_15;
rm -rf ~/rpmbuild/SOURCES/pg_jsonschema_14; cp -r ~/pg_jsonschema/target/release/pg_jsonschema-pg14 ~/rpmbuild/SOURCES/pg_jsonschema_14;
rm -rf ~/rpmbuild/SOURCES/pg_jsonschema_13; cp -r ~/pg_jsonschema/target/release/pg_jsonschema-pg13 ~/rpmbuild/SOURCES/pg_jsonschema_13;
rm -rf ~/rpmbuild/SOURCES/pg_jsonschema_12; cp -r ~/pg_jsonschema/target/release/pg_jsonschema-pg12 ~/rpmbuild/SOURCES/pg_jsonschema_12;

rm -rf ~/rpmbuild/SOURCES/wrappers_16;      cp -r ~/wrappers/target/release/wrappers-pg16 ~/rpmbuild/SOURCES/wrappers_16;
rm -rf ~/rpmbuild/SOURCES/wrappers_15;      cp -r ~/wrappers/target/release/wrappers-pg15 ~/rpmbuild/SOURCES/wrappers_15;
rm -rf ~/rpmbuild/SOURCES/wrappers_14;      cp -r ~/wrappers/target/release/wrappers-pg14 ~/rpmbuild/SOURCES/wrappers_14;

rm -rf ~/rpmbuild/SOURCES/pgmq_16;          cp -r ~/pgmq/target/release/pgmq-pg16 ~/rpmbuild/SOURCES/pgmq_16;
rm -rf ~/rpmbuild/SOURCES/pgmq_15;          cp -r ~/pgmq/target/release/pgmq-pg15 ~/rpmbuild/SOURCES/pgmq_15;
rm -rf ~/rpmbuild/SOURCES/pgmq_14;          cp -r ~/pgmq/target/release/pgmq-pg14 ~/rpmbuild/SOURCES/pgmq_14;
rm -rf ~/rpmbuild/SOURCES/pgmq_13;          cp -r ~/pgmq/target/release/pgmq-pg13 ~/rpmbuild/SOURCES/pgmq_13;
rm -rf ~/rpmbuild/SOURCES/pgmq_12;          cp -r ~/pgmq/target/release/pgmq-pg12 ~/rpmbuild/SOURCES/pgmq_12;

rm -rf ~/rpmbuild/SOURCES/pg_later_16;      cp -r ~/pg_later/target/release/pg_later-pg16 ~/rpmbuild/SOURCES/pg_later_16;
rm -rf ~/rpmbuild/SOURCES/pg_later_15;      cp -r ~/pg_later/target/release/pg_later-pg15 ~/rpmbuild/SOURCES/pg_later_15;
rm -rf ~/rpmbuild/SOURCES/pg_later_14;      cp -r ~/pg_later/target/release/pg_later-pg14 ~/rpmbuild/SOURCES/pg_later_14;
rm -rf ~/rpmbuild/SOURCES/pg_later_13;      cp -r ~/pg_later/target/release/pg_later-pg13 ~/rpmbuild/SOURCES/pg_later_13;

rm -rf ~/rpmbuild/SOURCES/vectorize_16;     cp -r ~/pg_vectorize/extension/target/release/vectorize-pg16 ~/rpmbuild/SOURCES/vectorize_16;
rm -rf ~/rpmbuild/SOURCES/vectorize_15;     cp -r ~/pg_vectorize/extension/target/release/vectorize-pg15 ~/rpmbuild/SOURCES/vectorize_15;
rm -rf ~/rpmbuild/SOURCES/vectorize_14;     cp -r ~/pg_vectorize/extension/target/release/vectorize-pg14 ~/rpmbuild/SOURCES/vectorize_14;

rm -rf ~/rpmbuild/SOURCES/pg_idkit_16;      cp -r ~/pg_idkit/target/release/pg_idkit-pg16 ~/rpmbuild/SOURCES/pg_idkit_16;
rm -rf ~/rpmbuild/SOURCES/pg_idkit_15;      cp -r ~/pg_idkit/target/release/pg_idkit-pg15 ~/rpmbuild/SOURCES/pg_idkit_15;
rm -rf ~/rpmbuild/SOURCES/pg_idkit_14;      cp -r ~/pg_idkit/target/release/pg_idkit-pg14 ~/rpmbuild/SOURCES/pg_idkit_14;
rm -rf ~/rpmbuild/SOURCES/pg_idkit_13;      cp -r ~/pg_idkit/target/release/pg_idkit-pg13 ~/rpmbuild/SOURCES/pg_idkit_13;
rm -rf ~/rpmbuild/SOURCES/pg_idkit_12;      cp -r ~/pg_idkit/target/release/pg_idkit-pg12 ~/rpmbuild/SOURCES/pg_idkit_12;

rm -rf ~/rpmbuild/SOURCES/pgsmcrypto_16;    cp -r ~/pgsmcrypto/target/release/pgsmcrypto-pg16 ~/rpmbuild/SOURCES/pgsmcrypto_16;
rm -rf ~/rpmbuild/SOURCES/pgsmcrypto_15;    cp -r ~/pgsmcrypto/target/release/pgsmcrypto-pg15 ~/rpmbuild/SOURCES/pgsmcrypto_15;
rm -rf ~/rpmbuild/SOURCES/pgsmcrypto_14;    cp -r ~/pgsmcrypto/target/release/pgsmcrypto-pg14 ~/rpmbuild/SOURCES/pgsmcrypto_14;
rm -rf ~/rpmbuild/SOURCES/pgsmcrypto_13;    cp -r ~/pgsmcrypto/target/release/pgsmcrypto-pg13 ~/rpmbuild/SOURCES/pgsmcrypto_13;
rm -rf ~/rpmbuild/SOURCES/pgsmcrypto_12;    cp -r ~/pgsmcrypto/target/release/pgsmcrypto-pg12 ~/rpmbuild/SOURCES/pgsmcrypto_12;

rm -rf ~/rpmbuild/SOURCES/plprql_16;        cp -r ~/plprql/target/release/plprql-pg16 ~/rpmbuild/SOURCES/plprql_16;
rm -rf ~/rpmbuild/SOURCES/plprql_15;        cp -r ~/plprql/target/release/plprql-pg15 ~/rpmbuild/SOURCES/plprql_15;
rm -rf ~/rpmbuild/SOURCES/plprql_14;        cp -r ~/plprql/target/release/plprql-pg14 ~/rpmbuild/SOURCES/plprql_14;
rm -rf ~/rpmbuild/SOURCES/plprql_13;        cp -r ~/plprql/target/release/plprql-pg13 ~/rpmbuild/SOURCES/plprql_13;
rm -rf ~/rpmbuild/SOURCES/plprql_12;        cp -r ~/plprql/target/release/plprql-pg12 ~/rpmbuild/SOURCES/plprql_12;

rm -rf ~/rpmbuild/SOURCES/vectorscale_16; cp -r ~/pgvectorscale/pgvectorscale/target/release/vectorscale-pg16 ~/rpmbuild/SOURCES/vectorscale_16;
rm -rf ~/rpmbuild/SOURCES/vectorscale_15; cp -r ~/pgvectorscale/pgvectorscale/target/release/vectorscale-pg15 ~/rpmbuild/SOURCES/vectorscale_15;

rm -rf ~/rpmbuild/SOURCES/pgdd_16;          cp -r ~/pgdd/target/release/pgdd-pg16 ~/rpmbuild/SOURCES/pgdd_16;
rm -rf ~/rpmbuild/SOURCES/pgdd_15;          cp -r ~/pgdd/target/release/pgdd-pg15 ~/rpmbuild/SOURCES/pgdd_15;
rm -rf ~/rpmbuild/SOURCES/pgdd_14;          cp -r ~/pgdd/target/release/pgdd-pg14 ~/rpmbuild/SOURCES/pgdd_14;
rm -rf ~/rpmbuild/SOURCES/pgdd_13;          cp -r ~/pgdd/target/release/pgdd-pg13 ~/rpmbuild/SOURCES/pgdd_13;
rm -rf ~/rpmbuild/SOURCES/pgdd_12;          cp -r ~/pgdd/target/release/pgdd-pg12 ~/rpmbuild/SOURCES/pgdd_12;

rm -rf ~/rpmbuild/SOURCES/pg_tiktoken_16;   cp -r ~/pg_tiktoken/target/release/pg_tiktoken-pg16 ~/rpmbuild/SOURCES/pg_tiktoken_16;
rm -rf ~/rpmbuild/SOURCES/pg_tiktoken_15;   cp -r ~/pg_tiktoken/target/release/pg_tiktoken-pg15 ~/rpmbuild/SOURCES/pg_tiktoken_15;
rm -rf ~/rpmbuild/SOURCES/pg_tiktoken_14;   cp -r ~/pg_tiktoken/target/release/pg_tiktoken-pg14 ~/rpmbuild/SOURCES/pg_tiktoken_14;
rm -rf ~/rpmbuild/SOURCES/pg_tiktoken_13;   cp -r ~/pg_tiktoken/target/release/pg_tiktoken-pg13 ~/rpmbuild/SOURCES/pg_tiktoken_13;
rm -rf ~/rpmbuild/SOURCES/pg_tiktoken_12;   cp -r ~/pg_tiktoken/target/release/pg_tiktoken-pg12 ~/rpmbuild/SOURCES/pg_tiktoken_12;

cd ~/rpmbuild/SPECS
make pgml
make pg_search pg_lakehouse
make pg_graphql pg_jsonschema wrappers
make pgmq pg_later pg_vectorize 
make pg_idkit pgsmcrypto plprql pgvectorscale

make pgdd pg_tiktoken
```
