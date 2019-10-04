#!/bin/bash

set -ex

rm -rf /backup/s3workspace/
mkdir /backup/s3workspace/
cd /backup/s3workspace/

mkdir -p bucket/mysql/ bucket/mongo/ bucket/sharelatex/

mysqldump -hmysql -ubackup -p"${MYSQL_BACKUP_PASSWORD}" --single-transaction --all-databases --ignore-table=cgserver.serverlist_clientreport >all-databases.sql
/usr/local/bin/mongodump -h mongo
tar cvf sharelatex.tar -C/mnt sharelatex/
tar cvf dump.tar dump/

xz -0 all-databases.sql
xz -0 dump.tar
xz -0 sharelatex.tar

openssl rand 32 >/dev/shm/aes_key
openssl rsautl -encrypt -in /dev/shm/aes_key -pubin -inkey <(echo "-----BEGIN PUBLIC KEY-----"; printenv BACKUP_PUBKEY; echo "-----END PUBLIC KEY-----") -out bucket/aes_key.enc
openssl enc -e -aes-256-cbc -in all-databases.sql.xz -kfile /dev/shm/aes_key -out bucket/mysql/all-databases.sql.xz.enc
openssl enc -e -aes-256-cbc -in dump.tar.xz -kfile /dev/shm/aes_key -out bucket/mongo/dump.tar.xz.enc
openssl enc -e -aes-256-cbc -in sharelatex.tar.xz -kfile /dev/shm/aes_key -out bucket/sharelatex/sharelatex.tar.xz.enc
rm -f /dev/shm/aes_key

s3cp() {
    aws --cli-read-timeout=30 --cli-connect-timeout=5 --region="${AWS_S3_REGION}" s3 cp --recursive bucket/ s3://"${AWS_S3_BUCKET}"/
}

s3cp || s3cp || s3cp

rm -rf /bucket/s3workspace/

# How to decrypt
#openssl rsautl -decrypt -in aes_key.enc -inkey id_rsa.pem -out aes_key
#openssl enc -d -aes-256-cbc -in file.xz.enc -kfile aes_key -out file.xz
#xz -d file.xz
