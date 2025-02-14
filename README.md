Network Configuration with OpenConfig and gRPC


Project Overview

This project explores modern network configuration techniques using OpenConfig data models and gRPC-based protocols (gNMI, gNOI, and gRIBI) to manage a simulated campus network. The goal is to provide a scalable, vendor-neutral, and automated solution to network configuration, monitoring, and security enforcement.


Key Features:

  Simulated Campus Network: Built using Containerlab to replicate real-world network topology.
  
  OpenConfig Integration: Vendor-neutral configuration using YANG-based data models.
  
  gNMI for Telemetry: Real-time monitoring and data collection.

  gNOI for Automation: Automating network operations such as OS upgrades, diagnostics, and log retrieval.

  gRIBI for Security & Routing: Managing routing tables and implementing firewall rules centrally.

  User Interface: Web-based platform to monitor network performance, apply configurations, and troubleshoot issues.


Usage

Network Configuration

  Use the web interface or CLI to push configurations using OpenConfig

  Deploy VLAN segmentation, IP addressing, and security policies.

Real-Time Monitoring

  View telemetry data from network devices using gNMI.

  Set alerts for performance issues.

Automated Network Operations

  Schedule OS upgrades and maintenance tasks using gNOI.

  Manage routing tables dynamically via gRIBI.


Architecture

The system consists of:

  Network Simulation: Using Containerlab for a virtualised network.

  Configuration Management: OpenConfig YANG models for consistency across vendors.

  Telemetry Collection: gNMI for real-time insights.

  Security & Routing: gRIBI to centralise firewall rules and routing.

  Web Interface: Provides a unified dashboard for monitoring and management.


Testing & Validation

  Unit & Integration Testing: Ensures core functionalities work as expected.

  Performance Testing: Evaluates scalability with alrge device counts.

  Reliability Testing: Simulates failures to validate fault tolerance.

  Usability Testing: Tests the ease of using the web interface.
