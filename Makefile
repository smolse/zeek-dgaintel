build:
	docker build -t zeek-dgaintel .

test:
	docker build --target=test -t zeek-dgaintel-test .

clean:
	docker rmi -f zeek-dgaintel-test zeek-dgaintel

run-zeek:
	zeek --no-unused-warnings --no-checksums -i eth0 dgaintel.example.zeek

run-zeek-dgaintel: build
	docker run --rm -it --env-file=./local.env zeek-dgaintel --log_level=INFO
