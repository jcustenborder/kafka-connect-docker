# Introduction

This project is way for me to create docker images of the containers that I use the most from the 
[Confluent Hub](https://www.confluent.io/hub/). The scripts here are used to connect to the 
Confluent Hub API and find connectors that are specified in `images.yml`. This isn't necessarily 
designed to be a production workflow. This repository is mainly to make my life easier by keeping 
connector images consistent across multiple versions of the Confluent images. Take a look at 
my [cp-kafka-connect](https://github.com/jcustenborder/cp-kafka-connect) and 
[cp-server-connect-operator](https://github.com/jcustenborder/cp-server-connect-operator) images 
for examples of how to maintain images with your own selection of connectors from the Confluent Hub.
