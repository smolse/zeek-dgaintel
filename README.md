# zeek-dgaintel

This repository contains a [Zeek Broker](https://zeek.org/) client code for the real-time detection of domain
generation algorithms (DGA), which are commonly used by malware for communicating with the command and control servers.
Detection is performed by intercepting DNS requests with Zeek and feeding the domain names to a CNN-LSTM neural network
model implemented by [dgaintel](https://github.com/sudo-rushil/dgaintel).
