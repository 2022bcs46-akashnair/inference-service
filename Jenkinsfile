pipeline {
    agent any

    environment {
        IMAGE_NAME = "akash0906/akashnair-22bcs46-wine-api:v1"
        CONTAINER_NAME = "wine-api-container"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                echo "Pulling Docker image..."
                sh "docker pull $IMAGE_NAME"
            }
        }

        stage('Run Container') {
            steps {
                echo "Running container..."
                sh """
                docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $IMAGE_NAME
                """
            }
        }

        stage('Wait for Readiness') {
            steps {
                echo "Waiting for API..."
                sh "sleep 5"
            }
        }

        stage('Valid Inference Test') {
            steps {
                script {
                    def response = sh(
                        script: '''
                        curl -s -X POST http://host.docker.internal:8000/predict \
                        -H "Content-Type: application/json" \
                        -d '{
                          "fixed_acidity": 7.4,
                          "volatile_acidity": 0.7,
                          "citric_acid": 0.0,
                          "residual_sugar": 1.9,
                          "chlorides": 0.076,
                          "free_sulfur_dioxide": 11.0,
                          "total_sulfur_dioxide": 34.0,
                          "density": 0.9978,
                          "pH": 3.51,
                          "sulphates": 0.56,
                          "alcohol": 9.4
                        }'
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains("prediction")) {
                        error("Valid inference FAILED")
                    }
                }
            }
        }

        stage('Invalid Input Test') {
            steps {
                script {
                    def status = sh(
                        script: '''
                        curl -s -o /dev/null -w "%{http_code}" \
                        -X POST http://host.docker.internal:8000/predict \
                        -H "Content-Type: application/json" \
                        -d '{"fixed_acidity": 7.4}'
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Invalid Test Status Code: ${status}"

                    if (status == "200") {
                        error("Invalid input test FAILED")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                sh """
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                """
            }
        }
    }

    post {
        success {
            echo "PIPELINE SUCCESS"
        }
        failure {
            echo "PIPELINE FAILED"
        }
        always {
            sh "docker ps -a"
        }
    }
}