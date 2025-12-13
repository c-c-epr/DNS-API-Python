from fastapi import FastAPI, Query, HTTPException
import dns.resolver
import ipaddress

app = FastAPI()

ALLOWED_TYPES = {"A", "AAAA", "MX", "TXT", "NS", "CNAME"}


@app.get("/dns/lookup")
def dns_lookup(
    domain: str = Query(..., example="google.com"),
    record_type: str = Query("A", alias="type"),
    resolver: str = Query("8.8.8.8", example="101.101.101.101"),
):
    record_type = record_type.upper()

    # 驗證 DNS record type
    if record_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported DNS record type")

    # 驗證 resolver IP（不限制來源，只確保是合法 IP）
    try:
        ipaddress.ip_address(resolver)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid resolver IP address")

    dns_resolver = dns.resolver.Resolver()
    dns_resolver.nameservers = [resolver]
    dns_resolver.timeout = 3
    dns_resolver.lifetime = 5

    try:
        answers = dns_resolver.resolve(domain, record_type)

        return {
            "domain": domain,
            "type": record_type,
            "resolver": resolver,
            "records": [r.to_text() for r in answers],
        }

    except dns.resolver.NoAnswer:
        return {
            "domain": domain,
            "type": record_type,
            "resolver": resolver,
            "records": [],
        }

    except dns.resolver.NXDOMAIN:
        raise HTTPException(status_code=404, detail="Domain not found")

    except dns.exception.Timeout:
        raise HTTPException(status_code=504, detail="DNS query timeout")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
