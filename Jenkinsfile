pipeline {
    agent any

    environment {
        BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
        RESOURCE_ENDPOINT = 'resources'
        TRASH_ENDPOINT = 'trash/resources'
        OAUTH_TOKEN = credentials('Ya_disk_token')
        ALLURE_HOME = tool 'allure'
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
                    rm -rf allure_results
                    mkdir allure_results

                    export PATH="$HOME/.local/bin:$PATH"
                    uv run pytest --alluredir=allure_results --junitxml=junit.xml
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

            sh '''
                export PATH="$ALLURE_HOME/bin:$PATH"
                cp /var/jenkins_home/jobs/$JOB_NAME/builds/$BUILD_NUMBER/archive/allure-report.zip \
                . || echo "ZIP не найден"
            '''

            junit 'junit.xml'

            script {
                def testResultAction = currentBuild.rawBuild.getAction(hudson.tasks.junit.TestResultAction)

                def failedTests = testResultAction.failedTests.collect { test ->
                    "FAILED: ${test.fullName}"
                }

                env.FAILED_TEST_LIST = failedTests ?
                    failedTests.collect { "<li>${it}</li>" }.join("\n") :
                    "<i>Нет упавших тестов</i>"

                env.ALLURE_TESTS_TOTAL  = testResultAction.totalCount.toString()
                env.ALLURE_TESTS_PASSED = testResultAction.result.passCount.toString()
                env.ALLURE_TESTS_FAILED = testResultAction.result.failCount.toString()
                env.ALLURE_TESTS_SKIPPED = testResultAction.result.skipCount.toString()
            }


                env.FAILED_TEST_LIST = failedTests ?
                    failedTests.collect { "<li>${it}</li>" }.join("\n") :
                    "<i>Нет упавших тестов</i>"
            }

            emailext(
                subject: "Результаты автотестов для ${env.JOB_NAME} - Сборка #${env.BUILD_NUMBER}",
                body: """
                    <!DOCTYPE html>
                    <html>
                    <head><meta charset="UTF-8"></head>
                    <body>
                        <h3>Результаты тестирования</h3>

                        <h4>Статистика тестов:</h4>
                        <ul>
                            <li>Общее количество тестов: <b>${env.ALLURE_TESTS_TOTAL}</b></li>
                            <li>Успешно: <b style="color:green;">${env.ALLURE_TESTS_PASSED}</b></li>
                            <li>Провалено: <b style="color:red;">${env.ALLURE_TESTS_FAILED}</b></li>
                            <li>Пропущено: <b style="color:orange;">${env.ALLURE_TESTS_SKIPPED}</b></li>
                        </ul>

                        <h4>Проваленные тесты:</h4>
                        <ul>${env.FAILED_TEST_LIST}</ul>

                        <p><a href="${env.BUILD_URL}allure">Отчет Allure</a></p>
                    </body>
                    </html>
                """,
                to: "sokol_night@mail.ru",
                attachmentsPattern: 'allure-report.zip'
            )
        }
    }
}
