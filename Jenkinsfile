pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                // Run tests and generate pytest-html report
                bat 'pytest --html=report.html --self-contained-html'
            }
        }
    }

    post {
        always {

            // Publish HTML report in Jenkins
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Playwright Test Report'
            ])

            // Send email after every build (SUCCESS / FAILURE / UNSTABLE)
            emailext(
                subject: "Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                mimeType: 'text/html',
                body: """
                    <p><b>Build Status:</b> ${currentBuild.currentResult}</p>
                    <p><b>Job Name:</b> ${env.JOB_NAME}</p>
                    <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>

                    <p>
                        <b>Jenkins Build URL:</b><br>
                        <a href="${env.BUILD_URL}">${env.BUILD_URL}</a>
                    </p>

                    <p>
                        <b>Playwright Test Report:</b><br>
                        <a href="${env.BUILD_URL}Playwright_Test_Report/">
                            View HTML Report
                        </a>
                    </p>

                    <p>Regards,<br>Jenkins</p>
                """,
                to: "esamsettitushparaj@gmail.com"
            )
        }
    }
}
