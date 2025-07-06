$ErrorActionPreference = "Stop"
$LambdaName = "PagamentoAppFiap"

Write-Host "ðŸ§¹ Cleaning previous build..."
if (Test-Path lambda_package) {
    Remove-Item lambda_package -Recurse -Force -ErrorAction SilentlyContinue
}
if (Test-Path function.zip) {
    Remove-Item function.zip -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path lambda_package | Out-Null

Write-Host "ðŸ“¦ Installing dependencies..."
pip install -r requirements.txt -t lambda_package

Write-Host "ðŸ“„ Copying application code..."
Copy-Item -Recurse -Path .\app\interfaces -Destination .\lambda_package\interfaces
Copy-Item -Recurse -Path .\app\application -Destination .\lambda_package\application
Copy-Item -Recurse -Path .\app\domain -Destination .\lambda_package\domain
Copy-Item .\app\lambda_function.py -Destination .\lambda_package\interfaces\lambda_function.py

Write-Host "ðŸ—œï¸ Creating ZIP package..."
Compress-Archive -Path .\lambda_package\* -DestinationPath function.zip

Write-Host "â˜ï¸ Deploying to AWS Lambda..."
aws lambda update-function-code `
  --function-name $LambdaName `
  --zip-file fileb://function.zip
Write-Host "Deployment complete."