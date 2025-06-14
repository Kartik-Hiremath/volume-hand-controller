pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'kartikhiremath/volume-hand-controller'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Kartik-Hiremath/volume-hand-controller.git'}}
        stage('SonarQube Analysis') {
  steps {
    withCredentials([string(credentialsId: 'Sonar', variable: 'SONAR_TOKEN')]) {
      sh '''
        sonar-scanner \
          -Dsonar.projectKey=volume-hand-controller \
          -Dsonar.sources=. \
          -Dsonar.host.url=http://localhost:9000 \
          -Dsonar.login=$SONAR_TOKEN
      '''}}}
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'}}
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE
                    '''}}}}
    post {
        always {
            echo 'Pipeline execution complete!'}}
}
