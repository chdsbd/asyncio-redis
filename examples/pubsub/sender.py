#!/usr/bin/env python
import asyncio
import logging

import asyncio_redis

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Enable logging
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().setLevel(logging.INFO)

    def run():
        # Create a new redis connection (this will also auto reconnect)
        connection = yield from asyncio_redis.Connection.create("localhost", 6379)

        try:
            while True:
                # Get input (always use executor for blocking calls)
                text = yield from loop.run_in_executor(None, input, "Enter message: ")

                # Publish value
                try:
                    yield from connection.publish("our-channel", text)
                    print("Published.")
                except asyncio_redis.Error as e:
                    print("Published failed", repr(e))

        finally:
            connection.close()

    loop.run_until_complete(run())
