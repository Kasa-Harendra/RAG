from fastapi import Request, HTTPException, status, Depends
from time import time
from collections import defaultdict

RATE_LIMIT = 10  # requests per minute
rate_data = defaultdict(list)

def rate_limiter(request: Request):
    ip = request.client.host
    now = time()
    window = 60
    rate_data[ip] = [t for t in rate_data[ip] if now - t < window]
    if len(rate_data[ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded.")
    rate_data[ip].append(now)
    return True
