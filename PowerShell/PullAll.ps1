if ($args.Count -eq 1)
{
    $rootDir = $args[0]
}
else
{
    $rootDir = "."    
}
Write-Host $("Root directory is $rootDir")

Get-ChildItem -Directory -Path $rootDir | Foreach-Object {
    if (Test-Path "$($rootDir)\$($_)\.git")
    {
        Write-Host "> Pulling $($_)" -ForegroundColor Green
        Set-Location "$($rootDir)\$_"
        git pull
        Set-Location ..
    }
}

Read-Host -Prompt "Press Enter to exit"