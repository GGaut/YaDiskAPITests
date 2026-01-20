node {
    env.BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
    env.RESOURCE_ENDPOINT = 'resources'
    env.TRASH_ENDPOINT = 'trash/resources'
    env.OAUTH_TOKEN = credentials('Ya_disk_token')
    env.ALLURE_HOME = tool 'allure'

    stage('Install Python and uv') {
        sh '''
            apt-get update && apt-get install -y python3 curl
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.local/bin:$PATH"
            uv --version
        '''
    }

    stage('Create .env file') {
        sh '''
            export PATH="$HOME/.local/bin:$PATH"
            echo "BASE_URL=$BASE_URL" > .env
            echo "OAUTH_TOKEN=$OAUTH_TOKEN" >> .env
            echo "RESOURCE_ENDPOINT=$RESOURCE_ENDPOINT" >> .env
            echo "TRASH_ENDPOINT=$TRASH_ENDPOINT" >> .env
        '''
    }

    stage('Install dependencies') {
        sh '''
            export PATH="$HOME/.local/bin:$PATH"
            uv sync
        '''
    }

    stage('Run tests') {
        sh '''
            rm -rf allure_results
            mkdir allure_results

            export PATH="$HOME/.local/bin:$PATH"
            uv run pytest --alluredir=allure_results --junitxml=junit.xml
        '''
    }

    stage('Publish Allure') {
        allure includeProperties: false,
               jdk: '',
               reportBuildPolicy: 'ALWAYS',
               results: [[path: 'allure_results']]

        sh '''
            export PATH="$ALLURE_HOME/bin:$PATH"
            cp /var/jenkins_home/jobs/$JOB_NAME/builds/$BUILD_NUMBER/archive/allure-report.zip \
            . || echo "ZIP не найден"
        '''
    }

    stage('Collect JUnit results') {
        junit 'junit.xml'

        def tr = currentBuild.rawBuild.getAction(hudson.tasks.junit.TestResultAction)

        total   = tr.totalCount
        passed  = tr.result.passCount
        failed  = tr.result.failCount
        skipped = tr.result.skipCount

        failedTests = tr.failedTests.collect { t ->
            "<li>FAILED: ${t.fullName}</li>"
        }.join("\n")
    }

    stage('Send email') {
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
                        <li>Общее количество тестов: <b>${total}</b></li>
                        <li>Успешно: <b style="color:green;">${passed}</b></li>
                        <li>Провалено: <b style="color:red;">${failed}</b></li>
                        <li>Пропущено: <b style="color:orange;">${skipped}</b></li>
                    </ul>

                    <h4>Проваленные тесты:</h4>
                    <ul>${failedTests ?: "<i>Нет упавших тестов</i>"}</ul>

                    <p><a href="${env.BUILD_URL}allure">Отчет Allure</a></p>
                </body>
                </html>
            """,
            to: "sokol_night@mail.ru",
            attachmentsPattern: 'allure-report.zip'
        )
    }
}
