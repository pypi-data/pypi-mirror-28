'''a wrapper for kafka.KafkaProducer, kafka.KafkaConsumer

'''

from kafka import KafkaProducer, KafkaConsumer


class KafkaIO(object):
    '''
    '''
    def __init__(self, kafkahost=None,
                 client_id=None, group_id=None,
                 input_topics=(), output_topic=None,
                 input_config={}, output_config={}):
        '''Initialize a new KafkaIO

        Keyword Arguments:
          kafkahost:
          client_id:
          group_id:
          input_topics:
          output_topic:
          input_config:
          output_config:

        '''
        self.input_config.update(input_config)
        self.output_config.update(output_config)
        self.output_topic = output_topic
        for d in [self.input_config, self.output_config]:
            if kafkahost:
                d.setdefault('bootstrap_servers', kafkahost)
            if client_id:
                d.setdefault('client_id', client_id)
        if input_topics:
            self.subscribe(topics=input_topics)

    @property
    def input_config(self):
        try:
            return self._input_config
        except AttributeError:
            pass
        self._input_config = {}
        return self._input_config

    @property
    def output_config(self):
        try:
            return self._output_config
        except AttributeError:
            pass
        self._output_config = {}
        return self._output_config

    @property
    def input(self):
        '''A kafka.KafkaConsumer configured via input_config.
        '''
        try:
            return self._input
        except AttributeError:
            pass
        self._input = KafkaConsumer(**self.input_config)
        return self._input

    @property
    def output(self):
        '''A kafka.KafkaProducer configured via output_config
        '''
        try:
            return self._output
        except AttributeError:
            pass
        self._output = KafkaProducer(**self.output_config)
        return self._output

    @property
    def client_id(self):
        '''
        '''
        return self.input.config['client_id']

    @client_id.setter
    def client_id(self, new_value):
        '''
        '''
        self.input.config['client_id'] = new_value
        self.output.config['client_id'] = new_value

    @property
    def group_id(self):
        '''
        '''
        return self.input.config['group_id']

    @group_id.setter
    def group_id(self, new_value):
        '''
        '''
        self.input.config['group_id'] = new_value

    def subscribe(self, topics=(), pattern=None):
        '''Subscribe to a list of topics or a topic regex pattern.

        See kafka.KafkaConsumer.subscribe
        '''
        self.input.subscribe(topics=topics, pattern=pattern)

    def subscription(self):
        '''Set of input topics current subscribed to.

        See kafka.KafkaConsumer.subscription
        '''
        try:
            return self.input.subscription()
        except AttributeError:
            pass
        return []

    def topics(self):
        '''List of Kafka topics the user is authorized to view.

        See kafka.KafkaConsumer.topics
        '''
        return self.input.topics()

    def write(self, value, topic=None, key=None, partition=None, flush=False):
        '''Publish a message to a topic.

        See kafka.KafkaProducer.send.
        '''
        self.output.send(topic or self.output_topic,
                         value=value,
                         key=key,
                         partition=partition)
        if flush:
            self.output.flush()

    def read(self, timeout_ms=0, max_records=None, commit=True):
        '''Fetch data from subscribed topics.

        Returns a dictionary of messages published to subscribed topics.

        See kafka.KafkaProducer.poll
        '''
        messages = self.input.poll(timeout_ms=timeout_ms,
                                   max_records=max_records)
        if messages and commit:
            try:
                self.input.commit_async()
            except AssertionError:
                pass
        return messages
