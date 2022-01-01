# FFID Service

`ffid.ffixp.net` is a service for [FFIXP](https://ffixp.net) peers to keep track of each other from a central server.

This service should not be manually interacted with, but instead exists for routing tools to query periodically. The API is read-only.

## Why FFID

The goal of FFID is to provide an internal substitute to [Autonomous System Numbers](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) in order to support peers without their own registered ASN.

FFIDs themselves are simply 3-byte hex numbers (although we keep the first byte locked at `FF` because it looks cool). This is handy, because we can assign IPv6 addresses based off of peer's FFID. For example:

```
FF0123 -> fd00:0123::1
```

NOTE: The real address conversion system in place is **not** the one shown above.
