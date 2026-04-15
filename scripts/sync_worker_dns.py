#!/usr/bin/env python3
import json
import os
import sys
import urllib.parse
import urllib.request


DEFAULT_IPS = "144.91.73.228,144.91.77.245,144.91.78.201"


def cf_request(token, method, path, payload=None):
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def find_zone(token, host):
    parts = host.split(".")
    for index in range(len(parts) - 1):
        candidate = ".".join(parts[index:])
        query = urllib.parse.urlencode({"name": candidate, "per_page": 1})
        result = cf_request(token, "GET", f"/zones?{query}")["result"]
        if result:
            return result[0]["id"]
    raise RuntimeError(f"could not resolve Cloudflare zone for {host}")


def sync_host(token, zone_id, host, ips):
    query = urllib.parse.urlencode({"name": host, "per_page": 100})
    result = cf_request(token, "GET", f"/zones/{zone_id}/dns_records?{query}")["result"]
    for record in result:
        if record["type"] in {"A", "AAAA", "CNAME"}:
            cf_request(token, "DELETE", f"/zones/{zone_id}/dns_records/{record['id']}")
            print(f"deleted {host} {record['type']} {record['content']}")

    for ip in ips:
        payload = {
            "type": "A",
            "name": host,
            "content": ip,
            "proxied": False,
            "ttl": 300,
        }
        record = cf_request(token, "POST", f"/zones/{zone_id}/dns_records", payload)["result"]
        print(f"created {host} {record['type']} {record['content']} proxied={record['proxied']}")


def main():
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CLOUDFLARE_API_TOKEN_1")
    if not token:
        raise SystemExit("CLOUDFLARE_API_TOKEN is required")

    hosts = sys.argv[1:]
    if not hosts:
        primary_host = os.environ.get("PRIMARY_DOMAIN_LOCK")
        if primary_host:
            hosts = [primary_host, f"www.{primary_host}"]
    if not hosts:
        raise SystemExit("usage: sync_worker_dns.py <host> [host...]")

    ips = [value.strip() for value in os.environ.get("K8S_LIVE_IPS", DEFAULT_IPS).split(",") if value.strip()]
    if not ips:
        raise SystemExit("K8S_LIVE_IPS is empty")

    zone_id = os.environ.get("CLOUDFLARE_ZONE_ID")
    for host in hosts:
        host_zone_id = zone_id or find_zone(token, host)
        sync_host(token, host_zone_id, host, ips)


if __name__ == "__main__":
    main()
