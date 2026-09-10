pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        PYTHON_APP = 'cart.py'
        TEST_RUNNER = 'pytest'
        REPORTS_DIR = 'reports'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source repository...'
                checkout scm
            }
        }

        stage('Environment Info') {
            steps {
                echo '=== System Environment Information ==='
                sh 'python3 --version || python --version || true'
                sh 'git --version || true'
            }
        }

        stage('Setup Virtualenv') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate || . venv/Scripts/activate
                    python -m pip install --upgrade pip
                    pip install pytest pytest-cov flake8
                '''
            }
        }

        stage('Lint & Code Quality') {
            steps {
                echo 'Running Flake8 static analysis and syntax validation...'
                sh '''
                    . venv/bin/activate || . venv/Scripts/activate
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Executing unit test suite and generating JUnit XML report...'
                sh '''
                    mkdir -p reports
                    . venv/bin/activate || . venv/Scripts/activate
                    pytest -v --junitxml=reports/jenkins-test-results.xml --cov=cart --cov-report=term-missing
                '''
            }
        }

        stage('Archive Test Results') {
            steps {
                echo 'Archiving test reports...'
                archiveArtifacts artifacts: 'reports/*.xml', fingerprint: true, allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Collecting JUnit test results...'
            junit testResults: 'reports/*.xml', allowEmptyResults: true
        }
        success {
            echo '=== Jenkins Build Succeeded! ==='
        }
        failure {
            echo '=== Jenkins Build Failed! ==='
        }
    }
}
