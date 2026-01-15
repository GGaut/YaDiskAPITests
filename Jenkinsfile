pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }

    environment {
        BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
        RESOURCE_ENDPOINT = 'resources'
        TRASH_ENDPOINT = 'trash/resources'
        OAUTH_TOKEN = credentials('Ya_disk_token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install uv') {
            steps {
                sh '''
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"
                    uv --version
                '''
            }
        }

        stage('Create .env file') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    echo "BASE_URL=$BASE_URL" > .env
                    echo "OAUTH_TOKEN=$OAUTH_TOKEN" >> .env
                    echo "RESOURCE_ENDPOINT=$RESOURCE_ENDPOINT" >> .env
                    echo "TRASH_ENDPOINT=$TRASH_ENDPOINT" >> .env
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    uv sync
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    uv run pytest
                '''
            }
        }
    }
}


