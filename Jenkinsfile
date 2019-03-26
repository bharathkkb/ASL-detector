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
            script {
            echo 'This build was successful.'
            if(GIT_BRANCH == 'master'){
            if(GIT_PREVIOUS_SUCCESSFUL_COMMIT == GIT_PREVIOUS_COMMIT){
            echo 'Promoting to staging'
            withCredentials([usernamePassword(credentialsId: 'github-cred', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
            sh"""
            rm -rf git-push-stg
            mkdir git-push-stg
            cd git-push-stg
            git config --global user.email \"bharath.baiju@sjsu.edu\"
            git config --global user.name \"jenkins-bot\"
            git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/bharathkkb/ASL-detector.git
            cd ASL-detector
            git checkout stg
            git branch
            git pull --commit --rebase origin master

            git push origin stg

            """
            }
            }
            else{
                echo 'Not eligible for promoting to staging'
            }
          }
        }
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
