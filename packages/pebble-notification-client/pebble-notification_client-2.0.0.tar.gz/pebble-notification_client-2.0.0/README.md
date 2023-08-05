# Notification Client

A client app for Pebble's notification system. Sends event data to Amazon SQS
for later processing by `notification-centre`.

## Installation

Install from PyPi:

```
pip install pebble-notification-client
```

## Usage

* Set `AWS_EVENT_QUEUE` to the name of the events queue in your app's
  `settings.py`
* Import `notification_client`
* Call `send_event` to push an event to SQS (see `utils.py` for full
  documentation)
