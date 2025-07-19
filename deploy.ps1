$ErrorActionPreference = "Stop"
$LambdaName = "PagamentoAppFiap"

Write-Host "Cleaning previous build..."
if (Test-Path lambda_package) {
    Remove-Item lambda_package -Recurse -Force -ErrorAction SilentlyContinue
}
if (Test-Path function.zip) {
    Remove-Item function.zip -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path lambda_package | Out-Null

Write-Host "Installing dependencies..."
pip install -r requirements.txt -t lambda_package

Write-Host "Copying application code..."
Copy-Item -Recurse -Path .\app -Destination .\lambda_package\app

Write-Host "Creating ZIP package..."
Compress-Archive -Path .\lambda_package\* -DestinationPath function.zip -Force

Write-Host "Deploying to AWS Lambda..."
$deployResult = aws lambda update-function-code `
  --function-name $LambdaName `
  --zip-file fileb://function.zip

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to deploy Lambda package."
    exit 1
} else {
    Write-Host "Lambda package deployed successfully."
}

Write-Host "Setting Lambda handler to 'app.interfaces.lambda_function.handler'..."
& {
    aws lambda update-function-configuration `
        --function-name $LambdaName `
        --handler "app.lambda_function.handler"
}
$handlerExitCode = $LASTEXITCODE

if ($handlerExitCode -ne 0) {
    Write-Error "Failed to update Lambda handler."
    exit 1
} else {
    Write-Host "Lambda handler updated successfully."
}

Write-Host "Deployment complete. Lambda function '$LambdaName' is ready to use."
