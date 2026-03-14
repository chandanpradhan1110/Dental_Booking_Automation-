#!/bin/bash

set -e

mkdir -p dental_agent/{config,models,tools,agents,workflows}

touch .env


touch dental_agent/__init__.py
touch dental_agent/agent.py

touch dental_agent/config/__init__.py
touch dental_agent/config/settings.py

touch dental_agent/models/__init__.py
touch dental_agent/models/state.py

touch dental_agent/tools/__init__.py
touch dental_agent/tools/csv_reader.py
touch dental_agent/tools/csv_writer.py

touch dental_agent/agents/__init__.py
touch dental_agent/agents/supervisor.py
touch dental_agent/agents/info_agent.py
touch dental_agent/agents/booking_agent.py
touch dental_agent/agents/cancellation_agent.py
touch dental_agent/agents/rescheduling_agent.py

touch dental_agent/workflows/__init__.py
touch dental_agent/workflows/graph.py

echo "✅ Structure created successfully!"