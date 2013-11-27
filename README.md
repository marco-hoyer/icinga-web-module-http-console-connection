icinga-web-module-http-console-connection
=========================================

Connector for Icinga-web to communicate with Icinga over HTTP

This uses https://github.com/ImmobilienScout24/livestatus_service to expose not only the livestatus socket but also the icinga.cmd via http. Both together allow sending commands from a remotely installed icinga-web instance to one or more icinga instances.
