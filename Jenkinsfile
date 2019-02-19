pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building'
                sh """
                export BUILD_ID=dontKillMe
                python3 --version
                cd asl-api
                python3 -m virtualenv env
                ls
                . env/bin/activate
                pip install -r requirements.txt

                python server.py -t &
                pytest -q test_api.py --url=http://0.0.0.0:5000

                """

            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
