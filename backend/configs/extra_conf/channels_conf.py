CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}