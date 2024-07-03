import argparse
import subprocess
import time
import os
import sys

""" 
This script is used by the pipeline to determine which repository/service has changes that needs to be tested, 
it executes the test suites for all services that have a change per push.
"""

# Define the mapping of folders to services
FOLDER_SERVICE_MAP = {
    "jobboard": "jobboard-test",
}

# Define the compose file for each environment
COMPOSE_FILES = {
    "development": "docker-compose.yaml",
    "staging": "docker-compose-staging.yaml",
    "production": "docker-compose-prod.yaml",
    "test": "docker-compose-test.yaml"
}

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Run Docker Compose tests based on changed directories.')
    parser.add_argument('--directory', type=str, required=True, help='Comma-separated list of changed directories.')
    parser.add_argument('--environment', type=str, default='test', choices=['development', 'staging', 'production', 'test'], help='Deployment environment (default: test).')
    return parser.parse_args()

def run_command(command):
    """Run a shell command and exit if it fails."""
    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def setup_test_environment():
    """Set up the test environment (e.g., starting test databases)."""
    print("Setting up the test environment...")
    run_command(['docker', 'compose', '-f', 'docker-compose-test.yaml', 'up', 'elasticsearch', '-d'])
    # Wait for Elasticsearch to start up
    time.sleep(10)  # Increased to ensure DB readiness


def run_tests(service, compose_file):
    """Run tests for a specific service."""
    print(f"Running tests for service: {service}")
    # Start the service
    run_command(['docker', 'compose', '-f', compose_file, 'up', service, '--build', '-d'])

    # Wait for the service to be fully up
    time.sleep(10)

    # Execute the test script inside the container
    try:
        run_command(['docker', 'exec', '-i', service, './tests/report.sh'])
    except subprocess.CalledProcessError as e:
        print(f"Tests failed for service {service} with exit code {e.returncode}")
        # Stop and remove the service container after tests
        run_command(['docker', 'compose', '-f', compose_file, 'down'])
        sys.exit(e.returncode)

    # Stop and remove the service container after tests
    run_command(['docker', 'compose', '-f', compose_file, 'down'])

def main():
    args = parse_args()

    # Determine the compose file based on the environment
    compose_file = COMPOSE_FILES.get(args.environment, COMPOSE_FILES['test'])
    
    # Ensure CHANGED_DIRS is not empty
    if not args.directory:
        print("No changed directories specified. Exiting.")
        sys.exit(1)

    # Split CHANGED_DIRS by comma into an array
    changed_dirs = args.directory.split(',')
    
    # Set up the required test environment
    setup_test_environment()

    # Determine which services to test
    services_to_test = []
    for dir in changed_dirs:
        if dir in FOLDER_SERVICE_MAP:
            service = FOLDER_SERVICE_MAP[dir]
            if service not in services_to_test:
                services_to_test.append(service)
        else:
            print(f"Directory {dir} does not map to any service. Skipping.")

    # If no services to test, exit
    if not services_to_test:
        print("No relevant services to test based on changes.")
        sys.exit(0)

    # Print services to test
    print(f"Services to test: {', '.join(services_to_test)}")

    # Run tests for each service
    for service in services_to_test:
        run_tests(service, compose_file)

    # Clean up Docker volumes (optional)
    run_command(['docker', 'volume', 'prune', '-f'])

if __name__ == "__main__":
    main()
