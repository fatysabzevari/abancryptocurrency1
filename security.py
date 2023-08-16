from datetime import datetime, timedelta
from database.data_currency import RedisConnection

REQUEST_LIMIT = 3
REQUEST_TIMEFRAME = timedelta(seconds=1)
REQUEST_RECORDS = {}


async def rate_limit_handler(request, call_next):
    remote_address = request.client.host



    now = datetime.now()
    if remote_address in REQUEST_RECORDS:
        record = REQUEST_RECORDS[remote_address]
        if now - record["start_time"] >= REQUEST_TIMEFRAME:
            # reset the request record
            record["start_time"] = now
            record["count"] = 1
        elif record["count"] >= REQUEST_LIMIT:
            # too many requests, raise an exception
            with RedisConnection() as redis:
                redis.client.setex(str(remote_address), 3600, 55)
            return False, 'تعداد درخواست شما بیش از حد مجاز بوده بعد از یک ساعت دوباره تلاش کنید'

        else:
            # increase the request count
            record["count"] += 1
    else:
        # create a new request record
        REQUEST_RECORDS[remote_address] = {"start_time": now, "count": 1}
    response = await call_next(request)
    return True, response
