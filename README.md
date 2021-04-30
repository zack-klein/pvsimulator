# pvsimulator

This is a simple application that simulates real-time power outputs from a power meter, communicated via a message broker.

# Components
There are four services involved here:

1. Rabbit MQ (message broker)
1. Meter service (pvsimulator/meter.py)
1. PV simulator service (pvsimulator/pvsimulator.py)
1. Dashboard (pvsimulator/dashboard.py)


# Spin it up locally

:warning: **WARNING:** Docker/docker-compose is required. You can download it for free [here](https://docs.docker.com/get-docker/).

Once you have docker installed, hit:

```
docker-compose up
```

:fire: And that's it! :fire:

There are a few ways to see it working. First, in the logs you should see A LOT of messages after around 5 seconds:

```
meter          | INFO:meter:[ ] Sent: {'measurement': 5460.258130074662}
pvsimulator    | INFO:pvsimulator:[x] Consumed: {'measurement': 5460.258130074662}
```

This is all well and good, but what does it mean?  To visualize what's happening, you can check out the dashboard (using the amazing [Streamlit](https://streamlit.io/) framework). Head to http://localhost, where you will see a dashboard update in real-time!

# Interesting tidbit on data storage

You can see an example of the file we use to store consumed messages after transformation at `results.jsonl`. You may notice that we use the JSON Lines file format here. Why not just normal JSON, you ask?  Because ideally we will stream data through this system pretty quickly, and as the file gets bigger and bigger, if we had to continuously update one big JSON array, we would end up with a lot of overhead when consuming messages (we would need to read the WHOLE array EVERY update!). With JSON Lines, we can open up the file in append mode and just keep stacking new messages as they come in. This way, we're not burdened with any read latency at write time.

Of course, the right way to store data like this is to not use a file at all and to instead use a separate storage service that is built to handle high-volume, low-latency reading/writing (think something like Redis). But this works for a small project!