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
export PGRX_VER=0.11.3

export HTTP_PROXY=${PROXY}
export HTTPS_PROXY=${PROXY}
export ALL_PROXY=${PROXY}
export NO_PROXY="localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"

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
cargo install --locked cargo-pgrx@${PGRX_VER-'0.11.3'}
cargo install --locked cargo-pgrx@${PGRX_VER-'0.10.2'}  # build pgdd & pg_tiktoken
cargo pgrx init
```


--------

## Batch Build

Clone rust extension repo:

```bash
cd ~;
cd ~; git clone --recursive git@github.com:postgresml/postgresml.git  ; cd ~/postgresml     && git checkout v2.9.3
cd ~; git clone --recursive https://github.com/paradedb/paradedb.git  ; cd ~/paradedb       && git checkout v0.8.6
cd ~; git clone git@github.com:supabase/pg_graphql.git                ; cd ~/pg_graphql     && git checkout v1.5.7                 
cd ~; git clone git@github.com:supabase/pg_jsonschema.git             ; cd ~/pg_jsonschema  && git checkout v0.3.1                    
cd ~; git clone git@github.com:supabase/wrappers.git                  ; cd ~/wrappers       && git checkout v0.4.1               
cd ~; git clone git@github.com:tembo-io/pgmq.git                      ; cd ~/pgmq           && git checkout v1.2.1 #v1.3.3           
cd ~; git clone git@github.com:tembo-io/pg_tier.git                   ; cd ~/pg_tier        && git checkout v0.0.4              
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
