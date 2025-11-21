# Monitor replace_printf_logger_all script progress
$logFile = "replace_printf_output.log"
$processId = 28224

Write-Host "Monitoring script progress (Process ID: $processId)..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
Write-Host ""

while ($true) {
    Start-Sleep -Seconds 30
    
    # Check if process is still running
    $proc = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if (-not $proc) {
        Write-Host "`nProcess has finished!" -ForegroundColor Green
        if (Test-Path $logFile) {
            Write-Host "`nLast 20 lines of output:" -ForegroundColor Cyan
            Get-Content $logFile -Tail 20
        }
        break
    }
    
    # Check log file for progress
    if (Test-Path $logFile) {
        $lines = Get-Content $logFile
        $lastLine = $lines[-1]
        
        # Check if script completed
        if ($lastLine -match "SUMMARY" -or $lastLine -match "Total files:") {
            Write-Host "`nScript completed!" -ForegroundColor Green
            Get-Content $logFile -Tail 15
            break
        }
        
        # Extract progress
        $progressLines = $lines | Select-String -Pattern "\[(\d+)/680\]" | Select-Object -Last 1
        if ($progressLines) {
            $current = $progressLines.Matches.Groups[1].Value
            $percent = [math]::Round([int]$current / 680 * 100, 1)
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Progress: $current/680 ($percent%)" -ForegroundColor Green
        }
    } else {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Waiting for log file..." -ForegroundColor Yellow
    }
}

