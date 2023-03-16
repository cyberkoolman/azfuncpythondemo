$jsonData = Get-Content -Path ".\Azure_data.json" -Raw
Write-Host $jsonData
$headers = @{
	"Content-Type" = "application/json"
}
$data = $jsonData
$uri = "http://localhost:7071/api/AlertReceived"

$response = Invoke-WebRequest -Uri $uri -Method Post -Headers $headers -Body $data
$response.Content