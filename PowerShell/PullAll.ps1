Get-ChildItem -Directory | Foreach-Object {
    if (Test-Path "$($_)\.git")
    {
        Write-Host "> Pulling $($_)" -ForegroundColor Green
        Set-Location $_
        git pull
        Set-Location ..
    }
}

Read-Host -Prompt "Press Enter to exit"