pipeline {
    agent any

    environment {
        OAUTH_TOKEN = credentials('yandex-oauth-token')
    }

    stages {
        stage('Test') {
            steps {
                sh '''
                    # Install uv
                    curl -LsSf https://astral.sh/uv/install.sh | sh -s -- -y
                    export PATH="$HOME/.cargo/bin:$PATH"

                    # Create .env file with hardcoded values
                    cat > .env << EOF
                    BASE_URL=https://cloud-api.yandex.net/v1/disk
                    RESOURCE_ENDPOINT=resources
                    TRASH_ENDPOINT=trash/resources
                    OAUTH_TOKEN=$OAUTH_TOKEN
                    EOF

                    # Run tests
                    uv sync
                    uv run pytest tests/ -v

                    # Cleanup
                    rm -f .env
                '''
            }
        }
    }
}
