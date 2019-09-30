node {
  checkout scm
  switch(env.BRANCH_NAME) {
    case "develop":
      runBuild()
      runTest()
      build job: 'staging', parameters: [[$class: 'StringParameterValue', name: 'BRANCH_NAME', value: "develop"]]
    break
    
    default:
      runBuild()
      runTest()
      build job: 'nightly', parameters: [[$class: 'StringParameterValue', name: 'BRANCH_NAME', value: "${env.BRANCH_NAME}"]]
    break
  }
}