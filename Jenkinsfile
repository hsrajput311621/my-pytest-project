// pipeline {
//   agent any

//   environment {
//     // Where we will save reports and screenshots
//     REPORTS_DIR = "reports"
//     SCREEN_DIR  = "screenshots"
//     VENV_DIR    = ".venv"
//     PYTHON      = "${WORKSPACE}/.venv/bin/python"
//     PIP         = "${WORKSPACE}/.venv/bin/pip"
//   }

//   stages {
//     stage('Checkout') {
//       steps {
//         checkout scm
//       }
//     }

//     stage('Set up Python') {
//       steps {
//         sh '''
//           python3 -V || true
//           python3 -m venv ${VENV_DIR}
//           ${PIP} install --upgrade pip
//           # Install your deps
//           if [ -f requirements.txt ]; then
//             ${PIP} install -r requirements.txt
//           else
//             ${PIP} install selenium pytest pytest-html allure-pytest pytest-xdist webdriver-manager
//           fi
//         '''
//       }
//     }

//     stage('Prepare Folders') {
//       steps {
//         sh '''
//           mkdir -p ${REPORTS_DIR} ${SCREEN_DIR}
//         '''
//       }
//     }

//     stage('Run Tests') {
//       steps {
//         // Add headless flags in your driver if running on a Linux agent without display
//         sh '''
//           ${VENV_DIR}/bin/pytest \
//             -m "not slow" \
//             --maxfail=1 \
//             --html=${REPORTS_DIR}/report.html --self-contained-html \
//             -q
//         '''
//       }
//     }
//   }

//   post {
//     always {
//       // Archive artifacts so you can download them from Jenkins
//       archiveArtifacts artifacts: "${REPORTS_DIR}/**", onlyIfSuccessful: false
//       archiveArtifacts artifacts: "${SCREEN_DIR}/**", onlyIfSuccessful: false

//       // If you use junit XML reports, publish them too (optional)
//       // junit 'reports/junit/*.xml'

//       // If using Allure (optional), uncomment once plugin installed and results are generated
//       // allure([
//       //   includeProperties: false,
//       //   jdk: '',
//       //   properties: [],
//       //   reportBuildPolicy: 'ALWAYS',
//       //   results: [[path: 'allure-results']]
//       // ])
//     }
//   }
// }
pipeline {
  agent any

  environment {
    REPORTS_DIR = "reports"
    SCREEN_DIR  = "screenshots"
    VENV_DIR    = ".venv"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set up Python') {
      steps {
        // We use 'bat' instead of 'sh' for Windows!
        bat """
          python -m venv ${VENV_DIR}
          ${VENV_DIR}\\Scripts\\pip install --upgrade pip
          ${VENV_DIR}\\Scripts\\pip install selenium pytest pytest-html allure-pytest webdriver-manager
        """
      }
    }

    stage('Prepare Folders') {
      steps {
        // Windows command to make folders
        bat "if not exist ${REPORTS_DIR} mkdir ${REPORTS_DIR}"
        bat "if not exist ${SCREEN_DIR} mkdir ${SCREEN_DIR}"
      }
    }

    stage('Run Tests') {
      steps {
        // Run pytest from the virtual environment
        bat "${VENV_DIR}\\Scripts\\pytest -m smoke --html=${REPORTS_DIR}\\report.html --self-contained-html"
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: "${REPORTS_DIR}/**", allowEmptyArchive: true
    }
  }
}
