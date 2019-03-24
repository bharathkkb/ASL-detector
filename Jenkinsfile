pipeline {
    agent {label 'master'}

    stages {
        stage('Build and test backend locally') {
            steps {
              echo 'Downloading Model'
                script {
                googleStorageDownload bucketUri: 'gs://asl-models/model_keras.h5', credentialsId: 'cs161-jenkins', localDirectory: './asl-api'
                }
                echo 'Building locally'
                sh "ls"
                sh """
                export BUILD_ID=dontKillMe
                python3 --version
                cd asl-api
                python3 -m virtualenv env
                ls
                . env/bin/activate
                pip install -r requirements.txt
                pytest -q test_api.py --url=http://0.0.0.0:5000  --local=0 -vv -s --html=test-results/feature-html-report/index.html --junitxml=test-results/junit/feature-xml-report.xml
                """

            }
        }
        stage('Build and test backend in container') {
            steps {
                echo 'Building backend in a container'
                sh "ls"
                sh """
                docker -v && docker-compose -v
                docker network create -d bridge web_dev
                sleep 5
                docker build -t asl-api -f Dockerfile-api-dev .
                docker run -d --network="web_dev" -p 5000:5000 asl-api:latest
                sleep 10
                docker ps -a
                """
            }
        }
        stage('Build and test front end in container') {
            steps {
                echo 'Building front end in a container'
                sh "ls"
                sh """
                docker build  -t asl-ui -f Dockerfile-ui-dev .
                docker run -d --network="web_dev" -p 5001:80 asl-ui:latest
                sleep 10
                docker ps -a
                """
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
            echo 'Clean up'
            sh """
            result=\$( docker ps -a -q )
            if [ -n "\$result" ]; then
              docker stop \$(docker ps -a -q)
               docker rm \$(docker ps -a -q)
            else
              echo "No containers left"
            fi
           """
           sh """
           docker volume prune -f
           docker network rm web_dev
           docker system prune -f
         """
         echo 'Archive artifacts and test results'
         archive "asl-api/test-results/*"

        junit 'asl-api/test-results/junit/*.xml'
        publishHTML target: [
            allowMissing: false,
            alwaysLinkToLastBuild: false,
            keepAll: true,
            reportDir: 'asl-api/test-results/feature-html-report/',
            reportFiles: 'index.html',
            reportName: 'API BB FeatureTest Coverage Report'
          ]

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
