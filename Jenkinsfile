pipeline {
    agent {label 'master'}

    stages {
        stage('Build and test backend locally') {
            steps {
              echo 'Downloading Model'
                echo 'Building tf serving'
                sh "ls"
                sh """
                docker-compose -f compose-dev.yml up --d --build
                """

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
                """
                sh """
                set +e
                cd asl-api
                . env/bin/activate
                pytest -q test_api.py --url=http://0.0.0.0:5000  --local=1 -vv -s --html=test-results/feature-html-report/index.html --junitxml=test-results/junit/feature-xml-report.xml
                cd wb-unittests
                coverage run --rcfile=.coveragerc -m unittest discover -s . -p '*_testing.py' -v
                """

            }
        }
          stage('Build and test frontend locally') {
            steps {
            echo 'Building tf serving'
            sh "ls"
            sh """
            export FRONTEND_DOMAIN="http://localhost:5050"
            export CI=true npm test
            yarn install
            yarn test-coverage --watchAll=false --forceExit
            yarn test a --watchAll=false --forceExit

            """

          }
        }


    }
    post {
        always {
          sh """
          docker-compose -f compose-dev.yml down
          """

         echo 'Archive artifacts and test results'
         archive "asl-api/test-results/feature-html-report/*"
         archive "asl-api/test-results/junit/*.xml"
         archive "frontend/junit.xml"

        junit 'asl-api/test-results/junit/*.xml'
        junit 'frontend/junit.xml'
        publishHTML target: [
            allowMissing: false,
            alwaysLinkToLastBuild: false,
            keepAll: true,
            reportDir: 'asl-api/test-results/feature-html-report/',
            reportFiles: 'index.html',
            reportName: 'API BB FeatureTest Coverage Report'
          ]
          publishHTML target: [
              allowMissing: false,
              alwaysLinkToLastBuild: false,
              keepAll: true,
              reportDir: 'frontend/jest-stare/',
              reportFiles: 'index.html',
              reportName: 'Front end Unit Test Report'
            ]
            publishHTML target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: 'frontend/coverage/lcov-report/',
                reportFiles: 'index.html',
                reportName: 'Front end Coverage Report'
              ]

        }
        success {
            script {
            echo 'This build was successful.'
            if(GIT_BRANCH == 'master'){
            if(GIT_PREVIOUS_SUCCESSFUL_COMMIT == GIT_PREVIOUS_COMMIT){
            echo 'Promoting to staging'
            withCredentials([usernamePassword(credentialsId: 'github', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
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
