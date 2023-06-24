event zeek_init()
    {
    Broker::subscribe("dgaintel/prediction");
    Broker::listen("127.0.0.1", 9999/tcp);
    Broker::auto_publish("dgaintel/dns_request", dns_request);
    }

event dgaintel_prediction(c: connection, query: string, prediction: string)
    {
    print fmt("zeek-dgaintel: DNS request from %s: %s", c$id$orig_h, prediction);
    }
