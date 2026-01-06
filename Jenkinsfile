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
                bat 'pytest --html=report.html --self-contained-html'
            }
        }
    }

    post {
        always {
            // Publish HTML report
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Playwright Test Report'
            ])

            // Send email for every build
            emailext(
                subject: "Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
Hello,

Build Status: ${currentBuild.currentResult}

Job Name: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}

Jenkins Build URL:
${env.BUILD_URL}

Playwright HTML Report:
${env.BUILD_URL}Playwright_20Test_20Report/

Regards,
Jenkins
""",
                to: "esamsettitushparaj@gmail.com"
            )
        }
    }
}
