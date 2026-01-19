pipeline {
    agent any

    triggers {
        cron('55 13 * * *')
    }

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
                    apt-get update && apt-get install -y python3 curl
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
                    uv run pytest --alluredir=allure_results
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   jdk: '',
                   reportBuildPolicy: 'ALWAYS',
                   results: [[path: 'allure_results']]

            mail to: 'sokol_night@mail.ru',
                 subject: "Автотесты ${env.JOB_NAME} - #${env.BUILD_NUMBER}",
                 body: "Статус: ${currentBuild.result}\nСсылка: ${env.BUILD_URL}allure"
        }
    }
}
