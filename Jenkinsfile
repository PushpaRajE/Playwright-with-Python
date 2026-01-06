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
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Playwright Test Report'
            ])
        }
    }
}
