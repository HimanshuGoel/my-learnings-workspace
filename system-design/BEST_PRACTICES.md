# Best Practices

- Containers - Why did containers happen? - Containers weren't mainly about isolation in the VM sense, but about solving the problem of managing many applications, not just many machines. VMs (built for consolidating underutilized hardware) with containers (designed for packaging apps, making deployments reproducible and shareable). One “forbidden thing” Docker introduced was encouraging rebuilds and redeploys instead of patching in place. This shift supports immutability, which simplifies reasoning and (in theory) security.
