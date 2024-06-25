from confluent_kafka.admin import AdminClient, NewTopic

BOOTSTRAP_SERVERS = 'kafka:9092'
admin_client = AdminClient({'bootstrap.servers': BOOTSTRAP_SERVERS})


def create_topic(topic_name, num_partitions=1, replication_factor=1):
    new_topic = NewTopic(topic_name,
                      num_partitions=num_partitions,
                      replication_factor=replication_factor)
    fs = admin_client.create_topics([new_topic])

    for topic, f in fs.items():
        try:
            f.result()  # Будет выброшено исключение, если произойдет ошибка
            print(f"Топик {topic} успешно создан.")
        except Exception as e:
            print(f"Ошибка при создании топика {topic}: {e}")


if __name__ == "__main__":
    admin_client = AdminClient({'bootstrap.servers': 'kafka:9092'})
    create_topic('input_topic')
    create_topic('output_topic')
