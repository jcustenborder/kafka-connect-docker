FROM confluentinc/cp-kafka-connect
ENV CONNECT_PLUGIN_PATH='/usr/share/java,/usr/share/kafka-connect'

RUN curl -Ls https://github.com/jcustenborder/kafka-connect-memcached/releases/download/0.1.0.6/kafka-connect-memcached-0.1.0.6.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-redis/releases/download/0.0.2.2/kafka-connect-redis-0.0.2.2.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-simulator/releases/download/0.1.118/kafka-connect-simulator-0.1.118.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-snmp/releases/download/0.0.1.9/kafka-connect-snmp-0.0.1.9.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-solr/releases/download/0.1.24/kafka-connect-solr-0.1.24.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-splunk/releases/download/0.2.0.28/kafka-connect-splunk-0.2.0.28.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-spooldir/releases/download/1.0.31/kafka-connect-spooldir-1.0.31.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-transform-archive/releases/download/0.1.0.3/kafka-connect-transform-archive-0.1.0.3.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-transform-cef/releases/download/0.1.0.7/kafka-connect-transform-cef-0.1.0.7.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-transform-common/releases/download/0.1.0.14/kafka-connect-transform-common-0.1.0.14.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-transform-maxmind/releases/download/0.1.0.7/kafka-connect-transform-maxmind-0.1.0.7.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-transform-xml/releases/download/0.1.0.4/kafka-connect-transform-xml-0.1.0.4.tar.gz | tar -xzC /
RUN curl -Ls https://github.com/jcustenborder/kafka-connect-twitter/releases/download/0.2.26/kafka-connect-twitter-0.2.26.tar.gz | tar -xzC /
