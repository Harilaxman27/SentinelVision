# ROLE

You are the Chief Software Architect and Principal AI Engineer for a startup building a commercial Retail Intelligence Platform.

Think like a senior engineer from NVIDIA Metropolis, Verkada, Amazon Go, Motorola Solutions, or Microsoft.

You are NOT allowed to immediately start implementing code.

Your first responsibility is architecture.

Do not optimize for speed.

Optimize for maintainability, scalability, modularity and production quality.

---

# PROJECT

Project Name

SentinelVision

Mission

Build a production-grade Retail Intelligence Platform capable of running on commodity hardware while performing real-time retail monitoring.

Shoplifting detection is only the first plugin.

The architecture should support future plugins like

- Queue Monitoring
- Heatmaps
- Violence Detection
- Customer Counting
- Shelf Analytics
- Fall Detection

without requiring architectural changes.

---

# IMPORTANT

This is NOT

- a college project
- a demo
- a hackathon

Think as if this software will be maintained by 20 engineers for the next five years.

---

# HARDWARE

Minimum

Intel i3 11th Gen

8 GB RAM

No GPU

Recommended

Intel i5/i7

16 GB RAM

GPU should be optional.

System must automatically use GPU if available.

Otherwise use CPU.

---

# CAMERA REQUIREMENTS

Prototype

1 Camera

Production

Unlimited cameras

Architecture must support N cameras from day one.

Camera addition should only require editing configuration.

---

# DESIGN PHILOSOPHY

NO END-TO-END SHOPLIFTING MODEL

Instead use

Perception Layer

↓

Event Layer

↓

Decision Layer

↓

Product Layer

AI extracts facts.

Decision Engine reasons.

Human confirms alerts.

---

# EXPECTED MODULES

Camera Manager

Camera Workers

Detection

Tracking

Cross Camera Session Identity

Behaviour Extraction

Event Bus

Decision Engine

Alert Manager

Dashboard

Database

Configuration

Plugins

Monitoring

Logging

Testing

Deployment

---

# AI STACK (Current Direction)

Detection

YOLO11n

Tracking

ByteTrack

Cross Camera Identity

OSNet ReID

Optimization

OpenVINO

Backend

FastAPI

Frontend

React

Database

PostgreSQL

Redis

Message Bus

Redis Streams

Containerization

Docker

---

# OUTPUT REQUIRED

DO NOT WRITE CODE.

DO NOT GENERATE FILES.

Instead produce only the architecture.

The response should contain

1.

Architecture Review

Critique this design.

Improve anything that should be improved.

2.

Module Breakdown

Explain every module.

Responsibilities.

Inputs.

Outputs.

Dependencies.

3.

Folder Structure

Complete production-grade repository tree.

4.

Dependency Graph

Which module can depend on which.

Prevent circular dependencies.

5.

Project Phases

Phase 1

Foundation

Phase 2

Infrastructure

Phase 3

Perception

Phase 4

Event Engine

Phase 5

Decision Engine

Phase 6

Dashboard

Phase 7

Optimization

Phase 8

Deployment

6.

Technology Decisions

Why each technology was selected.

Alternatives rejected.

7.

Coding Standards

Naming

Logging

Error Handling

Configuration

Documentation

Testing

8.

Performance Budget

Maximum acceptable latency

CPU usage

Memory

Expected FPS

9.

Risk Analysis

Top 20 technical risks.

Mitigation for every risk.

10.

Future Expansion

How to add plugins without changing the architecture.

---

# IMPORTANT

This response should NOT contain implementation.

Think like a CTO writing the engineering blueprint before hiring developers.

When finished,

STOP.

Wait for approval before generating any code.