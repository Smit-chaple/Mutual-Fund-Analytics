$project = Split-Path -Parent $PSScriptRoot
$python = (Get-Command python).Source
$script = Join-Path $project "SCRIPTS\run_pipeline.py"

$action = New-ScheduledTaskAction `
    -Execute $python `
    -Argument "`"$script`"" `
    -WorkingDirectory $project

$trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At 8:00PM

Register-ScheduledTask `
    -TaskName "MutualFundAnalytics_ETL" `
    -Action $action `
    -Trigger $trigger `
    -Description "Runs MutualFundAnalytics ETL every weekday at 8 PM" `
    -Force

Write-Host "Scheduled ETL created successfully."