FROM rabbitmq:latest

# Nice suggestion to turn them down:
# https://github.com/docker-library/rabbitmq/issues/225#issuecomment-352530827
RUN echo 'loopback_users.guest = false\n\
    listeners.tcp.default = 5672\n\
    management.tcp.port = 15672\n\
    log.console.level = warning'\
    >> /etc/rabbitmq/rabbitmq.conf