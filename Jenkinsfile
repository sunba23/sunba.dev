pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Load Environment Variables') {
            steps {
                script {
                    def envFile = '.env'
                    def envVars = readFile(envFile).split('\n').collectEntries { line ->
                        def parts = line.split('=')
                        [(parts[0].trim()): parts[1].trim()]
                    }
                    envVars.each { key, value ->
                        env[key] = value
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def buildArgs = "--build-arg POSTGRES_DB=${env.POSTGRES_DB} --build-arg POSTGRES_USER=${env.POSTGRES_USER} --build-arg POSTGRES_PASSWORD=${env.POSTGRES_PASSWORD} --build-arg POSTGRES_HOST=${env.POSTGRES_HOST} --build-arg POSTGRES_PORT=${env.POSTGRES_PORT}"
                    echo "Building Docker image ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_TAG}"
                    sh "docker build ${buildArgs} -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_TAG} ."
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_TAG} to ${env.DOCKER_REGISTRY}"
                    docker.withRegistry("https://${env.DOCKER_REGISTRY}", env.DOCKER_CREDENTIALS_ID) {
                        sh "docker push ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_TAG}"
                    }
                }
            }
        }
    }
}
