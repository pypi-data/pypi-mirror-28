underworlds is a **distributed and lightweight framework** that facilitates
**building and sharing models of the physical world** surrounding a robot
amongst independent software modules.

These modules can be for instance geometric reasoners (that compute topological
relations between objects), motion planner, event monitors, viewers... any
software that need to access a **geometric** (based on 3D meshes of objects)
and/or **temporal** (based on events) view of the world.

One of the main feature of underworlds is the ability to store many
*parallel* worlds: past models of the environment, future models, models with
some objects filtered out, models that are physically consistent, etc.

This package provides the underworlds server, a Python client library, and a set
of tools to interact with the system (viewers, scene loader, ROS bridge, etc.).

A handful of useful example applications are also provided, like skeleton
tracking (using OpenNI) or visibility tracking.

