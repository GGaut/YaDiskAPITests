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

            emailext (
                subject: "Результаты автотестов для ${env.JOB_NAME} - Сборка #${env.BUILD_NUMBER}",
                body: """
                    <!DOCTYPE html>
                    <html>
                    <head><meta charset="UTF-8"></head>
                    <body>
                        <p>Автоматический прогон тестов для проекта <b>${env.JOB_NAME}</b> (Сборка #${env.BUILD_NUMBER}) завершился со статусом <b style="color:green;">${currentBuild.result}</b>.</p>
                        <p><a href="${env.BUILD_URL}allure">Просмотреть отчет Allure</a></p>
                        <p>Архив с отчетом прикреплен к этому письму.</p>
                    </body>
                    </html>
                """,
                to: "sokol_night@mail.ru",
                mimeType: "text/html"
                attachmentsPattern: 'allure-report.zip'
            )
        }
    }
}
