#!/bin/bash

set -ex

rm -rf /backup/s3workspace/
mkdir /backup/s3workspace/
cd /backup/s3workspace/

mkdir -p bucket/mysql/ bucket/mongo/ bucket/sharelatex/ bucket/redis/

mysqldump -hmysql -ubackup -p"${MYSQL_BACKUP_PASSWORD}" --single-transaction --all-databases --ignore-table=cgserver.serverlist_clientreport >all-databases.sql
mongodump -h mongo
tar cvf sharelatex.tar -C/mnt --exclude='data/compiles/*' sharelatex/
redis-cli -h redis SAVE
tar cvf dump.tar dump/

xz -0 all-databases.sql
xz -0 dump.tar
xz -0 sharelatex.tar
xz -0 -c /mnt/redis/dump.rdb >dump.rdb.xz

openssl rand 32 >aes_key
openssl rsautl -encrypt -in aes_key -pubin -inkey <(echo "-----BEGIN PUBLIC KEY-----"; printenv BACKUP_PUBKEY; echo "-----END PUBLIC KEY-----") -out bucket/aes_key.enc
openssl enc -e -aes-256-cbc -in all-databases.sql.xz -kfile aes_key -out bucket/mysql/all-databases.sql.xz.enc
openssl enc -e -aes-256-cbc -in dump.tar.xz -kfile aes_key -out bucket/mongo/dump.tar.xz.enc
openssl enc -e -aes-256-cbc -in sharelatex.tar.xz -kfile aes_key -out bucket/sharelatex/sharelatex.tar.xz.enc
openssl enc -e -aes-256-cbc -in dump.rdb.xz -kfile aes_key -out bucket/redis/dump.rdb.xz.enc
rm -f aes_key

s3cp() {
    aws --cli-read-timeout=30 --cli-connect-timeout=5 --region="${AWS_S3_REGION}" s3 cp --recursive bucket/ s3://"${AWS_S3_BUCKET}"/
}

s3cp || s3cp || s3cp

rm -rf /bucket/s3workspace/

# How to decrypt
#openssl rsautl -decrypt -in aes_key.enc -inkey id_rsa.pem -out aes_key
#openssl enc -d -aes-256-cbc -in file.xz.enc -kfile aes_key -out file.xz
#xz -d file.xz
