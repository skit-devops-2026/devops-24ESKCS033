pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        PROJECT_NAME  = 'RealEstate – Property Discovery Platform'
        STUDENT_ID    = '24ESKCS019'
        STUDENT_NAME  = 'Akshat Gupta'
        TEST_DIR      = 'tests'
        REPORTS_DIR   = 'reports'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=== Checking out source repository ==="
                echo "Project  : ${env.PROJECT_NAME}"
                echo "Student  : ${env.STUDENT_NAME} (${env.STUDENT_ID})"
                checkout scm
            }
        }

        stage('Environment Info') {
            steps {
                echo '=== System Environment Information ==='
                sh 'python3 --version || python --version || echo "Python not found"'
                sh 'git --version || echo "Git not found"'
                sh 'echo "Workspace: $WORKSPACE"'
                sh 'ls -la'
            }
        }

        stage('Setup Virtualenv') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install pytest pytest-cov flake8
                '''
            }
        }

        stage('Lint & Code Quality') {
            steps {
                echo 'Running Flake8 static analysis and syntax validation...'
                sh '''
                    . venv/bin/activate
                    # Stop build on critical Python syntax errors or undefined names
                    flake8 tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
                    # Non-fatal style warnings
                    flake8 tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Executing unit test suite and generating JUnit XML report...'
                sh '''
                    mkdir -p ${REPORTS_DIR}
                    . venv/bin/activate
                    pytest tests/ -v \
                        --junitxml=${REPORTS_DIR}/jenkins-test-results.xml \
                        --cov=tests \
                        --cov-report=term-missing
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
            echo "=== Jenkins Build Succeeded! | ${env.PROJECT_NAME} | ${env.STUDENT_NAME} (${env.STUDENT_ID}) ==="
        }
        failure {
            echo "=== Jenkins Build FAILED! | ${env.PROJECT_NAME} | ${env.STUDENT_NAME} (${env.STUDENT_ID}) ==="
        }
    }
}
