pipeline {
    agent any

    environment {
        BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
        RESOURCE_ENDPOINT = 'resources'
        TRASH_ENDPOINT = 'trash/resources'
        OAUTH_TOKEN = credentials('Ya_disk_token')
    }

    stages {
        stage('Install Python and uv') {
            steps {
                sh '''
                    apt-get update && apt-get install -y python3 python3-pip curl
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

        stage('Run tests with allure') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    uv run pytest --alluredir=allure_results-${BUILD_NUMBER}
                '''
            }
        }

        stage('Generate and archibe report') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    mkdir -p allure_history
                    allure generate --clean allure_results-${BUILD_NUMBER} -o allure_history/${BUILD_NUMBER}
                '''
            }
        }
    }
    post {
        always {
            publishHTML(
                target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: "allure_history/${BUILD_NUMBER}",
                    reportFiles: 'index.html',
                    reportName: "Allure Report #${BUILD_NUMBER}",
                    reportTitles: "Test Results for Build ${BUILD_NUMBER}"
                ]
            )
            archiveArtifacts artifacts: "allure_results-${BUILD_NUMBER}/**/*,allure_history/${BUILD_NUMBER}/**/*", fingerprint: true
        }
    }
}

