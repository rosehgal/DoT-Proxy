## DNS-over-TLS proxy

This is very simple and mimimilistic, DNS proxy service capable of running in multi-thread mode, handling multilpe connections in parallel and build using python.

This is packaged with Docker and Dcoker-compose. Docker Compose can help deploy this in docker stack infrastructure or kubernetes.
The module Execution starts from `DNSoverTLS.__main__:start()` method.


```bash
+--------------+   U/T     +----------------------+     TCP   +-----------------------------+
|              + --------> +                      + --------> +                             |
|   DNS Req    |           |       DNS Proxy      |           |    Cloudflare - TLS - DNS   |
|              + <-------- +                      + <-------- +                             |
+--------------+    U/T    +----------------------+     TCP   +-----------------------------+
                             8053(UDP) - 8853(TCP)

```

### How to run:

#### Single service
```bash
# Build Docker
docker build -t dns .

# Run the docker Image
docker run -d -p 8053:8053/udp -p8853:8853 -t dns

# Test the proxy
# Handle TCP connections
dig @127.0.0.1 -p8853 rsehgal.in +tcp

# Handle UDP connections.
dig @127.0.0.1 -p8053 rsehgal.in

; <<>> DiG 9.11.3-1ubuntu1.11-Ubuntu <<>> @127.0.0.1 -p9090 rsehgal.in
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32042
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".........................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;rsehgal.in.			IN	A

;; ANSWER SECTION:
rsehgal.in.		20	IN	A	206.189.89.118
rsehgal.in.		20	IN	A	157.230.35.153

;; Query time: 589 msec
;; SERVER: 127.0.0.1#9090(127.0.0.1)
;; WHEN: Sat Sep 12 08:40:31 UTC 2020
;; MSG SIZE  rcvd: 468
```

#### Build and Deploy in cluster
```bash
# Build docker compose
docker-compose build .

# Run compose in docker-swarm mode
# Create master node
docker swarm init

# Join the Swarm, create multinode cluster
docker swarm join --token <SWARMTOKEN>

# Deploy proxy in swarn
docker stack deploy  --compose-file docker-compose.yml dns-proxy

# Handle TCP connections
dig @127.0.0.1 -p8853 rsehgal.in +tcp

# Handle UDP connections.
dig @127.0.0.1 -p8053 rsehgal.in

; <<>> DiG 9.11.3-1ubuntu1.11-Ubuntu <<>> @127.0.0.1 -p9090 rsehgal.in
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29786
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".........................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;rsehgal.in.			IN	A

;; ANSWER SECTION:
rsehgal.in.		20	IN	A	157.230.35.153
rsehgal.in.		20	IN	A	157.230.37.202

;; Query time: 522 msec
;; SERVER: 127.0.0.1#9090(127.0.0.1)
;; WHEN: Sat Sep 12 08:51:22 UTC 2020
;; MSG SIZE  rcvd: 468
```

### Proxy features
1. Supports TCP and UDP connections with Proxy.
1. Ready to use logging module.
2. Threaded server.
3. Packaged as docker.
4. Packaged as docker-compose.
    1. Ready to deploy in docker-swarm cluster, multinode deployment.
5. No third party library used.
6. No dependencies.
7. Currently connects with Cloudflare only, but can me modified to work with any DNS-TLS providers.
7. Server certificate verification using SSL.

