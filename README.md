# health-reporter

This is a little python app that runs as a standalone web server. It runs a
series of scripts (supplied by you) in a specified directory and checks whether
any of the scripts exited with a non-zero return code.

When a `GET` request is made to the server it will return either a 200 or a 500
response code depending on whether any of the scripts had a non-zero exit code.

This is designed to be used on nodes that sit behind a load balancer that can
only perform a simple HTTP health check to a single port (e.g. AWS ELBs).

With this app you can test an arbitrary number of things and have full control
over what qualifies a server as healthy or unhealthy.
