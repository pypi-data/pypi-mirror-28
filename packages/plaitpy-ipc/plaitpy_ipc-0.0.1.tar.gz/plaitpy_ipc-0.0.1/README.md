## plaitpy-ipc

This module is an external module for plait.py that provides an ecosystem to
run multiple plaitpy processes in, as well as inter-markov process
communication features like locks, queues and shared variables.

### what can be simulated

* simple [M/M/c queues](https://en.wikipedia.org/wiki/M/M/c_queue), like bank teller queues
* kitchen and bathroom usage in a house
* desk usage in a workspace
* multiple agents browsing multiple websites
* etc

### self contained example

The follow is an ecosystem with a single lock. It starts with a parent process
that spawns children every now and then. The children can spawn more children
and so on. The limitation is that only one child can be spawned per tick because of
the "spawner" lock.


    setup: |
      import plaitpy_ipc
      import json

      if not GLOBALS.ecosystem:
        GLOBALS.ecosystem = plaitpy_ipc.Ecosystem()
        GLOBALS.ECO = ecosystem.shared()

        ecosystem.add_lock("spawner", capacity=1)


    fields:
      tick:
       lambda: ecosystem.get_tick()

      make_child:
        onlyif: random.random() > 0.9 and ECO.spawner.grab()
        lambda: ecosystem.spawn("spawner.yaml")

      age:
        initial:
          lambda: 0
        lambda: prev.age + 1

      expired:
        onlyif: random.random() > 0.9 and this.age > 0
        lambda: ecosystem.expire()

      id:
        lambda: ecosystem.get_pid()


    print: |
      for r, p in ecosystem.gen_records():
        print(json.dumps(r))


Because this is a single yaml template for demonstration purposes, the parent
process and children process are sharing the same file. A consequence of this
is that the outermost parent process can not expire because it is not running
inside the ecosystem. Also notice that the parent process is not included in
gen_records.

## ecosystem usage

To create an ecosystem, a parent template must exist that will run the
ecosystem. In the parent template's print method, they will call
`gen_records()`, causing all the processes in the ecosystem to tick forward.

To create a process, `spawn(template_name)` is used. To expire the current
process, `expire()` is called from the process that should expire.

The parent template's fields will *not* be printed when using this pattern, so
they can be used to keep track of state information.

## structures

all resources should be declared ahead of time, using `add_queue`, `add_lock` and
`add_quantity`. Once a resource is declared, it is available through the ecosystem's
shared() variable.

### locks

To synchronize usage of a resource, we use named Locks. The lock can be grabbed
with `grab()` by any process. There is no release function, though - as long as
a process keeps calling `grab()`, they will hold the lock. It takes one tick to
release the lock by inactivity.

Any processes that didn't grab the lock will receive False, while the process
that did grab the lock will receive True.

Locks can have a capacity, which specifies how many individual processes can
hold that lock at once.

### queues

Queues are similar to locks, except the order of which process tried to grab
the lock is retained in a FIFO manner. Similar to a lock, the queue unlocks
implicitly and takes one tick of inactivity to be released.

## visualization

A simple table visualizer exists to watch processes as long as they have an
*id* and *tick* field in them. See the makefile's *bank* and *ecosystem* rules
for how to generate a `viz/output.js` file, then load `viz/viz.html` in a browser.

