#!/usr/bin/env bash

echo "=> Installing Cloud Foundry CLI..."
wget 'https://cli.run.pivotal.io/stable?release=linux64-binary&source=github' -qO cf-linux-amd64.tgz
tar -zxvf cf-linux-amd64.tgz
rm cf-linux-amd64.tgz

echo "=> Logging into Cloud Foundry..."
./cf api $CF_API --skip-ssl-validation
./cf login -u $CF_USERNAME -p $CF_PASSWORD -o $CF_ORG -s $CF_SPACE

echo "=> Deploying to Cloud Foundry..."
./cf push
./cf logout